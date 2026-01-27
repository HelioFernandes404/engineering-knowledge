class Calculator:
    def __init__(self) -> None:
        self.history = []
        self.result = 0

    def add(self, num: int) -> None:
        self.history.append(f"Added {num}")
        self.result += num
