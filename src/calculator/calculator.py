class Calculator:
    @staticmethod
    def add(x: float, y: float) -> float:
        """Add two numbers."""
        return x + y

    @staticmethod
    def subtract(x: float, y: float) -> float:
        """Subtract y from x."""
        return x - y

    @staticmethod
    def multiply(x: float, y: float) -> float:
        """Multiply two numbers."""
        return x * y

    @staticmethod
    def divide(x: float, y: float) -> float:
        """Divide x by y."""
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y 