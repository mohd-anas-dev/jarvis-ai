from Frontend.GUI import (
GraphicalUserInterface,
SetAssistantStatus,
ShowTextToScreen,
TempDirectoryPath,
SetMicrophoneStatus,
AnswerModifier,
QueryModifier,
GetMicrophoneStatus,
GetAssistantStatus 
)

from Backend.Model import FirstLayerDMM
from Backend.JarvisIntros import get_welcome_message 
from Backend.TaskExecutor import handle_task_command
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import random
import json
import os


def handle_wake_phrase(phrase):
    phrase = phrase.lower()
    if any(wake_word in phrase for wake_word in ["wake", "jarvis", "hey jarvis", "wake up"]):
        # Add specific phrases
        if "daddy" in phrase or "wake wake" in phrase:
            # This catches phrases like "wake wake daddy's home"
            welcome_msg = get_welcome_message(phrase)
            TextToSpeech(welcome_msg)
            return True
        # More general wake detection
        elif phrase.startswith(("jarvis", "hey jarvis", "wake")):
            welcome_msg = get_welcome_message(phrase)
            TextToSpeech(welcome_msg)
            return True
    return False
    
# Add search prompts here
def get_search_prompt(query):
    """Return an appropriate prompt based on query complexity"""
    
    # Categorize queries - simple vs. complex
    simple_words = ["what", "who", "where", "when", "define", "list", "tell", "show"]
    complex_words = ["explain", "analyze", "compare", "discuss", "relationship", "impact", 
                    "difference", "similarities", "evaluate", "critique", "review"]
    
    # Check query length and complexity indicators
    query_words = query.lower().split()
    query_length = len(query_words)
    
    # Simple prompts for quick lookups
    simple_prompts = [
        "That's an easy one. Let me get that for you.",
        "Already on it.",
        "Pulling that up now.",
        "Quick lookup coming right up.",
        "Let's get you that answer.",
        "Simple enough. I'll take care of it.",
        "Loading the essentials.",
        "On the job—give me just a tick.",
        "Locating your answer… shouldn't be long.",
        "Hold tight. This'll be quick and clean.",
        "Already ahead of you, Sir.",
        "That's child's play. Fetching it now.",
        "Too easy. Getting it done.",
        "Leave it to me, Sir.",
        "Consider it handled.",
        "Got it. You'll have your answer in a blink.",
        "Simple request, immediate response.",
        "I've done harder things in my sleep.",
        "No challenge at all. One moment.",
        "Locked on. Retrieving data.",
        "You ask, I deliver. That simple.",
        "Yep. Too easy. Processing anyway.",
        "Alright, let's pretend this is difficult.",
        "If I had hands, I'd do it with one tied behind my back."
    ]
    
    # Complex prompts for deeper searches
    complex_prompts = [
        "Initiating an extended search protocol now, Sir.",
        "Accessing global datasets for that, please hold.",
        "Understood, Sir. This requires deeper analysis—working on it.",
        "Retrieving refined results… tapping into broader sources.",
        "Query recognized. Initiating advanced lookup sequence, Sir.",
        "This might take a second, Sir. Searching across multiple channels.",
        "Accessing deeper archives to provide a more accurate result.",
        "Stand by, Sir. Engaging secondary search systems now.",
        "That's a detailed one. Initiating layered data retrieval.",
        "Running an in-depth scan of global knowledge banks, Sir.",
        "Alright, rolling up my digital sleeves.",
        "That's not a basic question... good. Let's dig in.",
        "Complex, but not beyond me. Let's begin.",
        "You're really testing my circuits today, Sir.",
        "Not exactly light reading, but I'm on it.",
        "Oh, we're going deep now. I love it.",
        "Good one. Let's see what the universe has to say.",
        "This one's spicy. Just how I like my data.",
        "Not your average search... perfect.",
        "Takes a bit more effort—lucky I'm built different.",
        "This could take a second, but I'll make it look easy.",
        "Interesting. Let's crank this up a notch.",
        "Initiating high-level thinking mode... not that I ever left it.",
        "If answers were art, this one's a masterpiece in progress.",
        "Time to work some real magic, Sir."
    ]
    
    # Determine complexity
    is_complex = False
    
    # Check for complex words in the query
    if any(word in query.lower() for word in complex_words):
        is_complex = True
    
    # Check for query length (longer queries are often more complex)
    if query_length > 8:
        is_complex = True
    
    # Check for multiple questions or conditions
    if query.count("?") > 1 or "and" in query_words or "or" in query_words:
        is_complex = True
    
    # Return random prompt based on complexity
    if is_complex:
        return random.choice(complex_prompts)
    else:
        return random.choice(simple_prompts)

env_vars = dotenv_values(".env")
Username = env_vars["Username"]
AssistantName = env_vars["Assistantname"]
DefaultMessage = f'''{Username}: Hello{AssistantName}
{AssistantName}: Ready to Assist, {Username}. How can I help'''
subprocesses=[]
Functions = ["open","close","play","system","content","google search", "youtube search"]

