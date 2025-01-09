# backend/backend.py

import requests
import time
from selenium import webdriver
import random

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

            print(f"Playing {video_name} on YouTube in {browser} browser.")
            time.sleep(10)  # Wait for the video to start playing

        else:
            print(f"No search results found for {video_name}.")

    except Exception as e:
        print(f"Error searching and playing on YouTube: {e}")
    finally:
        # Close the browser window after playing
        if driver is not None:
            driver.quit()
