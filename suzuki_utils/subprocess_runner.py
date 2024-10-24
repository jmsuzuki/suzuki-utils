import os
import subprocess


class SubprocessRunner(object):
    def run_command(self, command: list, working_directory: str = None, raise_errors: bool = True, suppress_output: bool = False) -> str:
        """
        Runs the given command on the command line

        :param command: the command to run
        :param working_directory: the directory to run the command in
        :param raise_errors: raise errors?
        :param suppress_output: suppress output?
        """
        if not suppress_output:
            print(f'Running Command: {" ".join(command)}')

        if not working_directory:
            working_directory = os.getcwd()

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=working_directory
        )

        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8').strip()
        if not suppress_output:
            print(output)
            print(f"Command Return Code: {process.returncode}, raise_errors={raise_errors}")
            print("---")

        if raise_errors:
            if not suppress_output:
                print("Raise Errors was true.")
            if process.returncode != 0:
                if not suppress_output:
                    print("The process return code is not equal to 0.")

                if suppress_output:
                    print(f'Command: {" ".join(command)}')
                    print(output)

                if not suppress_output:
                    print(f"raising ValueError: Process returned: {process.returncode}")

                raise ValueError(f"Process returned: {process.returncode}")

        return output


