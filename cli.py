#!/usr/bin/env python3
import argparse
import sys
from src.calculator.calculator import Calculator
from src.git_operations.git_utils import GitOperations

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='CLI tool for calculator and git operations')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Calculator commands
    calc_parser = subparsers.add_parser('calc', help='Calculator operations')
    calc_parser.add_argument('operation', choices=['add', 'subtract', 'multiply', 'divide'],
                           help='Mathematical operation to perform')
    calc_parser.add_argument('x', type=float, help='First number')
    calc_parser.add_argument('y', type=float, help='Second number')

    # Git commands
    git_parser = subparsers.add_parser('git', help='Git operations')
    git_parser.add_argument('operation', choices=['add', 'commit', 'delete'],
                          help='Git operation to perform')
    git_parser.add_argument('--files', nargs='+', help='Files to operate on')
    git_parser.add_argument('--message', '-m', help='Commit message')
    git_parser.add_argument('--auto-commit', action='store_true',
                          help='Automatically commit after delete')

    return parser

def handle_calculator(args):
    calc = Calculator()
    try:
        result = None
        if args.operation == 'add':
            result = calc.add(args.x, args.y)
        elif args.operation == 'subtract':
            result = calc.subtract(args.x, args.y)
        elif args.operation == 'multiply':
            result = calc.multiply(args.x, args.y)
        elif args.operation == 'divide':
            result = calc.divide(args.x, args.y)
        
        print(f"Result: {result}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def handle_git(args):
    git = GitOperations()
    try:
        if args.operation == 'add':
            if not args.files:
                print("Error: --files argument is required for git add", file=sys.stderr)
                return 1
            success, message = git.add_files(args.files)
        elif args.operation == 'commit':
            if not args.message:
                print("Error: --message argument is required for git commit", file=sys.stderr)
                return 1
            success, message = git.commit(args.message)
        elif args.operation == 'delete':
            if not args.files or len(args.files) != 1:
                print("Error: exactly one file must be specified for delete", file=sys.stderr)
                return 1
            success, message = git.delete_file(args.files[0], args.auto_commit)

        print(message)
        return 0 if success else 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

def main():
    parser = setup_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'calc':
        return handle_calculator(args)
    elif args.command == 'git':
        return handle_git(args)

if __name__ == '__main__':
    sys.exit(main()) 