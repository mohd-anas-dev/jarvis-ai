# Option 1: Move the search prompts to a new file
# Create a new file called search_prompts.py in the Backend folder

# In search_prompts.py:
import random

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
        # ... rest of simple prompts ...
    ]
    
    # Complex prompts for deeper searches
    complex_prompts = [
        "Initiating an extended search protocol now, Sir.",
        "Accessing global datasets for that, please hold.",
        # ... rest of complex prompts ...
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