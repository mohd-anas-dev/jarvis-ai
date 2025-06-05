from googlesearch import search
from groq import Groq
from json import load, dump
import datetime
import random
from dotenv import dotenv_values
from Backend.TextToSpeech import TTS  # Import the TTS function directly

env_vars = dotenv_values(".env")

Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide brief responses by default. Only give detailed answers when explicitly requested. ***
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

try:
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
except FileNotFoundError:
    with open(r"Data\ChatLog.json", "w") as f:
        dump([], f)

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

def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"

    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"

    Answer += "[end]"
    return Answer

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello Sir, How can i help you?"}
]

def information():
    data = ""
    current_data_time = datetime.datetime.now()
    day = current_data_time.strftime("%A")
    date = current_data_time.strftime("%d")
    month = current_data_time.strftime("%B")
    year = current_data_time.strftime("%Y")
    hour = current_data_time.strftime("%H")
    minute = current_data_time.strftime("%M")
    second = current_data_time.strftime("%S")
    data += f"Use This Real-time Information if needed:\n"
    data += f"Day: {day}\n"
    data += f"Date: {date}\n"
    data += f"Month: {month}\n"
    data += f"Year: {year}\n"
    data += f"Time: {hour} , {minute} , {second} .\n"
    return data

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages
    
    # Get and speak the appropriate search prompt
    search_prompt = get_search_prompt(prompt)
    # Use TTS directly for the search prompt - this will speak without adding to response
    TTS(search_prompt)
    
    with open(r"Data\ChatLog.json", "r") as f:
        messages = load(f)
    messages.append({"role": "user", "content": f"{prompt}"})

    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=SystemChatBot + [{"role": "system", "content": information()}] + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None,
    )

    Answer = ""

    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open(r"Data\ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer=Answer)

if __name__ == "__main__":
    while True:
        prompt = input("Enter your Query: ")
        print(RealtimeSearchEngine(prompt))