import wx
import socket
import threading
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


        app = App()

        server = AdvantageServer(server_ip, server_port, app.frame)
        server.start()

        app.MainLoop()

        self.root.destroy()

    def run(self):
        self.root.mainloop()

class OverlayFrame(wx.Frame):
    def __init__(self):
        super(OverlayFrame, self).__init__(None, style=wx.FRAME_NO_TASKBAR | wx.STAY_ON_TOP)
        self.panel = wx.Panel(self, size=(50, 1000))
        self.advantage_level = 50
        self.fill_color = wx.Colour(255, 255, 255)  # Default fill color (black)
        self.bg_color = wx.Colour(0, 0, 0)  # Default background color (white)
        self.panel.Bind(wx.EVT_PAINT, self.on_paint)
        self.position_overlay()

    def position_overlay(self):
        screen_width, screen_height = wx.GetDisplaySize()
        overlay_width, overlay_height = 50, 1000
        x = 0
        y = (screen_height - overlay_height) // 2
        self.SetPosition((x, y))
        self.SetSize((overlay_width, overlay_height))

    def set_advantage_level(self, level):
        self.advantage_level = level
        self.panel.Refresh()

    def set_fill_color(self, color):
        self.fill_color = color
        self.panel.Refresh()

    def set_bg_color(self, color):
        self.bg_color = color
        self.panel.Refresh()

    def on_paint(self, event):
        dc = wx.PaintDC(self.panel)
        dc.Clear()
        
        # Draw background
        dc.SetBrush(wx.Brush(self.bg_color))
        dc.DrawRectangle(0, 0, self.panel.GetSize().GetWidth(), self.panel.GetSize().GetHeight())
        
        # Draw fill
        bar_height = self.advantage_level * self.panel.GetSize().GetHeight() / 100
        dc.SetBrush(wx.Brush(self.fill_color))
        dc.DrawRectangle(0, int(self.panel.GetSize().GetHeight() - bar_height), int(self.panel.GetSize().GetWidth()), bar_height)


class AdvantageServer:
    def __init__(self, host, port, overlay_frame):
        self.overlay_frame = overlay_frame
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(host, port)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.client_socket = None
        self.advantage_level = 50  # Initial advantage level

    def start(self):
        print("Server is listening for connections...")
        self.client_socket, _ = self.server_socket.accept()
        print("Connection established.")

        self.update_thread = threading.Thread(target=self.update_advantage_loop)
        self.update_thread.start()

    def update_advantage(self, new_level):
        self.advantage_level = new_level
        self.overlay_frame.set_advantage_level(self.advantage_level)
        # Update GUI or visual representation of the advantage level

    def update_advantage_loop(self):
        while True:
            data = self.client_socket.recv(1024).decode()
            if not data:
                break
            new_level = int(data)
            self.update_advantage(new_level)

        print("Client disconnected.")
        self.client_socket.close()

class App(wx.App):
    def OnInit(self):
        self.frame = OverlayFrame()
        self.frame.Show(True)
        return True

# Run the server UI
server_ui = ServerUI()
server_ui.run()

# app = App()
# overlay_server = AdvantageServer('0.0.0.0', 12345, app.frame)  # Replace with appropriate IP and port
# overlay_server.start()

# app.MainLoop()
