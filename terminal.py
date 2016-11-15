import subprocess
import shlex
from nbstreamreader import NonBlockingStreamReader as NBSR

class Terminal():

    def __init__(self):
        self.term_started = False
        self.proc = None
        self.nbsr = None

    def start_terminal(self):
        self.proc = subprocess.Popen(["/bin/sh"], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.nbsr = NBSR(self.proc.stdout)
        self.term_started = True


    def execute_command(self, input_cmd):
        out_out = []

        #Format the command
        args_list = shlex.split(input_cmd)
        args_str = " ".join(i for i in args_list)
        args_str += "\n"

        if args_str == "exit\n":
            print("EXITING TERMINAL")
            self.term_started = False
            self.proc.terminate()
            return "Left Terminal mode"

        #Write the command
        self.proc.stdin.write(args_str)

        #Parse output
        while True:
            out = self.nbsr.readline(0.1)
            if not out:
                break
            out_out.append(out)

        print out_out

        #Format output
        response = "".join(i for i in out_out)

        return response
