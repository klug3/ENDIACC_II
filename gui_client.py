import tkinter as tk
from tkinter.constants import TRUE
from tkinter import messagebox
from PIL import ImageTk, Image
from resizeimage import resizeimage
from functions import (
    receive,
    write,
    run,
    natural_sort,
    send_command,
    validate_entered_values,
)
import threading
import glob
import time


class MyGUI:

    # Enable picture buttons
    picture_buttons_avaliable = True  # Change to False to disable buttons

    # Class variables:
    picture_count = 0
    picture_list = []
    # Experiment related variables
    experiment_in_progress = False
    sending_blocked = False

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("ENDIACC II")
        self.root.resizable(False, False)

        self.ico = Image.open("icon.png")
        self.photo = ImageTk.PhotoImage(self.ico)
        self.root.wm_iconphoto(True, self.photo)

        self.frame1 = tk.Frame(self.root)
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.columnconfigure(1, weight=1)
        self.frame1.columnconfigure(2, weight=1)

        # SERVER IP
        self.label_ip = tk.Label(
            self.frame1, text="Server IP:", font=("Helvetica", 12, "bold"), anchor="e"
        )
        self.label_ip.grid(row=0, column=0, sticky="we")
        self.entry_ip = tk.Entry(self.frame1, width=40, font=("Helvetica", 12), bd=2)
        self.entry_ip.grid(row=0, column=1, sticky="we")

        # SERVER PORT
        self.label_port = tk.Label(
            self.frame1, text="Port:", font=("Helvetica", 12, "bold"), anchor="e"
        )
        self.label_port.grid(row=1, column=0, sticky="we")
        self.entry_port = tk.Entry(self.frame1, font=("Helvetica", 12), bd=2)
        self.entry_port.grid(row=1, column=1, sticky="we")

        # NICK
        self.label_nick = tk.Label(
            self.frame1, text="Nickname:", font=("Helvetica", 12, "bold"), anchor="e"
        )
        self.label_nick.grid(row=2, column=0, sticky="we")
        self.entry_nick = tk.Entry(self.frame1, font=("Helvetica", 12), bd=2)
        self.entry_nick.grid(row=2, column=1, sticky="we")

        # CONNECT Button
        self.connect_butt = tk.Button(
            self.frame1,
            text="Connect",
            font=("Helvetica", 14, "bold"),
            bg="blue",
            fg="white",
            command=self.connect,
        )
        self.connect_butt.grid(row=0, column=2, rowspan=3, sticky="ns")

        ## SET DEFAULT VALUES FOR EACH ENTRY
        self.entry_ip.insert(0, "endiacc.projektstudencki.pl")
        self.entry_port.insert(0, "8282")
        # self.entry_nick.insert(0, "Pospolity Janusz")

        self.frame1.pack(fill="x")

        ###########################################
        ## DISPLAY IMAGES
        self.frame2 = tk.Frame(self.root)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.frame2.columnconfigure(2, weight=1)
        self.frame2.columnconfigure(3)  # For scrollbar

        # Find PATH to 1st picture
        self.picture_path = self.get_picture_list()[0]
        # Load and adjust image size
        self.img = self.adjust_image(
            root=self.root,
            picture_path=self.picture_path,
            target_width=450,
            target_heigh=460,
        )

        # Put img as a label
        self.label_picture = tk.Label(self.frame2, image=self.img)
        self.label_picture.grid(row=0, column=0, columnspan=2, sticky="we")

        #############################################################
        ## CHAT
        self.label_message = tk.Text(
            self.frame2,
            width=60,
            bd=5,
            state="disabled",
            height=30,
            wrap="word",
            font=("Helvetica", 12),
            relief="ridge",
        )  # size is in characters! not pixels!
        self.label_message.grid(row=0, column=2, rowspan=2, sticky="we")

        # Add tag to enable green bold entries (my nickname) in chat window
        self.label_message.tag_configure(
            "green_bold", foreground="green", font=("Helvetica", 12, "bold")
        )
        # Add tag to enable green entries (my messages) in chat window
        self.label_message.tag_configure(
            "green", foreground="green", font=("Helvetica", 12)
        )

        # Add tag to enable blue bold entries (other nickname) in chat window
        self.label_message.tag_configure(
            "blue_bold", foreground="blue", font=("Helvetica", 12, "bold")
        )
        # Add tag to enable blue entries (other messages) in chat window
        self.label_message.tag_configure(
            "blue", foreground="blue", font=("Helvetica", 12)
        )

        # Add tag to enable bold entries (wizard nickname) in chat window
        self.label_message.tag_configure(
            "red_bold", foreground="red", font=("Helvetica", 12, "bold")
        )
        # Add tag to enable red entries (wizard messages) in chat window
        self.label_message.tag_configure(
            "red", foreground="red", font=("Helvetica", 12)
        )

        # Add scroll bar to chat window
        self.scrollbar_chat = tk.Scrollbar(
            self.frame2, orient="vertical", command=self.label_message.yview
        )
        self.label_message.configure(yscrollcommand=self.scrollbar_chat.set)
        self.scrollbar_chat.grid(row=0, column=3, rowspan=2, sticky="ns")

        ## BUTTONS
        # Previous picture
        self.previous_butt = tk.Button(
            self.frame2,
            text="Previous",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.previous_pic,
        )
        self.previous_butt.grid(row=1, column=0, sticky="we")
        self.previous_butt.configure(state="disabled")

        # Next picture
        self.next_butt = tk.Button(
            self.frame2,
            text="Next",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.next_pic,
        )
        self.next_butt.grid(row=1, column=1, sticky="we")
        self.next_butt.configure(state="disabled")

        #############################################################
        ## WRITE BOX
        self.frame3 = tk.Frame(self.root)
        self.frame3.columnconfigure(0, weight=1)
        self.frame3.columnconfigure(1)  # For scrollbar

        self.label_write = tk.Text(
            self.frame3,
            width=50,
            bd=5,
            height=4,
            wrap="word",
            font=("Helvetica", 12),
            relief="ridge",
        )  # size is in characters! not pixels!

        self.label_write.grid(row=0, column=0, sticky="we")
        self.label_write.configure(state="normal")

        # Add scrollbar to writebox
        self.scrollbar_writebox = tk.Scrollbar(
            self.frame3, orient="vertical", command=self.label_write.yview
        )
        self.label_write.configure(yscrollcommand=self.scrollbar_writebox.set)
        self.scrollbar_writebox.grid(row=0, column=1, sticky="ns")

        ##############################################################
        ## SEND BUTTON
        self.frame4 = tk.Frame(self.root)
        self.frame4.columnconfigure(0, weight=1)
        self.frame4.columnconfigure(1, weight=1)
        self.frame4.columnconfigure(2, weight=1)

        self.send_butt = tk.Button(
            self.frame4,
            text="Send",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.send_msg,
        )
        self.send_butt.grid(row=0, column=2, sticky="we")
        self.send_butt.configure(state="normal")

        # Run key bindings function
        self.bindings()

        # Run get_picture_list function
        self.get_picture_list()

        self.root.mainloop()

    def bindings(self):
        self.label_write.bind("<Return>", lambda event: self.send_msg())
        self.label_write.bind("<Control-Return>", self.new_line)
        self.label_picture.bind(
            "<Button-1>", lambda event: self.start_canvas(self.picture_path)
        )
        self.label_picture.bind("<ButtonRelease-1>", self.close_canvas)

    def new_line(self, event):
        self.label_write.insert("end", "\n")
        return "break"

    def start_canvas(self, picture_path):
        # Create new TKinter instance for canvas window
        self.root2 = tk.Tk()
        self.root2.title("Picture")
        # Load picture and resize it if needed
        self.canvas_img = self.adjust_image(
            root=self.root2,
            picture_path=picture_path,
            target_width=1500,
            target_heigh=750,
        )
        # Create new canvas window
        self.picture_window = tk.Canvas(
            self.root2, width=self.canvas_img.width(), height=self.canvas_img.height()
        )
        # Load picture into canvas window
        self.picture_window.create_image(0, 0, anchor="nw", image=self.canvas_img)
        # Run canvas window
        self.picture_window.pack()

    def close_canvas(self, event):
        self.root2.destroy()

    def adjust_image(self, root, picture_path, target_width, target_heigh):
        img = Image.open(picture_path)
        # Get size of image object
        image = ImageTk.PhotoImage(master=root, image=img)
        original_width = image.width()  # get original img width
        original_heigh = image.height()  # get original img heigh

        # Resize img if needed
        if original_width > target_width:
            img = resizeimage.resize_width(img, target_width)
            # Get img heigh after resizing width, old one is obsolete
            image = ImageTk.PhotoImage(master=root, image=img)
            original_heigh = image.height()

        if original_heigh > target_heigh:
            img = resizeimage.resize_height(img, target_heigh)

        # Create new, final img object
        img = ImageTk.PhotoImage(master=root, image=img)
        return img

    def connect(self):
        # global server_ip, port, nick, client, listen
        # Validate entered values
        self.server_ip, self.port, self.nick, error_message = validate_entered_values(
            self.entry_ip.get(), self.entry_port.get(), self.entry_nick.get()
        )
        if error_message:
            messagebox.showerror("Error", error_message)
            return

        # Connect to ENDIACC II server
        try:
            self.client = run(server_ip=self.server_ip, port=self.port)
        except:
            messagebox.showerror("Error", "Cannot connect to the ENDIACC II server!")
            return

        # Show chat window, pictures and write box
        self.frame2.pack(fill="x")
        self.frame3.pack(fill="x")
        self.frame4.pack(fill="x")

        # Hide connection related labels
        self.frame1.destroy()

        # Hide previous/next picture buttons
        if not self.picture_buttons_avaliable:
            self.previous_butt.destroy()
            self.next_butt.destroy()

        receive_thread = threading.Thread(target=self.read_msg, daemon=TRUE)
        receive_thread.start()
        write_thread = threading.Thread(target=self.send_msg, daemon=TRUE)
        write_thread.start()

    def reconnect(self):
        while True:
            try:
                # Display information in chat window
                self.label_message.configure(state="normal")
                self.label_message.insert(
                    "end", ">>Connection lost!\nReconnecting in 1 sec.", "red"
                )
                self.label_message.insert("end", "\n")
                self.label_message.configure(state="disabled")
                self.label_message.see("end")  # scroll to the end
                # Try to reconnect
                self.client = run(server_ip=self.server_ip, port=self.port)
                # Exit loop when reconnected
                break
            except:
                # Wait 1 second and try again
                time.sleep(1)
                pass

    def get_picture_list(self):
        # Get paths to all pictures in ./pictures directory
        self.picture_list = glob.glob("./pictures/*.jpg")
        # Sort the list using natural sort
        natural_sort(self.picture_list)
        return self.picture_list

    def previous_pic(self):
        self.picture_count -= 1

        # Report picture change to other users using change picture command
        self.change_picture = "!COMMAND_PICTURE_COUNT" + str(self.picture_count)
        send_command(
            client=self.client, nickname=self.nick, command=self.change_picture
        )

    def next_pic(self):
        self.picture_count += 1

        # Report picture change to other users using change picture command
        self.change_picture = "!COMMAND_PICTURE_COUNT" + str(self.picture_count)
        send_command(
            client=self.client, nickname=self.nick, command=self.change_picture
        )

    def read_msg(self):
        while TRUE:
            received_message = receive(client=self.client, nickname=self.nick)
            if received_message == "!SOCKET CLOSED!":
                self.reconnect()
            elif received_message[:22] == "!COMMAND_PICTURE_COUNT":
                self.picture_count = int(received_message[22:])  # update picture count

                # Update buttons status
                if self.picture_buttons_avaliable:
                    self.previous_butt.configure(state="normal")
                    self.next_butt.configure(state="normal")

                    if self.picture_count <= 0:
                        self.previous_butt.configure(state="disabled")
                        self.picture_count = 0

                    if self.picture_count >= len(self.picture_list) - 1:
                        self.next_butt.configure(state="disabled")
                        self.picture_count = len(self.picture_list) - 1

                self.picture_path = self.picture_list[
                    self.picture_count
                ]  # update picture path
                self.img = self.adjust_image(
                    root=self.root,
                    picture_path=self.picture_path,
                    target_width=450,
                    target_heigh=460,
                )  # load new picture
                self.label_picture.configure(image=self.img)  # display new picture

            elif received_message[:25] == "!COMMAND_START_EXPERIMENT":
                self.experiment_in_progress = True
                # Enable next picture buttons if buttons are enabled and there are more than 1 pictures
                if self.picture_buttons_avaliable and len(self.picture_list) > 1:
                    self.next_butt.configure(state="normal")
                # Block sending messages for answering user
                if not self.picture_buttons_avaliable:
                    self.sending_blocked = True

            elif received_message[:26] == "!COMMAND_FINISH_EXPERIMENT":
                self.experiment_in_progress = False
                self.sending_blocked = False

            elif received_message[:2] == ">>":
                self.insert_server_message(received_message)

            elif self.experiment_in_progress and received_message[:7] != "!WIZARD":
                self.insert_user_message(received_message)
                # Unlock sending message
                self.sending_blocked = False

            elif received_message[:7] == "!WIZARD":
                self.insert_wizard_message(received_message)

            else:
                self.insert_user_message(received_message)

    def insert_user_message(self, received_message):
        # Split received message to nick and message
        nick, message = received_message.split(":", 1)
        # Inert bold nickname in chat window
        self.label_message.configure(state="normal")
        self.label_message.insert("end", f"{nick}:", "blue_bold")
        # Insert residual message
        self.label_message.insert("end", message, "blue")
        self.label_message.insert("end", "\n")
        self.label_message.configure(state="disabled")
        self.label_message.see("end")  # scroll to the end
        # Notify user with sound
        self.label_message.bell()

    def insert_wizard_message(self, received_message):
        # Split received message to nick and message
        nick, message = received_message[7:].split(":", 1)
        # Inert bold nickname in chat window
        self.label_message.configure(state="normal")
        self.label_message.insert("end", f"{nick}:", "red_bold")
        # Insert residual message
        self.label_message.insert("end", message, "red")
        self.label_message.insert("end", "\n")
        self.label_message.configure(state="disabled")
        self.label_message.see("end")  # scroll to the end

    def insert_server_message(self, received_message):
        self.label_message.configure(state="normal")
        self.label_message.insert("end", received_message)
        self.label_message.insert("end", "\n")
        self.label_message.configure(state="disabled")
        self.label_message.see("end")  # scroll to the end

    def send_msg(self):
        # Remove leading and trailing spaces and new lines
        input_msg = self.label_write.get("1.0", "end").strip(" \n")
        # Don't send empty messages (eg. Thread initialization, pressing Send button twice)
        if not input_msg:
            self.label_write.delete("1.0", "end")
            self.label_write.see("1.0")
            return "break"
        # Restrict sending messages to 1 per round during experiment
        ## Don't send message if answer is not received
        elif self.experiment_in_progress and self.sending_blocked:
            return "break"
        ## Send message and block sending another message until answer is received
        elif self.experiment_in_progress and not self.sending_blocked:
            self.sending_blocked = True
            # input_msg = f'{int(self.question_number)}. {input_msg}'
        # Send the message and clear write box
        write(client=self.client, nickname=self.nick, msg=input_msg)
        self.label_write.delete("1.0", "end")
        self.label_write.see("1.0")
        # Insert message to chat box
        self.label_message.configure(state="normal")
        self.label_message.insert("end", f"{self.nick}: ", "green_bold")
        self.label_message.insert("end", input_msg, "green")
        self.label_message.insert("end", "\n")
        self.label_message.configure(state="disabled")
        self.label_message.see("end")  # scroll to the end
        return "break"


MyGUI()
