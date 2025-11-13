# src/utils.py
def parse_history_input(input_str):
    """
    Recebe algo como:
    r1(x) w2(x) r2(y) w1(y) c1 c2
    Retorna uma lista ['r1(x)', 'w2(x)', 'r2(y)', 'w1(y)', 'c1', 'c2']
    """
    return input_str.replace(",", " ").split()
