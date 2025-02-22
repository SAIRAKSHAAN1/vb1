from src.calculator.calculator import Calculator
from src.git_operations.git_utils import GitOperations

def test_calculator():
    print("\n=== Testing Calculator Operations ===")
    calc = Calculator()
    
    # Test addition
    result = calc.add(10, 5)
    print(f"Addition: 10 + 5 = {result}")
    
    # Test subtraction
    result = calc.subtract(20, 8)
    print(f"Subtraction: 20 - 8 = {result}")
    
    # Test multiplication
    result = calc.multiply(6, 7)
    print(f"Multiplication: 6 * 7 = {result}")
    
    # Test division
    result = calc.divide(100, 4)
    print(f"Division: 100 / 4 = {result}")
    
    # Test division by zero error handling
    try:
        calc.divide(10, 0)
    except ValueError as e:
        print(f"Division by zero error caught: {e}")

def test_git_operations():
    print("\n=== Testing Git Operations ===")
    git = GitOperations()
    
    # Test adding files
    success, message = git.add_files(["test_example.py"])
    print(f"Add files result: {message}")
    
    # Test commit
    success, message = git.commit("Test commit message")
    print(f"Commit result: {message}")

if __name__ == "__main__":
    print("Starting tests...")
    test_calculator()
    test_git_operations()
    print("\nTests completed!") 