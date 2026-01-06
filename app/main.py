import sys


def main():
    try:
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()
            print(f"{user_input}: command not found")
    
    except KeyboardInterrupt:
        print("\nExiting shell.")
        sys.exit(0)


if __name__ == "__main__":
    main()
