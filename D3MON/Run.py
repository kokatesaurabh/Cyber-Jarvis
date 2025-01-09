import platform
import os
import time
from gtts import gTTS
import cv2
import speech_recognition as sr
import win32com.client
import webbrowser
import asyncio
import json
import requests
import subprocess
import shodan
import csv
import aiohttp
import spotipy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from spotipy.oauth2 import SpotifyOAuth
import numpy as np



import random  # Import random module

SHODAN_API_KEY = ''  # Replace with your Shodan API key
# Spotify API credential
SPOTIPY_CLIENT_ID = 'bce4322f88a84bd18e323167ff82455b'
SPOTIPY_CLIENT_SECRET = '78469c2db5834aedbca94a384a4ffcbb'
SPOTIPY_REDIRECT_URI = 'http://localhost:8997/callback'

class_labels = ["person", "car", "cat", "dog"]


# Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope='user-library-read user-read-playback-state user-modify-playback-state'))


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
    # r = sr.Recognizer()
    try:
        # with sr.Microphone() as source:
        #     print("Adjusting for ambient noise...")
        #     r.adjust_for_ambient_noise(source, duration=0.5)
        #     print("Listening...")
        #     audio = r.listen(source, timeout=3, phrase_time_limit=5)
        #     query = r.recognize_google(audio, language="en-in")
        #     return query.lower()
    # except sr.UnknownValueError:
    #     return "Sorry, I did not get that. Please repeat."
    # except sr.RequestError as e:
    #     return ""
         # Use input to take text input
        query = input("Enter your command: ").lower()

        return query
    except Exception as e:
        return f"Some Error occurred. Sorry from D3mon: {e}"

def openWebsite(query, browser="chrome"):
    try:
        if not any(suffix in query for suffix in [".com", ".net", ".org",".ac", ".ac.uk", ".ad", ".ae", ".aero", ".af", ".ag", ".ai", ".al", ".am", ".an", ".ao", ".aq", ".ar",
                    ".arpa", ".as", ".asia", ".at", ".au", ".aw", ".ax", ".az", ".ba", ".bb", ".bd", ".be", ".bf", ".bg",
                    ".bh", ".bi", ".biz", ".bj", ".bm", ".bn", ".bo", ".br", ".bs", ".bt", ".bv", ".bw", ".by", ".bz", ".ca",
                    ".cat", ".cc", ".cd", ".cf", ".cg", ".ch", ".ci", ".ck", ".cl", ".cm", ".cn", ".co", ".co.uk", ".com",
                    ".coop", ".cr", ".cs", ".cu", ".cv", ".cw", ".cx", ".cy", ".cz", ".dd", ".de", ".dj", ".dk", ".dm", ".do",
                    ".dz", ".ec", ".edu", ".ee", ".eg", ".eh", ".er", ".es", ".et", ".eu", ".fi", ".firm", ".fj", ".fk", ".fm",
                    ".fo", ".fr", ".fx", ".ga", ".gb", ".gd", ".ge", ".gf", ".gg", ".gh", ".gi", ".gl", ".gm", ".gn", ".gov",
                    ".gov.uk", ".gp", ".gq", ".gr", ".gs", ".gt", ".gu", ".gw", ".gy", ".hk", ".hm", ".hn", ".hr", ".ht", ".hu",
                    ".id", ".ie", ".il", ".im", ".in", ".info", ".int", ".io", ".iq", ".ir", ".is", ".it", ".je", ".jm", ".jo",
                    ".jobs", ".jp", ".ke", ".kg", ".kh", ".ki", ".km", ".kn", ".kp", ".kr", ".kw", ".ky", ".kz", ".la", ".lb",
                    ".lc", ".li", ".lk", ".lr", ".ls", ".lt", ".ltd.uk", ".lu", ".lv", ".ly", ".ma", ".mc", ".md", ".me", ".me.uk",
                    ".mg", ".mh", ".mil", ".mk", ".ml", ".mm", ".mn", ".mo", ".mobi", ".mod.uk", ".mp", ".mq", ".mr", ".ms", ".mt",
                    ".mu", ".museum", ".mv", ".mw", ".mx", ".my", ".mz", ".na", ".name", ".nato", ".nc", ".ne", ".net", ".net.uk",
                    ".nf", ".ng", ".nhs.uk", ".ni", ".nl", ".no", ".nom", ".np", ".nr", ".nt", ".nu", ".nz", ".om", ".org", ".org.uk",
                    ".pa", ".pe", ".pf", ".pg", ".ph", ".pk", ".pl", ".plc.uk", ".pm", ".pn", ".post", ".pr", ".pro", ".ps", ".pt", ".pw",
                    ".py", ".qa", ".re", ".ro", ".rs", ".ru", ".rw", ".sa", ".sb", ".sc", ".sch.uk", ".sd", ".se", ".sg", ".sh", ".si",
                    ".sj", ".sk", ".sl", ".sm", ".sn", ".so", ".sr", ".ss", ".st", ".store", ".su", ".sv", ".sy", ".sz", ".tc", ".td",
                    ".tel", ".tf", ".tg", ".th", ".tj", ".tk", ".tl", ".tm", ".tn", ".to", ".tp", ".tr", ".travel", ".tt", ".tv", ".tw",
                    ".tz", ".ua", ".ug", ".uk", ".um", ".us", ".uy", ".uz", ".va", ".vc", ".ve", ".vg", ".vi", ".vn", ".vu", ".web", ".wf",
                    ".ws", ".xxx", ".ye", ".yt", ".yu", ".za", ".zm", ".zr", ".zw"]):
            query += ""

        if not query.startswith(("http://", "https://")):
            query = f"https://{query}"

        if browser.lower() == "firefox":
            subprocess.Popen([r"C:\Program Files\Mozilla Firefox\firefox.exe", query])
        elif browser.lower() == "chrome":
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

