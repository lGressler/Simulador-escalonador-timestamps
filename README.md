# Relatório — Simulador de Escalonamento com Protocolo de Timestamps

## Aluno
**Nome:** Lucas Gressler  
**Disciplina:** Banco de Dados  
**Trabalho:** Escalonamento com Protocolo de Timestamps

---

## Como rodar

1. python -m venv .venv
2. Ativar o amb. virtual do python: .venv\Scripts\Activate.ps1
3. python.exe -m pip install --upgrade pip
4. pip install rich
5. Rode o simulador: python src/main.py
6. Resultado sairá em um arquivo txt

Historia teste: 

r1(x) w1(x) c1 r2(x) w2(x) c2 (simples)
r1(x) w2(x) w1(x) c2 c1 (Abort de transação antiga por conflito com escrita posterior)
w1(x) r2(x) c1 c2 (Abort da transação jovem por leitura suja / leitura após escrita futura)
r1(x) r2(x) w3(x) w1(x) w2(x) c3 c1 c2 (Multi-abort e reexecução / caso mais complexo)
HI curta pra ver reexecução visível rapidamente: r1(x) w2(x) w1(x) c2 c1

---

## Objetivo
Implementar, de forma simulada, um escalonador de transações que utilize o protocolo de *timestamps* (marcadores de tempo), controlando a execução de leituras, escritas e commits em um ambiente concorrente.

---

## Funcionamento
O programa recebe uma **História Inicial (HI)** como entrada, composta por operações no formato:

Cada operação é analisada em sequência pelo escalonador.  
Quando uma transação realiza sua primeira operação, é atribuído um *timestamp*.  
O escalonador aplica o protocolo de *timestamps*, comparando os *RTS* e *WTS* de cada dado antes de permitir leituras e escritas.

Se uma operação violar as regras do protocolo, a transação é abortada e reiniciada com um novo *timestamp*.

---

## Estrutura

| Estrutura        | Descrição |
|------------------|-----------|
| `Transaction`    | Armazena ID, timestamp, status e operações. |
| `DataItem`       | Controla RTS e WTS de cada dado. |
| `Scheduler`      | Gerencia HI, HF, execuções, abortos e logs. |

project/
├── main.py # Ponto de entrada
├── scheduler.py # Escalonador e controle de timestamps
├── transaction.py # Classe Transaction
├── data_item.py # Estrutura de dados manipulados
├── logger.py # Sistema de logs (console + arquivo)
├── init.py

---

## Características
- Protocolo completo de *timestamps* (leitura, escrita, commit e abort).  
- Geração de **História Final (HF)** corrigida.  
- Reexecução automática de transações abortadas.  
- Saída colorida e detalhada no terminal (via `rich`).  
- **Log automático** em arquivo txt.

---

## Entrada e Saída

### Entrada:
História Inicial digitada pelo usuário.

### Saída:
- Execução passo a passo no terminal.  
- Log salvo em arquivo no diretório do projeto.  
- Exibição final da **História Final (HF)**.

---

## 📋 Exemplo de Execução

**Entrada:**

r1(x) w2(x) r2(y) w1(y) c1 c2

**Saída Final:**

História Final (HF)
r1(x)
r2(y)
w1(y)
c1
c2


## Não Implementado
- Não está em banco de dados real.
- Reexecuções múltiplas são simuladas, não paralelas.

---

## Saída Gerada
O arquivo txt contém o log completo de cada simulação.

---

## Conclusão
O sistema implementa corretamente o protocolo de *timestamps*, simulando o comportamento do escalonamento de transações em ambientes concorrentes e garantindo consistência dos dados.