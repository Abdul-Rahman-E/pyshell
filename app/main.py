import os
import sys
import traceback
import subprocess
import shlex

def evaluateCommand(command: str, params=None, stdout_file=None):
    if params is None:
        params = []

    if not command: 
        return
    
    BUILTINS = ('echo', 'type', 'exit', 'pwd', 'cd')

    def checkValid(cmd) -> bool:
        return cmd in BUILTINS
    
    def open_stdout_file():
        try:
            return open(stdout_file, 'w')
        except FileNotFoundError:
            print(f"{stdout_file}: No such file or directory", file=sys.stderr)
            return None

    
    # Valid Commands

    def exitCommand():
        sys.exit(0)

    def commandNotFound(cmd):
        print(f"{cmd}: command not found")

    def echoCommand(msg=''):
        if stdout_file:
            f = open_stdout_file()
            if not f:
                return
            print(msg, file=f)
            f.close()
        else:
            print(msg)


    def typeCommand(cmd):
        output = ""
        if checkValid(cmd):
            output = f'{cmd} is a shell builtin'
        else:
            found = False
            for p in os.environ['PATH'].split(os.pathsep):
                createdPath = os.path.join(p, cmd)
                if os.path.isfile(createdPath) and os.access(createdPath, os.X_OK):
                    output = f"{cmd} is {createdPath}"
                    found = True
                    break
            if not found:
                output = f"{cmd}: not found"

        if stdout_file:
            f = open_stdout_file()
            if not f:
                return
            print(output, file=f)
            f.close()
        else:
            print(output)


    def executeCommand(cmd, *args):
        for p in os.environ['PATH'].split(os.pathsep):
            createdPath = os.path.join(p, cmd)
            if os.path.isfile(createdPath) and os.access(createdPath, os.X_OK):
                f = None
                if stdout_file:
                    f = open_stdout_file()
                    if not f:
                        return

                process = subprocess.Popen(
                    [cmd, *args],
                    executable=createdPath,
                    stdout=f if f else None,
                    stderr=sys.stderr
                )
                process.wait()

                if f:
                    f.close()
                return

        commandNotFound(cmd)


    def pwdCommand():
        output = os.getcwd()
        if stdout_file:
            f = open_stdout_file()
            if not f:
                return
            print(output, file=f)
            f.close()
        else:
            print(output)


    def cdCommand(params):
        if len(params) == 0:
            print("cd: missing path")
            return

        if len(params) > 1:
            print("cd: too many arguments")
            return

        path = os.path.expanduser(params[0])

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
    if not clientInput.strip():
        return
    
    inputAsList = shlex.split(clientInput)

    if not inputAsList:
        return
    
    stdout_file = None

    if '>' in inputAsList:
        idx = inputAsList.index('>')
        command = inputAsList[0]
        arguments = inputAsList[1:idx]
        if idx+1 < len(inputAsList):
            stdout_file = inputAsList[idx+1]
        else:
            print("Syntax error: no file specified for redirection")
            return
    elif '1>' in inputAsList:
        idx = inputAsList.index('1>')
        command = inputAsList[0]
        arguments = inputAsList[1:idx]
        if idx + 1 < len(inputAsList):
            stdout_file = inputAsList[idx + 1]
        else:
            print("Syntax error: no file specified for redirection")
            return
    else:
        command = inputAsList[0]
        arguments = inputAsList[1:]

    evaluateCommand(command, arguments, stdout_file=stdout_file)
    
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