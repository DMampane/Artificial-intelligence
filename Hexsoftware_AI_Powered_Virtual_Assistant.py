import speech_recognition as sr
import pyttsx3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import platform
import time

# Initialize Text-to-Speech
try:
    engine = pyttsx3.init()
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    engine = None

def speak(text):
    """Makie speaks the given text."""
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"Speaking failed. TTS not initialized: {text}")

def listen():
    """Capture user's voice input."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("I'm listening. Please tell me your query.")
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            query = recognizer.recognize_google(audio)
            print(f"You said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand that.")
            return None
        except sr.RequestError:
            speak("There seems to be an issue with my speech recognition service.")
            return None
        except Exception as e:
            print(f"Error during voice recognition: {e}")
            return None

def search_jobs(query):
    """Search for job opportunities on Google."""
    speak("Searching for job opportunities. Please hold on.")

    # Configure undetected_chromedriver
    options = webdriver.ChromeOptions()
    if platform.system() == "Windows":
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    elif platform.system() == "Darwin":  # macOS
        options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    else:  # Linux
        options.binary_location = "/usr/bin/google-chrome"

    try:
        driver = uc.Chrome(options=options)
        driver.get("https://www.google.com")
        time.sleep(2)

        # Search query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        speak("Here are the results. I have opened Google for you.")
        time.sleep(10)  # Give user time to see the results
    except Exception as e:
        print(f"Error during job search: {e}")
        speak(f"An error occurred: {e}")
    finally:
        driver.quit()

def main():
    """Main function for the assistant."""
    speak("Hello, I am Makie, your personal assistant. How can I help you today?")
    while True:
        command = listen()
        if command:
            if "job opportunities" in command or "chemical engineering" in command:
                search_jobs("Chemical Engineering jobs in South Africa actively recruiting")
            elif "exit" in command or "quit" in command:
                speak("Goodbye! Have a great day.")
                break
            else:
                speak("I can help you find job opportunities. Just say 'find job opportunities in Chemical Engineering'.")
        else:
            speak("Please repeat your request.")

if __name__ == "__main__":
    main()
