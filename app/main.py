import os
import sys
import traceback
import subprocess
import shlex


def evaluateCommand(command: str, params=None, stdout_file=None, stderr_file=None, stdout_flag=None):

    if params is None:
        params = []

    if not command:
        return

    # --- prepare stderr redirection (must happen BEFORE execution) ---
    stderr_handle = None
    if stderr_file:
        try:
            stderr_handle = open(stderr_file, 'w')
        except FileNotFoundError:
            print(f"{stderr_file}: No such file or directory", file=sys.stderr)
            return

    BUILTINS = ('echo', 'type', 'exit', 'pwd', 'cd')

    def open_stdout_file(flag: str):
        try:
            return open(stdout_file, flag)
        except FileNotFoundError:
            print(f"{stdout_file}: No such file or directory", file=sys.stderr)
            return None

    # ---------------- builtins ----------------

    def exitCommand():
        if stderr_handle:
            stderr_handle.close()
        sys.exit(0)

    def commandNotFound(cmd):
        print(f"{cmd}: command not found", file=stderr_handle or sys.stderr)

    def echoCommand(msg=''):
        if stdout_file:
            f = open_stdout_file(stdout_flag)
            if not f:
                return
            print(msg, file=f)
            f.close()
        else:
            print(msg)

    def typeCommand(cmd):
    output = None
    is_error = False

    if cmd in BUILTINS:
        output = f"{cmd} is a shell builtin"
    else:
        for p in os.environ['PATH'].split(os.pathsep):
            full = os.path.join(p, cmd)
            if os.path.isfile(full) and os.access(full, os.X_OK):
                output = f"{cmd} is {full}"
                break
        else:
            output = f"{cmd}: not found"
            is_error = True

    if is_error:
        print(output, file=stderr_handle or sys.stderr)
        return

    if stdout_file:
        f = open_stdout_file(stdout_flag)
        if not f:
            return
        print(output, file=f)
        f.close()
    else:
        print(output)


    def pwdCommand():
        output = os.getcwd()
        if stdout_file:
            f = open_stdout_file(stdout_flag)
            if not f:
                return
            print(output, file=f)
            f.close()
        else:
            print(output)

    def cdCommand(params):
        if len(params) == 0:
            print("cd: missing path", file=stderr_handle or sys.stderr)
            return
        if len(params) > 1:
            print("cd: too many arguments", file=stderr_handle or sys.stderr)
            return

        try:
            os.chdir(os.path.expanduser(params[0]))
        except FileNotFoundError:
            print(f"cd: {params[0]}: No such file or directory", file=stderr_handle or sys.stderr)
        except NotADirectoryError:
            print(f"cd: {params[0]}: Not a directory", file=stderr_handle or sys.stderr)
        except PermissionError:
            print(f"cd: {params[0]}: Permission denied", file=stderr_handle or sys.stderr)

    # ---------------- external commands ----------------

    def executeCommand(cmd, *args):
        for p in os.environ['PATH'].split(os.pathsep):
            full = os.path.join(p, cmd)
            if os.path.isfile(full) and os.access(full, os.X_OK):
                out = None
                if stdout_file:
                    out = open_stdout_file(stdout_flag)
                    if not out:
                        return

                process = subprocess.Popen(
                    [cmd, *args],
                    executable=full,
                    stdout=out if out else None,
                    stderr=stderr_handle if stderr_handle else sys.stderr
                )
                process.wait()

                if out:
                    out.close()
                return

        commandNotFound(cmd)

    # ---------------- dispatcher ----------------

    match command:
        case "exit":
            exitCommand()
        case "echo":
            echoCommand(' '.join(params))
        case "type":
            if len(params) == 1:
                typeCommand(params[0])
            else:
                print("type takes exactly 1 argument", file=stderr_handle or sys.stderr)
        case "pwd":
            pwdCommand()
        case "cd":
            cdCommand(params)
        case _:
            executeCommand(command, *params)

    if stderr_handle:
        stderr_handle.close()


def classifyCommandAndData(clientInput: str):
    if not clientInput.strip():
        return

    tokens = shlex.split(clientInput)
    if not tokens:
        return

    stdout_file = None
    stderr_file = None
    stdout_flag = None

    # IMPORTANT: most specific first
    if '>>' in tokens:
        idx = tokens.index('>>')
        stdout_file = tokens[idx + 1]
        tokens = tokens[:idx]
        stdout_flag = 'a'

    if '2>' in tokens:
        idx = tokens.index('2>')
        stderr_file = tokens[idx + 1]
        tokens = tokens[:idx]

    if '1>' in tokens:
        idx = tokens.index('1>')
        stdout_file = tokens[idx + 1]
        tokens = tokens[:idx]
        stdout_flag = 'w'

    elif '>' in tokens:
        idx = tokens.index('>')
        stdout_file = tokens[idx + 1]
        tokens = tokens[:idx]
        stdout_flag = 'w'

    command = tokens[0]
    arguments = tokens[1:]

    evaluateCommand(command, arguments, stdout_file=stdout_file, stderr_file=stderr_file, stdout_flag=stdout_flag)


def main():
    while True:
        try:
            sys.stdout.write("$ ")
            sys.stdout.flush()
            line = sys.stdin.readline()
            if not line:
                break
            classifyCommandAndData(line.strip())
        except KeyboardInterrupt:
            sys.exit(0)
        except SystemExit:
            raise
        except Exception:
            traceback.print_exc()


if __name__ == "__main__":
    main()
