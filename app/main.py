import sys

def evaluateCommand(command: str):

    def exitCommand():
        print("Exiting shell.")
        sys.exit(0)

    def commandNotFound(cmd):
        print(f"{cmd}: command not found")

    commandDict = {
        "exit": exitCommand,
    }

    if not command: 
        return

    if command not in commandDict:
        commandNotFound(command)
        return

    commandDict[command]()

def main():
    try:
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()
            evaluateCommand(user_input)

    except KeyboardInterrupt:
        print("\nExiting shell.")
        sys.exit(0)

if __name__ == "__main__":
    main()
