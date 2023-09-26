import socket
import tkinter as tk

class ServerUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Server Configuration")

        self.ip_label = tk.Label(self.root, text="Server IP:")
        self.ip_label.pack()

        self.ip_entry = tk.Entry(self.root)
        self.ip_entry.pack()

        self.port_label = tk.Label(self.root, text="Server Port:")
        self.port_label.pack()

        self.port_entry = tk.Entry(self.root)
        self.port_entry.pack()

        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server)
        self.start_button.pack()

    def start_server(self):
        server_ip = self.ip_entry.get()
        server_port = int(self.port_entry.get())


        client = AdvantageClient(server_ip, server_port)
        client.start()

        self.root.destroy()

    def run(self):
        self.root.mainloop()

class AdvantageClient:
    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.root = tk.Tk()
        self.advantage_slider = tk.Scale(self.root, from_=0, to=100, orient='horizontal', length=300)

        self.advantage_slider.pack()

        self.advantage_slider.bind("<Motion>", self.update_slider)

    def update_advantage(self):
        advantage_level = self.advantage_slider.get()
        self.client_socket.send(str(advantage_level).encode())

    def update_slider(self, event):
        advantage_level = self.advantage_slider.get()
        self.client_socket.send(str(advantage_level).encode())

    def start(self):
        self.root.mainloop()
        self.client_socket.close()

server_ui = ServerUI()
server_ui.run()

