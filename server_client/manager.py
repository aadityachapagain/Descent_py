import os, threading

from time import sleep

server = "python server.py"
client = "python client.py"

class run_cmd(threading.Thread):
    def __init__(self,command):
        threading.Thread.__init__(self)
        self.command = command


    def run(self):
        print(f" running {self.command.split(' ')[1]} ......")
        os.system(self.command)
        print(f"exiting thread {self.command.split(' ')[1]} ......")


if __name__ == '__main__':
    server_thread  = run_cmd(server)
    client_thread = run_cmd(client)

    server_thread.start()
    sleep(1)
    client_thread.start()