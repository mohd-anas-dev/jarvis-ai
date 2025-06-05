from Backend.SystemPrompts import get_volume_response, get_battery_response, get_brightness_response
from Backend.TaskExecutor import handle_task_command
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
import re
import random
import psutil
import platform

# For volume control
if platform.system() == "Windows":
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# For brightness control
import screen_brightness_control as sbc

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "Z0LcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta",
           "IZ6rdc", "O5uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table__webanswers-table", "dDoNo ikb4Bb gsrt", "xSLaOe",
           "LWkfKe", "VQF4g", "qv3Wpe", "know-rdesc", "SPZz6b"]

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

client = Groq(api_key=GroqAPIKey)

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with Sir.",
    "I'm at your service for any additional questions or support you may need, Sir.",
]

messages = []

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letter"}]

class SystemControl:
    def __init__(self):
        self.os_type = platform.system()
        # Initialize volume control
        if self.os_type == "Windows":
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_control = cast(interface, POINTER(IAudioEndpointVolume))
        
        # Battery status messages
        self.battery_messages = {
            "high": [
                "Battery is well charged and ready to go, Sir.",
                "Power levels are optimal. We're good to go.",
                "Battery is in good condition, no need to worry about charging.",
                "All charged up and ready for action, Sir.",
                "Power situation is looking good. We're set."
            ],
            "medium": [
                "Battery is at a moderate level.",
                "You still have a decent amount of power left.",
                "Battery is holding up fine for now.",
                "We're running on adequate power, Sir.",
                "Battery levels are acceptable at the moment."
            ],
            "low": [
                "Battery is getting low, might want to plug in soon.",
                "Power is running low, consider charging soon.",
                "Battery needs attention in the near future.",
                "I'd recommend finding a power source soon, Sir.",
                "We're running on limited power. Might be time to charge."
            ],
            "critical": [
                "Battery is critically low, please connect to power immediately.",
                "Power levels are dangerously low, charge now to avoid shutdown.",
                "Critical battery level detected, urgent charging required.",
                "Sir, we need power now. System shutdown is imminent.",
                "Emergency power situation. Please connect to a charger immediately."
            ],
            "charging": [
                "Battery is currently charging.",
                "Power is being replenished.",
                "The battery is charging up nicely.",
                "We're plugged in and charging, Sir.",
                "Power levels are increasing. Charging in progress."
            ]
        }
    
    def control_volume(self, command):
        """
        Controls system volume based on user command
        Commands can be like:
        - "Set volume to 20"
        - "Decrease volume by 10"
        - "Increase volume by 5"
        """
        try:
            # Extract the numeric value and action type from command
            if "set volume to" in command.lower():
                level_match = re.search(r'set volume to (\d+)', command.lower())
                if level_match:
                    level = int(level_match.group(1))
                    return self._set_volume(level)
                else:
                    return "I couldn't understand the volume level requested."
                    
            elif "increase volume by" in command.lower():
                amount_match = re.search(r'increase volume by (\d+)', command.lower())
                if amount_match:
                    amount = int(amount_match.group(1))
                    return self._change_volume(amount)
                else:
                    return "I couldn't understand how much to increase the volume."
                    
            elif "decrease volume by" in command.lower():
                amount_match = re.search(r'decrease volume by (\d+)', command.lower())
                if amount_match:
                    amount = int(amount_match.group(1))
                    return self._change_volume(-amount)
                else:
                    return "I couldn't understand how much to decrease the volume."
                    
            else:
                return "I didn't understand the volume command. Try saying 'set volume to 50' or 'increase volume by 10'."
        except Exception as e:
            return f"Error controlling volume: {str(e)}"
    
    def control_brightness(self, command):
        """
        Controls screen brightness based on user command
        Commands can be like:
        - "Set brightness to 70"
        - "Decrease brightness by 20"
        - "Increase brightness by 15"
        """
        try:
            # Extract the numeric value and action type from command
            if "set brightness to" in command.lower():
                level_match = re.search(r'set brightness to (\d+)', command.lower())
                if level_match:
                    level = int(level_match.group(1))
                    return self._set_brightness(level)
                else:
                    return "I couldn't understand the brightness level requested."
                    
            elif "increase brightness by" in command.lower():
                amount_match = re.search(r'increase brightness by (\d+)', command.lower())
                if amount_match:
                    amount = int(amount_match.group(1))
                    return self._change_brightness(amount)
                else:
                    return "I couldn't understand how much to increase the brightness."
                    
            elif "decrease brightness by" in command.lower():
                amount_match = re.search(r'decrease brightness by (\d+)', command.lower())
                if amount_match:
                    amount = int(amount_match.group(1))
                    return self._change_brightness(-amount)
                else:
                    return "I couldn't understand how much to decrease the brightness."
                    
            else:
                return "I didn't understand the brightness command. Try saying 'set brightness to 70' or 'increase brightness by 15'."
        except Exception as e:
            return f"Error controlling brightness: {str(e)}"
    
    def check_battery(self):
        """
        Checks battery status and returns a dynamic message based on charge level
        """
        try:
            battery = psutil.sensors_battery()
            if battery is None:
                return "I couldn't detect a battery. Your device might be a desktop or the battery information is not accessible."
            
            percent = battery.percent
            power_plugged = battery.power_plugged
            time_str = None
            
            # Determine status message category
            if power_plugged and battery.secsleft != 0:
                hours, remainder = divmod(battery.secsleft, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str =""

                if hours > 0:
                    time_str += f"{hours} hour{'s' if hours != 1 else ''} "
                if minutes > 0:
                    time_str += f"{minutes} minute{'s' if minutes != 1 else ''} "
            elif not power_plugged and battery.secsleft != -1:
                hours, remainder = divmod(battery.secsleft, 3600)
                minutes, seconds = divmod(remainder, 60)
                time_str = ""
                if hours > 0:
                    time_str += f"{hours} hour{'s' if hours != 1 else ''} "
                if minutes > 0:
                    time_str += f"{minutes} minute{'s' if minutes != 1 else ''} "

            return get_battery_response(percent, power_plugged, time_str)
        
        except Exception as e:
                return f"Error checking battery status: {str(e)}"
    
    def _set_volume(self, level):
        """Set volume to a specific level (0-100)"""
        if level < 0:
            level = 0
        elif level > 100:
            level = 100
        
        try:
            if self.os_type == "Windows":
                # In Windows, volume is between 0 and 1
                self.volume_control.SetMasterVolumeLevelScalar(level / 100, None)
                return get_volume_response("set", level=level)
            elif self.os_type == "Darwin":  # macOS
                os.system(f"osascript -e 'set volume output volume {level}'")
                return get_volume_response("set", level=level)
            elif self.os_type == "Linux":
                os.system(f"amixer -D pulse sset Master {level}%")
                return get_volume_response("set", level=level)
            else:
                return "Volume control is not supported on this operating system."
        except Exception as e:
            return f"Error setting volume: {str(e)}"
    
    def _change_volume(self, change_amount):
        """Increase or decrease volume by a given amount"""
        try:
            current_level = self._get_current_volume()
            new_level = current_level + change_amount
            self._set_volume(new_level)

            action = "increase" if change_amount > 0 else "decrease"
            change_amount_abs = abs(change_amount)
            return get_volume_response(action, level=new_level, amount=change_amount_abs)
        except Exception as e:
            return f"Error changing volume: {str(e)}"
    
    def _get_current_volume(self):
        """Get the current volume level (0-100)"""
        try:
            if self.os_type == "Windows":
                current_volume = self.volume_control.GetMasterVolumeLevelScalar() * 100
                return int(current_volume)
            elif self.os_type == "Darwin":  # macOS
                cmd = "osascript -e 'output volume of (get volume settings)'"
                result = subprocess.check_output(cmd, shell=True).strip()
                return int(result)
            elif self.os_type == "Linux":
                cmd = "amixer -D pulse sget Master | grep 'Left:' | awk -F'[][]' '{ print $2 }' | tr -d '%'"
                result = subprocess.check_output(cmd, shell=True).strip()
                return int(result)
            else:
                return 50  # Default fallback
        except Exception as e:
            print(f"Error getting current volume: {str(e)}")
            return 50  # Default fallback
    
    def _set_brightness(self, level):
        """Set brightness to a specific level (0-100)"""
        if level < 0:
            level = 0
        elif level > 100:
            level = 100
        
        try:
            sbc.set_brightness(level)
            return get_brightness_response("set", level=level)
        except Exception as e:
            return f"Error setting brightness: {str(e)}"
    
    def _change_brightness(self, change_amount):
        """Increase or decrease brightness by a given amount"""
        try:
            current_level = self._get_current_brightness()
            new_level = current_level + change_amount

            self._set_brightness(new_level)
            action = "increase" if change_amount > 0 else "decrease"
            change_amount_abs = abs(change_amount)
            return get_brightness_response(action, level=new_level, amount=change_amount_abs)
        except Exception as e:
            return f"Error changing brightness: {str(e)}"
    
    def _get_current_brightness(self):
        """Get the current brightness level (0-100)"""
        try:
            current_brightness = sbc.get_brightness()[0]
            return current_brightness
        except Exception as e:
            print(f"Error getting current brightness: {str(e)}")
            return 50  # Default fallback

# Initialize system control
system_control = SystemControl()

def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editior = 'notepad.exe'
        subprocess.Popen([default_text_editior, File])

    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=SystemChatBot + messages,
            max_tokens=2048,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None,
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        messages.append({"role": "assistant", "content": Answer})
        return Answer

    Topic: str = Topic.replace("Content ", "")
    ContentByAI = ContentWriterAI(Topic)

    with open(rf"Data\{Topic.lower().replace(' ', '')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI)

    OpenNotepad(rf"Data\{Topic.lower().replace(' ', '')}.txt")
    return True

def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"
    webbrowser.open(Url4Search)
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True

    except:
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.find_all('a', {'jsname': 'UWckNb'})
            return [link.get('href') for link in links]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrieve search results.")
            return None

        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True

def CloseApp(app):
    if "chrome" in app:
        pass
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            return True
        except:
            return False

def System(command):
    """
    Enhanced system control function to handle volume, brightness, and battery commands
    """
    # Legacy commands
    if command == "mute":
        keyboard.press_and_release('volume mute')
        return "System muted."
    elif command == "unmute":
        keyboard.press_and_release('volume mute')
        return "System unmuted."
    elif command == "volume up":
        keyboard.press_and_release('volume up')
        return "Volume increased."
    elif command == "volume down":
        keyboard.press_and_release('volume down')
        return "Volume decreased."
    elif command == "shutdown":
        os.system("shutdown /s /t 1")
        return "Shutting down system."
    elif command == "restart":
        os.system("shutdown /r /t 1")
        return "Restarting system."
    elif command == "sleep":
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        return "Putting system to sleep."
    
    # New enhanced commands
    
    # Volume control with specific levels
    elif "set volume to" in command.lower() or "increase volume by" in command.lower() or "decrease volume by" in command.lower():
        return system_control.control_volume(command)
    
    # Brightness control
    elif "set brightness to" in command.lower() or "increase brightness by" in command.lower() or "decrease brightness by" in command.lower():
        return system_control.control_brightness(command)
    
    # Battery check
    elif command.lower() in ["battery", "check battery", "battery status", "battery level", "power level", "power status"]:
        return system_control.check_battery()
    
    # Default fallback
    else:
        return f"System command '{command}' not recognized."

async def TranslateAndExecute(commands: list[str]):
    funcs = []
    responses = []
    for command in commands:
        # Check if this is a task execution command
        task_response = handle_task_command(command)
        if task_response:
            responses.append(task_response)
            continue  # Skip to the next command
            
        # Original logic continues below...
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)

    for command in commands:
        if command.startswith("open "):
            fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
            funcs.append(fun)

        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)

        elif command.startswith("content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)

        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YoutubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)

        elif command.startswith("system "):
            # Handle system commands with responses
            system_cmd = command.removeprefix("system ")
            response = System(system_cmd)
            responses.append(response)
            # No need to add to funcs for immediate responses
        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)

    # First yield any immediate responses from system commands
    for response in responses:
        yield response
    
    # Then yield results from async functions
    for result in results:
        if isinstance(result, str):
            yield result
        else:
            yield result

async def Automation(command: list[str]):
    responses = []
    async for result in TranslateAndExecute(command):
        if isinstance(result, str) and result:  # Only collect non-empty string responses
            responses.append(result)
    
    # Return a combined response if we have any
    if responses:
        return " ".join(responses)
    return True

if __name__ == "__main__":
    # Test the system control functions
    response = System("battery")
    print(response)
    
    # To test other functions, uncomment the appropriate line
    # print(System("set volume to 50"))
    # print(System("increase volume by 10"))
    # print(System("decrease volume by 5"))
    # print(System("set brightness to 70"))