def search_username(username):
    try:
        sherlock_path = 'C:\\Users\\saura\\PycharmProjects\\Jarvis\\sherlock'  # Update with the correct path
        output_file = f'{username}_osint_results.txt'
        subprocess.run(['python', os.path.join(sherlock_path, 'sherlock'), username, '--output', output_file])

        with open(output_file, 'r') as file:
            results = file.read()

        os.remove(output_file)  # Remove the file after reading its content

        return results
    except Exception as e:
        return f"Error performing OSINT: {e}"

def search_and_play_youtube(song_name, browser="brave"):
    driver = None

    try:
        # Set up the browser driver
        if browser.lower() == "brave":
            browser_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        elif browser.lower() == "chrome":
            browser_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        else:
            raise ValueError("Invalid browser type. Supported types: 'brave', 'chrome'")

        driver_path = r"C:\Users\saura\Downloads\chromedriver-win64\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.binary_location = browser_path
        driver = webdriver.Chrome(executable_path=driver_path, options=options)

        # Open YouTube in the browser
        driver.get("https://www.youtube.com/")

        # Find the search input field and enter the song name
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search_query"))
        )
        search_box.send_keys(song_name)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "video-title"))
        )

        # Click on the first search result (assuming it's a video)
        first_result = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "video-title"))
        )
        first_result.click()

        print(f"Playing {song_name} on YouTube in {browser.capitalize()} browser.")

        # Wait for the video to start playing
        time.sleep(10)

    except Exception as e:
        print(f"Error searching and playing on YouTube: {e}")
    finally:
        if driver is not None:
            driver.quit()


def send_text_message(response):
    pass

def open_app(app_name):
    try:
        if "notepad" in app_name:
            subprocess.Popen(["notepad.exe"])
        elif "chrome" in app_name:
            subprocess.Popen(["C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"])
        elif "spotify" in app_name:
            subprocess.Popen(["C:\\Users\\saura\\AppData\\Local\\Microsoft\\WindowsApps\\spotify.exe"])
        elif "vscode" in app_name:
            subprocess.Popen(["C:\\Users\\saura\\Downloads\\VSCodeUserSetup-x64-1.85.2.exe"])
        elif "file explorer" in app_name:
            subprocess.Popen(["C:\\Windows\\explorer.exe"])
        elif "pycharm" in app_name:
            subprocess.Popen(["C:\\Users\\saura\\Downloads\\pycharm-community-2023.3.3.exe"])
        elif "brave" in app_name:
            subprocess.Popen(["C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"])
        elif "cmd" in app_name:
            subprocess.Popen(["C:\\Windows\\system32\\cmd.exe"])
        else:
            print(f"App {app_name} not recognized.")
            say(f"Sorry, I don't know how to open {app_name}.")

    except Exception as e:
        print(f"Error opening {app_name}: {e}")
        say(f"Sorry, I encountered an error while trying to open {app_name}.")

