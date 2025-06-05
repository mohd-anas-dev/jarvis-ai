from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

env_vars = dotenv_values(".env")
InputLanguage = env_vars.get("InputLanguage")

HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

HtmlCode = str(HtmlCode).replace("recognition.lang = '';", f" recognition.lang = '{InputLanguage}';")

with open(r"Data\Voice.html", "w") as f:
    f.write(HtmlCode)

current_dir = os.getcwd()
Link = f"{current_dir}\Data\Voice.html"

chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
chrome_options.add_argument(f'user-agent={user_agent}') 
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options) 

TempDirPath = rf"{current_dir}/Frontend/Files"

def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}/Status.data', "w", encoding='utf-8') as file:
        file.write(Status)

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's", "is it", "can you"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    else:
        if query_words[-1][-1] in ['.', '?', '!']:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."
    return new_query.capitalize()

def UniversalTranslator(Text):
    # First check if the text has non-Latin characters (potential Hindi)
    has_non_latin = any(ord(c) > 127 for c in Text)
    
    if has_non_latin:
        # Translate the entire text to ensure all Hindi portions are converted
        english_translation = mt.translate(Text, "en", "auto")
        print(f"Translated from mixed language: {Text} -> {english_translation}")
        return english_translation.capitalize()
    else:
        # Already English, just return it
        return Text.capitalize()
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

def SpeechRecognition(force_restart=False):
    try:
        # If force_restart is True or we're encountering issues, do a more thorough reset
        if force_restart:
            try:
                # Try to stop any ongoing recognition
                driver.find_element(By.ID, value="end").click()
            except Exception as e:
                print(f"Reset error (non-critical): {e}")
                
            # Refresh the page completely
            driver.get("file:///" + Link)
            
            # Small delay to ensure page loads properly
            from time import sleep
            sleep(0.5)
            
        else:
            # Normal operation - just make sure the page is loaded
            current_url = driver.current_url
            if not current_url.endswith("Voice.html"):
                driver.get("file:///" + Link)
        
        # Start recognition
        driver.find_element(By.ID, value="start").click()
        
        # Main recognition loop
        while True:
            try:
                Text = driver.find_element(By.ID, value="output").text
                if Text:
                    # Successfully got text, stop recognition
                    driver.find_element(By.ID, value="end").click()
                    
                    # Process the text
                    SetAssistantStatus("Processing...")
                    translated_text = UniversalTranslator(Text)
                    
                    # Check if translation is different from original
                    if translated_text.lower() != Text.lower():
                        print(f"Original: {Text}")
                        print(f"Translated: {translated_text}")
                    
                    return QueryModifier(translated_text)
                    
            except Exception as e:
                print(f"Recognition loop error (non-critical): {e}")
                # Continue trying to get text
                pass
    
    except Exception as e:
        print(f"Critical error in speech recognition: {e}")
        # In case of a critical error, try to reset everything
        try:
            driver.get("file:///" + Link)
            driver.find_element(By.ID, value="start").click()
            return "I'm sorry, I had trouble hearing you. Could you repeat that?"
        except:
            return "I encountered an error with speech recognition. Please try again."
        
        
if __name__ == "__main__":
    while True:
        Text = SpeechRecognition()
        print(Text)
