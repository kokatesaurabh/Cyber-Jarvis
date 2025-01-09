import platform
import os
import speech_recognition as sr
import win32com.client
import webbrowser
import subprocess
import shodan
import csv
import random  # Import random module

SHODAN_API_KEY = 'XAbsu1Ruj5uhTNcxGdbGNgrh9WuMS1B6'  # Replace with your Shodan API key


# Placeholder for get_response function
def get_response(category=None):
    responses = {
        'greeting': [
            "Hello, how can I assist you today?",
            "Greetings! What do you need help with?",
            "Hi there! How may I be of service?",
            "Good day! What can I do for you?"
        ],
        'confirmation': [
            "Yes, how can I assist you?",
            "Certainly! What do you need?",
            "At your service!",
            "What can I do for you?",
            "Ready to help!"
        ],
        'farewell': [
            "Goodbye! If you need anything else, feel free to ask.",
            "Farewell! Let me know if there's anything else I can do for you.",
            "Until next time! Take care.",
            "Have a great day! If you have more questions, just ask."
        ],
        # Add more categories and responses as needed
    }

    if category is not None and category in responses:
        return random.choice(responses[category])
    else:
        all_responses = [response for category_responses in responses.values() for response in category_responses]
        return random.choice(all_responses)


def say(text):
    system_platform = platform.system().lower()
    if system_platform == 'darwin':
        os.system(f"say {text}")
    elif system_platform == 'linux':
        os.system(f"espeak -s 150 -v en '{text}'")
    elif system_platform == 'windows':
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        speaker.Rate = 2  # Adjust the rate as needed
        speaker.Speak(text)
    else:
        print("Text-to-speech not supported on this platform.")


def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
            query = r.recognize_google(audio, language="en-in")
            return query.lower()
    except sr.UnknownValueError:
        return "Sorry, I did not get that. Please repeat."
    except sr.RequestError as e:
        return ""
    except Exception as e:
        return f"Some Error occurred. Sorry from D3mon: {e}"


def openWebsite(query, browser="chrome"):
    try:
        if not any(suffix in query for suffix in [".com", ".net", ".org"]):
            query += ".com"

        if not query.startswith(("http://", "https://")):
            query = f"https://{query}"

        if browser.lower() == "chrome":
            subprocess.Popen([r"C:\Program Files\Google\Chrome\Application\chrome.exe", query])
        elif browser.lower() == "brave":
            subprocess.Popen([r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe", query])
        else:
            webbrowser.open(query)

        say(f"Opening website {query} in {browser.capitalize()} Sir...")

        # Shodan integration
        shodan_info = getShodanInfo(query)
        if shodan_info:
            say(f"Shodan Info: {shodan_info}")

            # Save Shodan information to a CSV file
            saveToCSV(query, shodan_info)

    except Exception as e:
        print(f"Error opening website: {e}")
        say(f"Sorry, I encountered an error while trying to open the website. {e}")


def getShodanInfo(query):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.search(query)
        return f"Shodan Result: {result['total']} matches found.\n{result['matches']}"
    except shodan.APIError as e:
        if e.value == '403 Forbidden':
            return "Access to Shodan API is denied. Please check your API key."
        else:
            print(f"Shodan API error: {e}")
            return None


def saveToCSV(query, shodan_info):
    try:
        with open('shodan_dataset.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Query', 'Shodan_Info']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({'Query': query, 'Shodan_Info': shodan_info})
    except Exception as e:
        print(f"Error saving to CSV: {e}")


def assistant_response(query):
    if "hello" in query or "hi" in query:
        return get_response('greeting')
    elif "how are you" in query:
        return "I'm just a computer program, but I'm functioning well. How can I help you?"
    elif "what can you do" in query:
        return "I can assist you with opening websites, providing Shodan information, and answering general questions. What do you need help with?"
    elif "open" in query:
        openWebsite(query.split('open')[1].strip(), browser="chrome")
        return "Opening the requested website, sir."
    elif "tell me a joke" in query:
        return "Why don't scientists trust atoms? Because they make up everything!"
    elif "how old are you" in query:
        return "I don't have an age, as I'm just a piece of software running on a computer."
    elif "what is your name" in query:
        return "You can call me D3mon. How can I assist you today?"
    # Add more categories and responses as needed
    else:
        return "I'm sorry, I didn't quite catch that. Could you please repeat or ask something else?"


if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am D3mon")
    while True:
        print("Listening...")
        query = takeCommand()

        if "exit" in query or "bye" in query or "goodbye" in query:
            print("Goodbye! Have a great day.")
            say("Goodbye! Have a great day.")
            break

        assistant_reply = assistant_response(query)
        print("Assistant:", assistant_reply)
        say(assistant_reply)
