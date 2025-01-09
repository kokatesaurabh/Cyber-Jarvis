import tkinter as tk
from main import say, search_and_play_youtube, detect_objects, osint_tool, check_vulnerabilities, hash_cracker, steganography

def handle_command():
    query = entry.get().lower()

    if "exit" in query or "bye" in query or "goodbye" in query:
        response_label.config(text="Goodbye! Have a great day.")
        say("Goodbye! Have a great day.")

    elif "jailbreak chatgpt" in query:
        # Your handling logic for "jailbreak chatgpt"

    elif "play video" in query:
        response = "Sure! What video would you like to see?"
        response_label.config(text=response)
        say(response)
        song_name = video_entry.get().strip()
        browser_type = browser_entry.get().strip()
        search_and_play_youtube(song_name, browser=browser_type)

    elif "detect objects" in query:
        # Your handling logic for "detect objects"

    elif "perform osint" in query:
        # Your handling logic for "perform osint"

    elif "vulnerability" in query or "find vulnerability" in query or "Scan Website" in query:
        # Your handling logic for "vulnerability"

    elif "hashcrack" in query or "crack hash" in query or "find hash" in query:
        # Your handling logic for "hashcrack"

    elif "start stego" in query or "Perform stegnography" in query or "Stegnography" in query:
        # Your handling logic for "start stego"

    else:
        assistant_reply = "Assistant: " + assistant_response(query)
        response_label.config(text=assistant_reply)

# Create the main Tkinter window
root = tk.Tk()
root.title("Command Prompt")

# Create an entry box for user input
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create a button to trigger command execution
button = tk.Button(root, text="Execute", command=handle_command)
button.pack(pady=5)

# Create a label to display responses
response_label = tk.Label(root, text="")
response_label.pack(pady=10)

# If the command is "play video", ask for video name and browser type
video_entry = tk.Entry(root, width=50)
video_entry.pack(pady=5)
browser_entry = tk.Entry(root, width=20)
browser_entry.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