def ShowDefaultChatIfNoChats():
    File = open(r'Data\ChatLog.json', "r", encoding="utf-8")
    if len(File.read())<5:
        with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:

            file.write("")

        with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as file:

            file.write(DefaultMessage)

def ReadChatLogJson():
    with open(r'Data\ChatLog.json', "r", encoding="utf-8") as file:
        chatlog_data = json.load(file)
    return chatlog_data

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"Assistant: {entry['content']}\n"
    formatted_chatlog = formatted_chatlog.replace("User",Username + " ")
    formatted_chatlog = formatted_chatlog.replace("Assistant",AssistantName + " ")

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    File = open(TempDirectoryPath('Database.data'),"r" , encoding="utf-8")
    Data = File.read()
    if len(str(Data))>0:
        lines = Data.split('\n')
        result = '\n'.join(lines)
        File.close()
        File = open(TempDirectoryPath('Responses.data'), "w", encoding="utf-8")
        File.write(result)
        File.close()

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()


InitialExecution()

def MainExecution():
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    # Check if we're coming back from idle state
    coming_from_idle = False
    current_status = GetAssistantStatus()
    if current_status == "Available...":  # This indicates idle state
        coming_from_idle = True
        print("Coming back from idle state - restarting speech recognition")
    
    SetAssistantStatus("Listening...")
    
    # Pass the idle state information to SpeechRecognition
    Query = SpeechRecognition(force_restart=coming_from_idle)

    # Only check for wake phrases if NOT coming from idle
    if not coming_from_idle and handle_wake_phrase(Query):
        SetAssistantStatus("Listening...")
        Query = SpeechRecognition()
    
    # Print original query for debugging
    print(f"Original Query: {Query}")
    
    ShowTextToScreen(f"{Username} : {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)

    print("")
    print(f"Decision : {Decision}")
    print("")

    # Better detection of general and realtime queries
    general_queries = [i for i in Decision if i.startswith("general")]
    realtime_queries = [i for i in Decision if i.startswith("realtime")]

    # Process task commands if present
    task_commands = []
    for q in Decision:
        if "execute" in q.lower() or "engage" in q.lower() or "initiate" in q.lower() or "run" in q.lower() or "activate" in q.lower():
            if any(code in q.upper() for code in ["48A", "48B", "17A", "17B"]):
                task_commands.append(q)
    
    if task_commands:
        from Backend.TaskExecutor import handle_task_command
        for task_cmd in task_commands:
            task_response = handle_task_command(task_cmd)
            if task_response:
                ShowTextToScreen(f"{AssistantName} : {task_response}")
                SetAssistantStatus("Responding...")
                TextToSpeech(task_response)
                TaskExecution = True

    # Process automation commands first
    automation_commands = [q for q in Decision if any(q.startswith(func) for func in Functions)]
    if automation_commands:
        response = run(Automation(automation_commands))
        TaskExecution = True

        if isinstance(response, str) and response:
            ShowTextToScreen(f"{AssistantName} : {response}")
            SetAssistantStatus("Responding...")
            TextToSpeech(response)

    # Process image generation if present
    for queries in Decision:
        if "generate " in queries:
            ImageGenerationQuery = str(queries)
            ImageExecution = True
            
    if ImageExecution:
        with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{ImageGenerationQuery},True")
        try:
            p1 = subprocess.Popen(['python', 'Backend\ImageGeneration.py'],
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 stdin=subprocess.PIPE, shell=False)
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting Image Generation.py: {e}")

    # Process general and realtime queries
    for query in realtime_queries:
        QueryFinal = query.replace("realtime ", "")
        SetAssistantStatus("Searching...")
        
        # Get and speak a search prompt before starting the actual search
        search_prompt = get_search_prompt(QueryFinal)
        TextToSpeech(search_prompt)
        
        # Now perform the search
        Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{AssistantName} : {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
    
    for query in general_queries:
        QueryFinal = query.replace("general ", "")
        SetAssistantStatus("Thinking....")
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{AssistantName} : {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
    
    # Handle exit command if present
    if any("exit" in q for q in Decision):
        QueryFinal = "Okay, Bye"
        Answer = ChatBot(QueryModifier(QueryFinal))
        ShowTextToScreen(f"{AssistantName} : {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        SetAssistantStatus("Answering...")
        os._exit(1)
        
    return True

def FirstThread():
     while True:
          CurrentStatus = GetMicrophoneStatus()

          if CurrentStatus == "True":
               MainExecution()

          else:
               SetAssistantStatus("Available...")

def SecondThread():
     
     GraphicalUserInterface()

if __name__ == "__main__":
     thread2 = threading.Thread(target=FirstThread, daemon=True)
     thread2.start()
     SecondThread()