def is_website(target):
    return any(suffix in target for suffix in [".com", ".net", ".org",".ac", ".ac.uk", ".ad", ".ae", ".aero", ".af", ".ag", ".ai", ".al", ".am", ".an", ".ao", ".aq", ".ar",
                    ".arpa", ".as", ".asia", ".at", ".au", ".aw", ".ax", ".az", ".ba", ".bb", ".bd", ".be", ".bf", ".bg",
                    ".bh", ".bi", ".biz", ".bj", ".bm", ".bn", ".bo", ".br", ".bs", ".bt", ".bv", ".bw", ".by", ".bz", ".ca",
                    ".cat", ".cc", ".cd", ".cf", ".cg", ".ch", ".ci", ".ck", ".cl", ".cm", ".cn", ".co", ".co.uk", ".com",
                    ".coop", ".cr", ".cs", ".cu", ".cv", ".cw", ".cx", ".cy", ".cz", ".dd", ".de", ".dj", ".dk", ".dm", ".do",
                    ".dz", ".ec", ".edu", ".ee", ".eg", ".eh", ".er", ".es", ".et", ".eu", ".fi", ".firm", ".fj", ".fk", ".fm",
                    ".fo", ".fr", ".fx", ".ga", ".gb", ".gd", ".ge", ".gf", ".gg", ".gh", ".gi", ".gl", ".gm", ".gn", ".gov",
                    ".gov.uk", ".gp", ".gq", ".gr", ".gs", ".gt", ".gu", ".gw", ".gy", ".hk", ".hm", ".hn", ".hr", ".ht", ".hu",
                    ".id", ".ie", ".il", ".im", ".in", ".info", ".int", ".io", ".iq", ".ir", ".is", ".it", ".je", ".jm", ".jo",
                    ".jobs", ".jp", ".ke", ".kg", ".kh", ".ki", ".km", ".kn", ".kp", ".kr", ".kw", ".ky", ".kz", ".la", ".lb",
                    ".lc", ".li", ".lk", ".lr", ".ls", ".lt", ".ltd.uk", ".lu", ".lv", ".ly", ".ma", ".mc", ".md", ".me", ".me.uk",
                    ".mg", ".mh", ".mil", ".mk", ".ml", ".mm", ".mn", ".mo", ".mobi", ".mod.uk", ".mp", ".mq", ".mr", ".ms", ".mt",
                    ".mu", ".museum", ".mv", ".mw", ".mx", ".my", ".mz", ".na", ".name", ".nato", ".nc", ".ne", ".net", ".net.uk",
                    ".nf", ".ng", ".nhs.uk", ".ni", ".nl", ".no", ".nom", ".np", ".nr", ".nt", ".nu", ".nz", ".om", ".org", ".org.uk",
                    ".pa", ".pe", ".pf", ".pg", ".ph", ".pk", ".pl", ".plc.uk", ".pm", ".pn", ".post", ".pr", ".pro", ".ps", ".pt", ".pw",
                    ".py", ".qa", ".re", ".ro", ".rs", ".ru", ".rw", ".sa", ".sb", ".sc", ".sch.uk", ".sd", ".se", ".sg", ".sh", ".si",
                    ".sj", ".sk", ".sl", ".sm", ".sn", ".so", ".sr", ".ss", ".st", ".store", ".su", ".sv", ".sy", ".sz", ".tc", ".td",
                    ".tel", ".tf", ".tg", ".th", ".tj", ".tk", ".tl", ".tm", ".tn", ".to", ".tp", ".tr", ".travel", ".tt", ".tv", ".tw",
                    ".tz", ".ua", ".ug", ".uk", ".um", ".us", ".uy", ".uz", ".va", ".vc", ".ve", ".vg", ".vi", ".vn", ".vu", ".web", ".wf",
                    ".ws", ".xxx", ".ye", ".yt", ".yu", ".za", ".zm", ".zr", ".zw"])


