import os
import sys
import traceback
import subprocess
import shlex

def evaluateCommand(command: str, params=None):
    if params is None:
        params = []

    if not command: 
        return
    
    BUILTINS = ('echo', 'type', 'exit', 'pwd', 'cd')

    def checkValid(cmd) -> bool:
        return cmd in BUILTINS
    
    # Valid Commands

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
            pathAllStr = os.environ['PATH']
            pathDir = pathAllStr.split(os.pathsep)
            found = False
            for p in pathDir:
                createdPath = os.path.join(p, cmd)
                if os.path.isfile(createdPath) and os.access(createdPath, os.X_OK):
                    print(f"{cmd} is {createdPath}")
                    found = True
                    break  
            if not found:
                print(f"{cmd}: not found")

    def executeCommand(cmd, *args):
        pathAllStr = os.environ['PATH']
        pathDir = pathAllStr.split(os.pathsep)
        found = False
        for p in pathDir:
            createdPath = os.path.join(p, cmd)
            if os.path.isfile(createdPath) and os.access(createdPath, os.X_OK):
                process = subprocess.Popen(
                args=[cmd, *args],      
                executable=createdPath,
                stdin=None,
                stdout=None,
                stderr=None
            )
                process.wait()
                found = True
                break  
        if not found:
            commandNotFound(cmd)

    def pwdCommand():
        currentDir = os.getcwd()
        print(currentDir)

    def cdCommand(params):
        if len(params) == 0:
            print("cd: missing path")
            return

        if len(params) > 1:
            print("cd: too many arguments")
            return

        path = params[0]

        try:
            os.chdir(path)

        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")

        except NotADirectoryError:
            print(f"cd: {path}: Not a directory")

        except PermissionError:
            print(f"cd: {path}: Permission denied")

        except OSError as e:
            print(f"cd: {path}: {e.strerror}")

    # Handlers

    def handleMissingArgs(cmd, minArgs, maxArgs):
        if minArgs == maxArgs:
            print(f"{cmd} takes exactly {maxArgs} argument(s)")
        else:
            print(f"{cmd} takes {minArgs} to {maxArgs} arguments")


    match command:
        case "exit":
            exitCommand()
        case "echo":
            if len(params) > 0:
                echoCommand(' '.join(params))
            else:
                echoCommand()
        case "type":
            if len(params) == 1:
                typeCommand(params[0])
            else:
                handleMissingArgs(command, 1, 1)
        case "pwd":
            pwdCommand()
        case "cd":
            cdCommand(params)
        case _:
            executeCommand(command, *params)

def classifyCommandAndData(clientInput: str):
    inputAsList = shlex.split(clientInput)

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
            sys.exit(0)

        except SystemExit:
            raise

        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()