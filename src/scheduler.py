# src/scheduler.py
from rich.console import Console
from datetime import datetime
from transaction import Transaction, TransactionStatus
from data_item import DataItem

console = Console(record=True)  # permite salvar em arquivo depois


class Scheduler:
    def __init__(self):
        self.data_store = {}   # nome -> DataItem
        self.transactions = {} # id -> Transaction
        self.HI = []           # História inicial
        self.HF = []           # História final
        self.log_enabled = True

    def add_operation(self, op_str):
        op_str = op_str.strip().lower()
        if op_str.startswith("c"):
            tid = op_str[1:]
            self.HI.append(("commit", tid, None))
        else:
            action = op_str[0]
            tid = op_str[1]
            data = op_str[3:-1]
            self.HI.append((action, tid, data))

    def ensure_transaction(self, tid):
        if tid not in self.transactions:
            self.transactions[tid] = Transaction(tid)
            console.print(f"[bold cyan]Nova transação criada:[/bold cyan] {self.transactions[tid]}")
        return self.transactions[tid]

    def ensure_data(self, data_name):
        if data_name not in self.data_store:
            self.data_store[data_name] = DataItem(data_name)
        return self.data_store[data_name]

    def execute(self):
        console.rule("[bold green]Início da Simulação[/bold green]")
        i = 0
        while i < len(self.HI):
            op_type, tid, data_name = self.HI[i]
            tx = self.ensure_transaction(tid)

            if tx.status == TransactionStatus.ABORTED:
                i += 1
                continue

            if op_type == "commit":
                self.commit_transaction(tx)
            elif op_type == "r":
                self.read_operation(tx, data_name)
            elif op_type == "w":
                self.write_operation(tx, data_name)

            i += 1

        console.rule("[bold yellow]História Final (HF)[/bold yellow]")
        for op in self.HF:
            console.print(op)

        if self.log_enabled:
            self.save_log()

    # -------------------------------
    # Operações do protocolo
    # -------------------------------
    def read_operation(self, tx, data_name):
        data = self.ensure_data(data_name)
        console.print(f"[blue]Tentando executar[/blue] r{tx.id}({data_name})")

        if tx.timestamp < data.wts:
            console.print(f"[red]r{tx.id}({data_name}) rejeitada[/red] → T{tx.id} abortada (WTS > TS)")
            self.abort_transaction(tx)
            return

        data.rts = max(data.rts, tx.timestamp)
        self.HF.append(f"r{tx.id}({data_name})")
        tx.operations.append(f"r{tx.id}({data_name})")
        console.print(f"[green]Executada[/green] r{tx.id}({data_name}) → RTS({data_name})={data.rts:.0f}")

    def write_operation(self, tx, data_name):
        data = self.ensure_data(data_name)
        console.print(f"[blue]Tentando executar[/blue] w{tx.id}({data_name})")

        if tx.timestamp < data.rts:
            console.print(f"[red]w{tx.id}({data_name}) rejeitada[/red] → T{tx.id} abortada (RTS > TS)")
            self.abort_transaction(tx)
            return
        if tx.timestamp < data.wts:
            console.print(f"[red]w{tx.id}({data_name}) rejeitada[/red] → T{tx.id} abortada (WTS > TS)")
            self.abort_transaction(tx)
            return

        data.wts = tx.timestamp
        self.HF.append(f"w{tx.id}({data_name})")
        tx.operations.append(f"w{tx.id}({data_name})")
        console.print(f"[green]Executada[/green] w{tx.id}({data_name}) → WTS({data_name})={data.wts:.0f}")

    def commit_transaction(self, tx):
        if tx.status == TransactionStatus.ACTIVE:
            tx.status = TransactionStatus.COMMITTED
            self.HF.append(f"c{tx.id}")
            console.print(f"[bold green]Transação T{tx.id} commitada[/bold green]")

    def abort_transaction(self, tx):
        tx.status = TransactionStatus.ABORTED
        console.print(f"[yellow]Removendo operações anteriores de T{tx.id} da HF...[/yellow]")

        self.HF = [op for op in self.HF if not (f"{tx.id}" in op and op.startswith(("r", "w")))]
        console.print(f"[italic]T{tx.id} reiniciando com novo timestamp...[/italic]")

        new_tx = Transaction(tx.id)
        self.transactions[tx.id] = new_tx
        tx.operations.clear()

    # -------------------------------
    # LOG EM ARQUIVO
    # -------------------------------
    def save_log(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = f"execution_log_{timestamp}.txt"
        console.save_text(log_path)
        console.print(f"\n[bold cyan]→ Log salvo em:[/bold cyan] {log_path}\n")