def detect_objects_yolov8(image_path):
    # Load YOLOv8 model
    net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
    layer_names = net.getUnconnectedOutLayersNames()

    # Load image
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    # Normalize and preprocess image
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Run forward pass
    outs = net.forward(layer_names)

    # Get bounding boxes and confidence scores
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Adjust confidence threshold as needed
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Draw bounding boxes on the image
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indices:
            x, y, w, h = boxes[i]
            label = str(class_ids[i])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Save or display the image
    cv2.imwrite("output.jpg", image)
    cv2.imshow("YOLOv8 Object Detection", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    class_id = np.argmax(scores)
    class_label = class_labels[class_id] if class_id < len(class_labels) else "Unknown"

    # Print or use the class label for providing information
    print(f"Detected object: {class_label}")


def handle_command(query):
    try:
        if "play music" in query:
            open_app("Spotify")
            response = "Opening Spotify. What song would you like to listen to?"
            say(response)
            send_text_message(response)
            # Instead of taking input from the console, you might want to use speech recognition here.
            # Example: song_name = takeCommand()
            song_name = input("Enter the name of the song: ").strip()
            play_spotify(song_name)
            return
        elif "open website" in query:
            target = query.split('open website', 1)[1].strip()
            openWebsite(target, browser="chrome")
            response = f"Opening the requested website, sir."
        elif "open" in query:
            target = query.split('open')[1].strip()
            if is_website(target):
                openWebsite(target, browser="chrome")
                response = f"Opening the requested website, sir."
            else:
                open_app(target)
                response = f"Opening {target}, sir."
        else:
            response = "I'm sorry, I didn't quite catch that. Could you please repeat or ask something else?"

        say(response)
        send_text_message(response)
        return response
    except Exception as e:
        print(f"Error handling command: {e}")
        say(f"Sorry, I encountered an error while handling the command. {e}")

def play_spotify(track_name):
    # Search for the track
    results = sp.search(q=track_name, type='track', limit=1)

    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']

        # Play the track
        sp.start_playback(uris=[track_uri])
        print(f"Playing {track_name} on Spotify, sir.")
        say(f"Playing {track_name} on Spotify, sir.")
    else:
        print(f"Could not find the track: {track_name}")
        say(f"Sorry, I couldn't find the track {track_name} on Spotify.")

def assistant_response(query):
    try:
        if "hello" in query or "Hii" in query or "hii" in query or "hey" in query or "Hey" in query or "Hello" in query or "Heyy" in query:
            response = get_response('greeting')
        elif "how are you" in query:
            response = "I'm just a computer program, but I'm functioning well. How can I help you?"
        elif "what can you do" in query:
            response = "I can assist you with opening websites, providing Shodan information, and answering general questions. What do you need help with?"
        elif "open website" in query:
            target = query.split('open website', 1)[1].strip()
            openWebsite(target, browser="chrome")
            response = f"Opening the requested website, sir."
        elif "open" in query:
            target = query.split('open')[1].strip()
            if is_website(target):
                openWebsite(target, browser="chrome")
                response = f"Opening the requested website, sir."
            else:
                open_app(target)
                response = f"Opening {target}, sir."
        elif "tell me a joke" in query:
            response = "Why don't scientists trust atoms? Because they make up everything!"
        elif "how old are you" in query:
            response = "I don't have an age, as I'm just a piece of software running on a computer."
        elif "what is your name" in query:
            response = "You can call me D3mon. How can I assist you today?"
        elif "what is your main purpose?" in query:
            response = "My main purpose is to assist you in hacking tasks like 'social engineering', 'footprinting', 'cracking hashes', etc."
        elif "start footprinting" in query:
            username = input("Enter the username for OSINT: ")
            osint_results = search_username(username)
            response = osint_results
        elif "open spotify" in query:
            open_app("Spotify")
            response = "Opening Spotify. What song would you like to listen to?"
            say(response)
            send_text_message(response)
            song_name = input("Enter the name of the song: ").strip()
            play_spotify(song_name)
            return
        else:
            from z import replicate_chat
            replicate_chat()

        say(response)
        send_text_message(response)
        return response
    except Exception as e:
        print(f"Error in assistant_response: {e}")
        say(f"Sorry, I encountered an error while processing your request. {e}")



def search_and_play_youtube(video_name):
    # Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube Data API key
    youtube_api_key = 'AIzaSyC9hiVMtgJWurYfRR4D8bcYPloJQ8bRdhU'

    try:
        # Search for the song using YouTube Data API
        search_url = f'https://www.googleapis.com/youtube/v3/search?q={video_name}&part=snippet&type=video&key={'AIzaSyC9hiVMtgJWurYfRR4D8bcYPloJQ8bRdhU'}'
        response = requests.get(search_url)
        search_results = response.json()

        # Extract video ID of the first search result
        items = search_results.get('items', [])
        if items:
            video_id = items[0]['id']['videoId']

            # Play the video using the web browser
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            webbrowser.open(video_url)

            print(f"Playing {video_name} on YouTube.")
            time.sleep(10)  # Wait for the video to start playing
        else:
            print(f"No search results found for {song_name}.")

    except Exception as e:
        print(f"Error searching and playing on YouTube: {e}")

def search_and_play_youtube(video_name, browser="brave"):
    driver = None  # Initialize the driver outside the try block

    try:
        # Replace 'YOUR_YOUTUBE_API_KEY' with your actual YouTube Data API key
        youtube_api_key = 'AIzaSyC9hiVMtgJWurYfRR4D8bcYPloJQ8bRdhU'

        # Use the YouTube Data API to search for the song
        search_url = f'https://www.googleapis.com/youtube/v3/search?q={video_name}&part=snippet&type=video&key={youtube_api_key}'
        response = requests.get(search_url)
        search_results = response.json()

        # Debugging: Print the raw API response
        print("API Response:", search_results)

        # Extract video ID of the first search result
        items = search_results.get('items', [])
        if items:
            video_id = items[0]['id']['videoId']

            # Play the video using the specified browser
            if browser == "brave":
                brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
                options = webdriver.ChromeOptions()
                options.binary_location = brave_path
                driver = webdriver.Chrome(options=options)
            elif browser == "chrome":
                driver = webdriver.Chrome()

            video_url = f'https://www.youtube.com/watch?v={video_id}'
            driver.get(video_url)

            print(f"Playing {song_name} on YouTube in {browser} browser.")
            time.sleep(10)  # Wait for the video to start playing

            # Prompt user to press Enter before closing the browser window
            input("Press Enter to close the browser...")

        else:
            print(f"No search results found for {video_name}.")

    except Exception as e:
        print(f"Error searching and playing on YouTube: {e}")
    finally:
        # Close the browser window after playing
        if driver is not None:
            driver.quit()



def detect_objects(image_path, net, layer_names):
    # Read the image
    frame = cv2.imread(image_path)

    # Normalize and preprocess image
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Run forward pass
    outs = net.forward(layer_names)

    # Get bounding boxes and confidence scores
    class_ids = []
    confidences = []
    boxes = []

    height, width, _ = frame.shape

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Adjust confidence threshold as needed
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    # Draw bounding boxes on the image
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    for i in range(len(boxes)):
        if i in indices:
            x, y, w, h = boxes[i]
            label = str(class_ids[i])
            confidence = confidences[i]
            color = (0, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the resulting frame
    cv2.imshow("YOLOv8 Object Detection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print('PyCharm')
    say("Hello, I am D3mon. Listening for text messages.")

    while True:
        query = input("Enter your command: ").lower()

        if "exit" in query or "bye" in query or "goodbye" in query:
            print("Goodbye! Have a great day.")
            say("Goodbye! Have a great day.")
            break

        elif "play video" in query:
            response = "Sure! What video would you like to see to?"
            say(response)
            send_text_message(response)
            song_name = input("Enter the name of the video: ").strip()
            browser_type = input("Enter the browser type (brave or chrome): ").strip()
            search_and_play_youtube(song_name, browser=browser_type)

        elif "detect objects" in query:
            from eye import detect_objects

            # image_path = input("Enter the path of the image: ").strip()
            detect_objects()

        elif "perform osint" in query:
            from osint import osint_tool

            osint_tool()

        elif "vulnerability" in query or "find vulnerability" in query or "Scan Website" in query:
            from WebSec import check_vulnerabilities

            website_url = input("Enter the URL of the website to check for vulnerabilities: ")

            asyncio.run(check_vulnerabilities(website_url))

        elif "hashcrack" in query or "crack hash" in query or "find hash" in query:
            from HashCracker import hash_cracker

            hash_cracker()

        elif "start stego" in query or "Perform stegnography" in query or "Stegnography" in query:
            from Stegnography import steganography

            steganography()


        else:
            assistant_reply = assistant_response(query)
            print("Assistant:", assistant_reply)




