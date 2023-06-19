from tkinter import *
import threading
import time


class StopAndWait:
    def __init__(self, master):
        self.master = master
        self.master.title("Stop and Wait Protocol")
        self.master.geometry("1620x1080")
        self.master.resizable(False, False)
        self.master.config(bg="#F6F6F6")
        self.frames_to_send = []
        self.frames_received = []

        self.timeout_duration = 1  # Default timeout duration (in seconds)

        self.btn_increase_timeout = Button(
            self.master,
            text="Increase Timeout",
            font=("Helvetica", 12),
         bg="#333",
            fg="#FFF",
            command=self.increase_timeout,
        )
        self.btn_increase_timeout.pack(side=LEFT, padx=10)

        self.lbl_sender = Label(
            self.master, text="Sender", font=("Helvetica", 16), fg="#333", bg="#F6F6F6"
        )
        self.lbl_sender.pack(side=LEFT, pady=20)

        self.frames_sender = Listbox(
            self.master, font=("Helvetica", 12), bg="#FFF", fg="#333", height=10
        )
        self.frames_sender.pack(side=LEFT, padx=20, pady=10)

        self.lbl_receiver = Label(
            self.master, text="Receiver", font=("Helvetica", 16), fg="#333", bg="#F6F6F6"
        )
        self.lbl_receiver.pack(side=RIGHT, pady=20)

        self.frames_receiver = Listbox(
            self.master, font=("Helvetica", 12), bg="#FFF", fg="#333", height=10
        )
        self.frames_receiver.pack(side=RIGHT, padx=20, pady=10)

        self.btn_send_packet = Button(
            self.master,
            text="Send Packet",
            font=("Helvetica", 14),
            bg="#4CAF50",
            fg="#FFF",
            command=self.send_packet,
        )
        self.btn_send_packet.pack(pady=20)

        self.lbl_received = Label(
            self.master, text="Received Packets:", font=("Helvetica", 14), fg="#333", bg="#F6F6F6"
        )
        self.lbl_received.pack(side=TOP, pady=10)

        self.lbl_packets = Label(
            self.master, text="", font=("Helvetica", 12), fg="#333", bg="#F6F6F6"
        )
        self.lbl_packets.pack(pady=10)

        self.timer_label = Label(
            self.master, text="", font=("Helvetica", 12), fg="#333", bg="#F6F6F6"
        )
        self.timer_label.pack(pady=10)

        self.timer = None

        self.master.mainloop()

    def increase_timeout(self):
        self.timeout_duration += 1
        self.lbl_packets.config(text=f"Timeout Duration: {self.timeout_duration} seconds")

    def start_timer(self):
        self.timer_start = time.time()
        self.update_timer()

    def update_timer(self):
        elapsed_time = time.time() - self.timer_start
        self.timer_label.config(text=f"Timer: {int(elapsed_time)} seconds")
        if elapsed_time >= self.timeout_duration:
            self.resend_frame()
        else:
            self.master.after(1000, self.update_timer)

    def stop_timer(self):
        self.timer_label.config(text="")

    def send_packet(self):
        if not self.frames_to_send:
            self.frames_to_send = [f"Frame {i + 1}" for i in range(10)]
            self.frames_sender.delete(0, END)
            for frame in self.frames_to_send:
                self.frames_sender.insert(END, frame)

        if self.frames_to_send:
            frame = self.frames_to_send.pop(0)
            self.frames_sender.delete(0)
            self.lbl_sender.config(text=f"Sender: Sending {frame}")
            self.start_timer()
            self.master.after(1000, self.simulate_packet_transmission, frame)

    def simulate_packet_transmission(self, frame):
        self.master.after(1000, self.receive_packet, frame)

    def receive_packet(self, frame):
        self.stop_timer()
        self.lbl_sender.config(text="Sender: Waiting for ACK...")

        elapsed_time = time.time() - self.timer_start
        if elapsed_time < self.timeout_duration:
            if frame not in self.frames_received:  # Check if frame is already received
                self.frames_received.append(frame)
                self.frames_receiver.insert(END, f"Received {frame}")
                self.lbl_received.config(text=f"Received {frame}")
            self.lbl_sender.config(text="Sender: ACK received")

            if self.frames_to_send:
                next_frame = self.frames_to_send.pop(0)
                self.frames_sender.delete(0)
                self.lbl_sender.config(text=f"Sender: Sending {next_frame}")
                self.start_timer()
                self.master.after(1000, self.simulate_packet_transmission, next_frame)
        else:
            self.lbl_sender.config(text="Sender: ACK not received, resending frame...")
            self.frames_to_send.insert(0, frame)
            self.start_timer()
            self.master.after(1000, self.simulate_packet_transmission, frame)
        if len(self.frames_received) == 10:
            self.master.after(1000,exit)


    def resend_frame(self):
        self.lbl_sender.config(text="Sender: Resending frame...")
        frame = self.frames_received[-1]
        self.frames_receiver.delete(END)
        self.frames_sender.insert(0, frame)
        self.start_timer()
        self.master.after(1000, self.simulate_packet_transmission, frame)
    
if __name__ == "__main__":
    root = Tk()
    app = StopAndWait(root)

