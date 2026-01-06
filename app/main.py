import sys
def evaluateCommand(command: str):

    def exitCommand():
        sys.exit(0)

    def commandNotFound(cmd):
        print(f"{cmd}: command not found")

    def echoCommand(msg=''):
        print(*msg)

    commandDict = {
        "exit": exitCommand,
        "echo": echoCommand,
        "invalidCommand": commandNotFound
    }

    if not command: 
        return

    return commandDict[command]

def classifyCommandAndData(clientInput: str):
    inputAsList = clientInput.split()
    validCommands = ('exit', 'echo')

    if len(inputAsList) < 1:
        return

    command, *arguments = inputAsList
    
    if command in validCommands:
        if arguments:
            evaluateCommand(command)(arguments)
            return
        else:
            evaluateCommand(command)()
            return
    
    else:
        evaluateCommand("invalidCommand")(command)
    


def main():
    try:
        while True:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()
            classifyCommandAndData(user_input)

    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()
