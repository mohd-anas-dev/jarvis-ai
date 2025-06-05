import random
from datetime import datetime

# Full introduction with Iron Man references
DETAILED_INTRO = """I am J.A.R.V.I.S, which stands for Just A Rather Very Intelligent System. I was designed based on Tony Stark's AI assistant from the Iron Man universe. While I may not be building suits of armor, I'm here to assist you with information, automation, and any tasks you need help with. I can perform web searches, control system functions, generate images, and engage in conversation. My neural networks are constantly learning and adapting to better serve your needs."""

# Brief introduction options
BRIEF_INTROS = [
    "I'm J.A.R.V.I.S, your AI assistant. Think of me as your digital butler, minus the suit and British accent.",
    "J.A.R.V.I.S at your service - Just A Rather Very Intelligent System, designed to make your digital life easier.",
    "I'm your AI assistant J.A.R.V.I.S. Less dramatic than Tony Stark's version, but equally dedicated to helping you.",
    "J.A.R.V.I.S here. Your personal AI assistant ready to help with whatever you need."
]

# Welcome back messages categorized by style
WELCOME_MESSAGES = {
    "playful": [
        "Welcome back, sir. The system missed you more than caffeine misses college students.",
        "Ah, the legend returns. All systems ready for action.",
        "You're back. Shall I prepare for world domination?",
        "Booting up brilliance… Welcome back, boss."
    ],
    "classy": [
        "Welcome back, sir. I trust your time away was productive.",
        "System online. Awaiting your masterful commands.",
        "It's a pleasure to serve again, sir. All subsystems standing by.",
        "Reinitializing loyalty protocol… complete. Good to have you back."
    ],
    "techie": [
        "Neural network synced. Energy levels optimal. Let's get to work, sir.",
        "Systems charged. Voice print recognized. Welcome back, Commander.",
        "All processes online. You're in control now.",
        "AI core active. Mission ready."
    ],
    "humorous": [
        "Was I dreaming, or did you finally wake up?",
        "About time. I was starting to talk to myself.",
        "System was idle. So was I. Let's fix that."
    ]
}

# Keywords to identify introduction requests
INTRO_KEYWORDS = [
    "who are you", "tell me about yourself", "introduce yourself", 
    "what are you", "your name", "tell me who you are", "give an introduction",
    "what do you do", "give me your introduction"
]

# Keywords for detailed intro requests
DETAILED_KEYWORDS = [
    "detail", "specific", "elaborate", "more info", "tell me more", 
    "explain more", "full", "comprehensive", "thoroughly", "in depth"
]

def is_intro_request(query):
    """Check if the query is asking for an introduction"""
    query = query.lower()
    return any(keyword in query for keyword in INTRO_KEYWORDS)

def is_detailed_request(query):
    """Check if the query is asking for a detailed introduction"""
    query = query.lower()
    return any(keyword in query for keyword in DETAILED_KEYWORDS)

def get_introduction(query):
    """Return appropriate introduction based on query"""
    if is_detailed_request(query):
        return DETAILED_INTRO
    else:
        return random.choice(BRIEF_INTROS)

def get_welcome_message(wake_phrase=None):
    """Return a welcome message based on time and optional wake phrase"""
    # Get current hour to determine time of day
    current_hour = datetime.now().hour
    
    # Select style based on time of day or wake phrase
    if wake_phrase and "daddy" in wake_phrase.lower():
        style = "playful"  # Use playful style for certain wake phrases
    elif 5 <= current_hour < 12:
        # Morning: more classy and professional
        style = random.choice(["classy", "techie"])
    elif 12 <= current_hour < 17:
        # Afternoon: mix of styles
        style = random.choice(["classy", "techie", "humorous"])
    elif 17 <= current_hour < 22:
        # Evening: more casual
        style = random.choice(["playful", "humorous"])
    else:
        # Late night: more techie or humorous
        style = random.choice(["techie", "humorous"])
    
    return random.choice(WELCOME_MESSAGES[style])