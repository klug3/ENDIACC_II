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
    save_backup,
    validate_entered_values,
    save_dialogue_file,
)
import threading
import glob
import time


class MyGUI:

    # Class variables:
    picture_count = 0
    picture_list = []
    picture_buttons_avaliable = True

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
            bg="#8EBBED",
            fg="white",
            command=self.connect,
        )
        self.connect_butt.grid(row=0, column=2, rowspan=3, sticky="ns")

        ## SET DEFAULT VALUES FOR EACH ENTRY
        self.entry_ip.insert(0, "endiacc.projektstudencki.pl")
        self.entry_port.insert(0, "8282")
        # self.entry_nick.insert(0, "Wizard")

        self.frame1.pack(fill="x")

        ###########################################
        ## DISPLAY IMAGES
        self.frame2 = tk.Frame(self.root)
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.columnconfigure(1, weight=1)
        self.frame2.columnconfigure(2)  # For scrollbar

        # Find PATH to 1st picture
        self.picture_1_path = self.get_picture_list()[0]
        # Find PATH to 2nd picture
        self.picture_2_path = self.get_picture_list()[1]

        # Load and adjust images sizes
        self.img_1 = self.adjust_image(
            root=self.root,
            picture_path=self.picture_1_path,
            target_width=450,
            target_heigh=250,
        )
        self.img_2 = self.adjust_image(
            root=self.root,
            picture_path=self.picture_2_path,
            target_width=450,
            target_heigh=250,
        )

        # Put img_1 as a label
        self.label_picture_1 = tk.Label(self.frame2, image=self.img_1)
        self.label_picture_1.grid(row=0, column=0, sticky="we")

        # Put img_2 as a label
        self.label_picture_2 = tk.Label(self.frame2, image=self.img_2)
        self.label_picture_2.grid(row=1, column=0, sticky="we")

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
        self.label_message.grid(row=0, column=1, sticky="we", rowspan=2)

        # Add tag to enable bold entries (nicknames) in chat window
        self.label_message.tag_configure("bold", font=("Helvetica", 12, "bold"))

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
        self.scrollbar_chat.grid(row=0, column=2, sticky="ns", rowspan=2)

        #############################################################
        ## BUTTONS
        self.frame3 = tk.Frame(self.root)
        self.frame3.columnconfigure(0, weight=10)
        self.frame3.columnconfigure(1, weight=10)
        self.frame3.columnconfigure(2, weight=10)
        self.frame3.columnconfigure(3, weight=1)

        # Previous picture
        self.previous_butt = tk.Button(
            self.frame3,
            text="Previous",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.previous_pic,
        )
        self.previous_butt.grid(row=1, column=0, sticky="we")
        self.previous_butt.configure(state="disabled")

        # Next picture
        self.next_butt = tk.Button(
            self.frame3,
            text="Next",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.next_pic,
        )
        self.next_butt.grid(row=1, column=1, sticky="we")
        self.next_butt.configure(state="disabled")

        # Start/finish experiment button
        self.experiment_butt = tk.Button(
            self.frame3,
            text="Start experiment",
            relief="groove",
            bg="#429E19",
            fg="black",
            font=("Helvetica", 12, "bold"),
            command=self.start_experiment,
        )
        self.experiment_butt.grid(row=1, column=2, sticky="we")
        self.experiment_butt.configure(state="normal")

        #############################################################
        ## WRITE BOX
        self.frame4 = tk.Frame(self.root)
        self.frame4.columnconfigure(0, weight=1)
        self.frame4.columnconfigure(1)  # For scrollbar

        self.label_write = tk.Text(
            self.frame4,
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
            self.frame4, orient="vertical", command=self.label_write.yview
        )
        self.label_write.configure(yscrollcommand=self.scrollbar_writebox.set)
        self.scrollbar_writebox.grid(row=0, column=1, sticky="ns")

        ##############################################################
        ## SAVE, UNLOCK CHAT, CLEAR WINDOW AND SEND BUTTONS
        self.frame5 = tk.Frame(self.root)
        self.frame5.columnconfigure(0, weight=1)
        self.frame5.columnconfigure(1, weight=1)
        self.frame5.columnconfigure(2, weight=1)
        self.frame5.columnconfigure(3, weight=1)

        # Save Button
        self.save_butt = tk.Button(
            self.frame5,
            text="Save",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.save_dialogue,
        )
        self.save_butt.grid(row=0, column=0, sticky="we")
        self.save_butt.configure(state="normal")

        # Chat button
        self.chat_butt = tk.Button(
            self.frame5,
            text="Unlock chat",
            relief="groove",
            font=("Helvetica", 12),
            command=self.unlock_chat,
        )
        self.chat_butt.grid(row=0, column=1, sticky="we")
        self.chat_butt.configure(state="normal")

        # Clear chat window Button
        self.clear_butt = tk.Button(
            self.frame5,
            text="Clear chat",
            relief="groove",
            font=("Helvetica", 12),
            command=self.clear_chat_window,
        )
        self.clear_butt.grid(row=0, column=2, sticky="we")
        self.clear_butt.configure(state="normal")

        # Send Button
        self.send_butt = tk.Button(
            self.frame5,
            text="Send",
            relief="groove",
            font=("Helvetica", 12, "bold"),
            command=self.send_msg,
        )
        self.send_butt.grid(row=0, column=3, sticky="we")
        self.send_butt.configure(state="normal")

        # Run key bindings function
        self.bindings()

        self.root.mainloop()

    def bindings(self):
        self.label_write.bind("<Return>", lambda event: self.send_msg())
        self.label_write.bind("<Control-Return>", self.new_line)
        self.label_picture_1.bind(
            "<Button-1>", lambda event: self.start_canvas(self.picture_1_path)
        )
        self.label_picture_1.bind("<ButtonRelease-1>", self.close_canvas)
        self.label_picture_2.bind(
            "<Button-1>", lambda event: self.start_canvas(self.picture_2_path)
        )
        self.label_picture_2.bind("<ButtonRelease-1>", self.close_canvas)

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

    def unlock_chat(self):
        self.label_message.configure(state="normal")
        # Update chat_button
        self.chat_butt.configure(text="Lock chat", bg="#D2100C", command=self.lock_chat)

    def lock_chat(self):
        self.label_message.configure(state="disabled")
        # Update unlock_button
        self.chat_butt.configure(
            text="Unlock chat", bg="#f0f0f0", command=self.unlock_chat
        )

    def clear_chat_window(self):
        self.label_message.configure(state="normal")
        content = self.label_message.get("1.0", "end-2c")
        # Save conternt and get saved file name
        file_name = save_backup(content)
        # Clean chat window
        self.label_message.delete("1.0", "end")
        self.label_message.configure(state="disabled")
        # Show info
        messagebox.showinfo("Information", f"Chat content archived as: {file_name}.")

    def save_dialogue(self):
        dialogue_raw = self.label_message.get("1.0", "end-2c")
        # Save raw and clean dialogue files:
        files_names_list = save_dialogue_file(dialogue_raw, self.nick)
        ## Covert list of names to string
        created_files = "\n".join([str(x) for x in files_names_list])
        # Show info
        messagebox.showinfo(
            "Information", f"Chat content archived as:\n{created_files}."
        )

    def start_experiment(self):
        # Inform other clients
        send_command(
            client=self.client, nickname=self.nick, command="!COMMAND_START_EXPERIMENT"
        )
        # Update experiment_button
        self.experiment_butt.configure(
            text="Finish experiment", bg="#D2100C", command=self.finish_experiment
        )

    def finish_experiment(self):
        # Inform other clients
        send_command(
            client=self.client, nickname=self.nick, command="!COMMAND_FINISH_EXPERIMENT"
        )
        # Update experiment_button
        self.experiment_butt.configure(
            text="Start experiment", bg="#429E19", command=self.start_experiment
        )

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
        self.frame2.pack(fill="x")  # Pictures and chat window
        self.frame3.pack(fill="x")  # Previous, next, start exp buttons
        self.frame4.pack(fill="x")  # Write box
        self.frame5.pack(fill="x")  # Save, clear, send buttons

        # Hide connection related labels
        self.frame1.destroy()

        # Enable next picture button if there are more than 1 pictures
        if len(self.picture_list) > 1:
            self.next_butt.configure(state="normal")

        # Start read_msg() and send_msg() functions as new threads
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
        # Get paths to all pictures in ./pictures_wizard directory
        self.picture_list = glob.glob("./pictures_wizard/*.jpg")
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
        # cl.write(client=self.client, nickname=self.nick, msg=self.change_picture)

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

                    if self.picture_count >= (len(self.picture_list) / 2) - 1:
                        self.next_butt.configure(state="disabled")
                        self.picture_count = int(
                            (len(self.picture_list) / 2) - 1
                        )  # Division results in float number

                self.picture_1_path = self.picture_list[
                    self.picture_count * 2
                ]  # update picture_1_path
                self.picture_2_path = self.picture_list[
                    (self.picture_count * 2) + 1
                ]  # update picture_2_path
                self.img_1 = self.adjust_image(
                    root=self.root,
                    picture_path=self.picture_1_path,
                    target_width=450,
                    target_heigh=250,
                )  # load new picture_1
                self.img_2 = self.adjust_image(
                    root=self.root,
                    picture_path=self.picture_2_path,
                    target_width=450,
                    target_heigh=250,
                )  # load new picture_2
                self.label_picture_1.configure(
                    image=self.img_1
                )  # display new picture_1
                self.label_picture_2.configure(
                    image=self.img_2
                )  # display new picture_2
                picture_1_name = self.get_picture_name(
                    self.picture_1_path
                )  # get name of the 1st picture
                picture_2_name = self.get_picture_name(
                    self.picture_2_path
                )  # get name of the 2nd picture
                self.info_message = f">>Pictures changed to: {picture_1_name} and {picture_2_name}.\n"  # Create info msg
                self.label_message.configure(state="normal")
                self.label_message.insert("end", self.info_message)
                self.label_message.configure(state="disabled")
                self.label_message.see("end")  # scroll to the end

            elif received_message[:25] == "!COMMAND_START_EXPERIMENT":
                self.label_message.configure(state="normal")
                self.label_message.insert("end", ">>EXPERIMENT STARTED.\n")
                self.label_message.configure(state="disabled")
                self.label_message.see("end")  # scroll to the end

            elif received_message[:26] == "!COMMAND_FINISH_EXPERIMENT":
                self.label_message.configure(state="normal")
                self.label_message.insert("end", ">>EXPERIMENT FINISHED.\n")
                self.label_message.configure(state="disabled")
                self.label_message.see("end")  # scroll to the end

            elif received_message[:2] == ">>":
                self.insert_server_message(received_message)

            else:
                self.inser_user_message(received_message)

    def inser_user_message(self, received_message):
        # Split received message to nick and message
        nick, message = received_message.split(":", 1)
        # Inert bold nickname in chat window
        self.label_message.configure(state="normal")
        self.label_message.insert("end", f"{nick}:", "bold")
        # Insert residual message
        self.label_message.insert("end", message)
        self.label_message.insert("end", "\n")
        self.label_message.configure(state="disabled")
        self.label_message.see("end")  # scroll to the end

    def insert_server_message(self, received_message):
        self.label_message.configure(state="normal")
        self.label_message.insert("end", received_message)
        self.label_message.insert("end", "\n")
        self.label_message.configure(state="disabled")
        self.label_message.see("end")  # scroll to the end

    def get_picture_name(self, picture_path):
        # replace / with \ to unify path on different OS
        picture_path = picture_path.replace("/", "\\")
        picture_name = picture_path.split("\\")[
            -1
        ]  # last element of the list is the picture name
        return picture_name

    def send_msg(self):
        # Remove leading and trailing spaces and new lines
        input_msg = self.label_write.get("1.0", "end").strip(" \n")
        # Don't send empty messages (eg. Thread initialization, pressing Send button twice)
        if input_msg:
            # Send message as a wizard
            write(
                client=self.client,
                nickname=self.nick,
                msg=input_msg,
                sent_by_wizard=True,
            )
            # Insert message to chat box
            self.label_message.configure(state="normal")
            self.label_message.insert("end", f"{self.nick}: ", "red_bold")
            self.label_message.insert("end", input_msg, "red")
            self.label_message.insert("end", "\n")
            self.label_message.configure(state="disabled")
            self.label_message.see("end")  # scroll to the end
            self.label_write.delete("1.0", "end")
            self.label_write.see("1.0")
        return "break"


MyGUI()
