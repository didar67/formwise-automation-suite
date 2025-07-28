# Entry Point
from core.cli import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Execution interrupted by user.")
    except Exception as e:
        print(f"Error: {e}")
