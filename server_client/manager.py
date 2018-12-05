import os, threading

from time import sleep

server = "python server.py"
client = "python client.py"
multi_server = "python multi_server.py"
multi_client = "python multi_client.py"


class run_cmd(threading.Thread):
    def __init__(self,command):
        threading.Thread.__init__(self)
        self.command = command


    def run(self):
        print(f" running {self.command.split(' ')[1]} ......")
        os.system(self.command)
        print(f"exiting thread {self.command.split(' ')[1]} ......")


if __name__ == '__main__':
    while 1:
        toggle = input("type S for single server &  M for multi server .....    ")
        if toggle.upper() =='S':
            server_thread  = run_cmd(server)
            client_thread = run_cmd(client)

            server_thread.start()
            sleep(1)
            client_thread.start()
            break
        if toggle.upper() =='M':
            server_thread = run_cmd(multi_server)
            client_thread = run_cmd(multi_client)

            server_thread.start()
            sleep(1)
            client_thread.start()
            break