# CLI Tool with Calculator and Git Operations

A command-line tool that provides basic calculator functionality and Git operations, with Docker support.

## Features

- Basic Calculator Operations
  - Addition
  - Subtraction
  - Multiplication
  - Division

- Git Operations
  - Add files to staging
  - Commit changes
  - Delete files

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Make the CLI script executable:
```bash
chmod +x cli.py  # On Unix-like systems
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t cli-tool .
```

## Usage

### Calculator Operations

```bash
# Addition
./cli.py calc add 5 3

# Subtraction
./cli.py calc subtract 10 4

# Multiplication
./cli.py calc multiply 6 7

# Division
./cli.py calc divide 15 3
```

### Git Operations

```bash
# Add files to staging
./cli.py git add --files file1.txt file2.txt

# Commit changes
./cli.py git commit --message "Your commit message"

# Delete a file
./cli.py git delete --files file1.txt
./cli.py git delete --files file1.txt --auto-commit  # With automatic commit
```

### Using with Docker

```bash
# Calculator operations
docker run cli-tool calc add 5 3

# Git operations
docker run -v $(pwd):/app cli-tool git add --files file1.txt
```

## Project Structure

```
project-root/
│── src/
│   ├── calculator/
│   │   ├── calculator.py  # Calculator logic
│   ├── git_operations/
│   │   ├── git_utils.py  # Git utilities
│── cli.py  # Command-line interface
│── Dockerfile  # Docker setup
│── requirements.txt  # Python dependencies
│── README.md  # Project documentation
│── .gitignore  # Git ignore rules
```

## Error Handling

The tool includes comprehensive error handling for:
- Invalid calculator operations (e.g., division by zero)
- Missing or invalid Git command arguments
- File system errors
- Git operation failures

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 