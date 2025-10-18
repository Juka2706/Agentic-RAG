class Budget:
    def __init__(self, tokens: int):
        self.tokens = tokens
        self.used = 0
    def allow(self, n: int) -> bool:
        if self.used + n > self.tokens:
            return False
        self.used += n
        return True
