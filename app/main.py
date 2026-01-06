import sys


def main():
    # TODO: Uncomment the code below to pass the first stage
    sys.stdout.write("$ ")
    sys.stdout.flush()
    user_input = sys.stdin.readline().strip()
    print(f"{user_input}: command not found")
    pass


if __name__ == "__main__":
    main()
