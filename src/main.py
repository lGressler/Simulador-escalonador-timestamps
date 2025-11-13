# src/main.py
from scheduler import Scheduler
from utils import parse_history_input

def main():
    print("=== Simulador de Escalonamento com Timestamps ===\n")
    hi_input = input("Digite a História Inicial (ex: r1(x) w2(x) r2(y) w1(y) c1 c2):\n> ")

    scheduler = Scheduler()
    for op in parse_history_input(hi_input):
        scheduler.add_operation(op)

    print("\n--- Executando simulação ---\n")
    scheduler.execute()

if __name__ == "__main__":
    main()
