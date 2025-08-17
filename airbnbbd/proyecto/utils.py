from datetime import datetime, date

def input_date(prompt: str) -> date:
    while True:
        s = input(prompt + " (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(s, "%Y-%m-%d").date()
        except ValueError:
            print("Formato inválido. Ejemplo: 2025-08-20")
