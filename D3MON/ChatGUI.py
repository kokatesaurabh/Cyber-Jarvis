import tkinter as tk
import main

class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D3mon")
        self.root.configure(bg="#282a36")  # Dracula background color

        # Dracula color scheme
        self.dracula_pink = "#ff79c6"
        self.dracula_purple = "#bd93f9"
        self.dracula_white = "#f8f8f2"
        self.dracula_black = "#44475a"

        # Create chat history display
        self.chat_history = tk.Text(self.root, state=tk.DISABLED, bg="#282a36", fg=self.dracula_white, wrap="word",
                                    font=("Helvetica", 12))
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Create input field frame
        self.input_frame = tk.Frame(self.root, bg="#282a36")
        self.input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Create input field
        self.input_field = tk.Entry(self.input_frame, bg=self.dracula_white, fg=self.dracula_black,
                                    insertbackground=self.dracula_black, font=("Helvetica", 12), relief="flat", bd=2,
                                    width=70)
        self.input_field.grid(row=0, column=0, padx=5, sticky="ew")
        self.input_field.bind("<Return>", self.send_message)

        # Create send button
        self.send_button = tk.Button(self.input_frame, text="➤", bg=self.dracula_pink, fg=self.dracula_white,
                                     font=("Helvetica", 12), relief="flat", bd=2, command=self.send_message)
        self.send_button.grid(row=0, column=1, padx=(0, 5), sticky="e")
        self.send_button.bind("<Enter>", lambda event: self.animate_button(self.send_button, self.dracula_pink, self.dracula_white))
        self.send_button.bind("<Leave>", lambda event: self.animate_button(self.send_button, self.dracula_white, self.dracula_pink))

        # Create microphone button
        self.microphone_button = tk.Button(self.input_frame, text="🎤", bg=self.dracula_pink, fg=self.dracula_white,
                                           font=("Helvetica", 12), relief="flat", bd=2, command=self.record_audio)
        self.microphone_button.grid(row=0, column=2, padx=(0, 5), sticky="e")
        self.microphone_button.bind("<Enter>", lambda event: self.animate_button(self.microphone_button, self.dracula_pink, self.dracula_white))
        self.microphone_button.bind("<Leave>", lambda event: self.animate_button(self.microphone_button, self.dracula_white, self.dracula_pink))

        # Create camera button
        self.camera_button = tk.Button(self.input_frame, text="📷", bg=self.dracula_pink, fg=self.dracula_white,
                                       font=("Helvetica", 12), relief="flat", bd=2, command=self.take_picture)
        self.camera_button.grid(row=0, column=3, padx=(0, 5), sticky="e")
        self.camera_button.bind("<Enter>", lambda event: self.animate_button(self.camera_button, self.dracula_pink, self.dracula_white))
        self.camera_button.bind("<Leave>", lambda event: self.animate_button(self.camera_button, self.dracula_white, self.dracula_pink))

        # Configure grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def run(self):
        self.root.mainloop()

    def send_message(self, event=None):
        message = self.input_field.get()
        print("Sending message:", message)  # Debug print
        if message.strip() != "":
            # Saying the message
            main.say("You said: " + message)

            # Getting and saying the response
            response = main.assistant_response(message)
            # main.say("D3mon responded: " + response)

            # Displaying the message in chat history
            self.display_message("You: " + message)
            self.display_message("D3mon: " + response)

            # Clearing the input field
            self.input_field.delete(0, tk.END)
            print("Input field cleared")  # Debug print
        else:
            print("Empty message")  # Debug print
            self.input_field.delete(0, tk.END)  # Clear input field

    # def send_message(self, event=None):
    #     message = self.input_field.get()
    #     print("Sending message:", message)  # Debug print
    #     if message.strip() != "":
    #         self.display_message("You: " + message)
    #         response = main.assistant_response(message)
    #         self.display_message("D3mon: " + response)
    #         self.input_field.delete(0, tk.END)
    #         print("Input field cleared")  # Debug print
    #     else:
    #         print("Empty message")  # Debug print
    #         self.input_field.delete(0, tk.END)  # Clear input field



    def display_message(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
        self.input_field.delete(0, tk.END)

    def animate_button(self, button, bg_color, fg_color):
        current_bg = button.cget("bg")
        current_fg = button.cget("fg")
        if current_bg != bg_color:
            button.config(bg=bg_color, fg=fg_color)
        else:
            button.config(bg=fg_color, fg=bg_color)

    def take_picture(self):
        # Placeholder function for taking a picture
        print("Taking a picture...")

    def record_audio(self):
        # Placeholder function for recording audio
        print("Recording audio...")

if __name__ == "__main__":
    chat_gui = ChatGUI()
    chat_gui.run()
