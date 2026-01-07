import sys
import traceback

def evaluateCommand(command: str, params=None):
    if params is None:
        params = []

    if not command: 
        return
    
    BUILTINS = ('echo', 'type', 'exit')

    def checkValid(cmd) -> bool:
        return cmd in BUILTINS

    def exitCommand():
        sys.exit(0)

    def commandNotFound(cmd):
        print(f"{cmd}: command not found")

    def echoCommand(msg=''):
        print(msg)

    def typeCommand(cmd):
        if checkValid(cmd):
            print(f'{cmd} is a shell builtin')
        else:
            print(f'{cmd}: not found')

    def handleMissingArgs(cmd, minArgs, maxArgs):
        if minArgs == maxArgs:
            print(f"{cmd} takes exactly {maxArgs} argument(s)")
        else:
            print(f"{cmd} takes {minArgs} to {maxArgs} arguments")



    commandDict = {
        "exit": exitCommand,
        "echo": echoCommand,
        "type": typeCommand,
        "commandNotFound": commandNotFound
    }

    if checkValid(command):
        action = commandDict[command]
        match command:
            case "exit":
                action()
            case "echo":
                if len(params) > 0:
                    action(' '.join(params))
                else:
                    action()
            case "type":
                if len(params) == 1:
                    action(params[0])
                else:
                    handleMissingArgs(command, 1, 1)

            case _:
                action(command)


    else:
        commandDict["commandNotFound"](command)

def classifyCommandAndData(clientInput: str):
    inputAsList = clientInput.split()

    if len(inputAsList) < 1:
        return

    command, *arguments = inputAsList

    evaluateCommand(command, arguments)
    


def main():
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()
            classifyCommandAndData(user_input)

        except KeyboardInterrupt:
            print()
            continue

        except SystemExit:
            raise

        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()
