import random

# Volume control response prompts
volume_responses = {
    "set": [
        "Volume has been set to {level} percent, Sir.",
        "I've adjusted the volume to {level} percent, Sir.",
        "Audio is now at {level} percent, as requested.",
        "Volume level is now {level} percent, Sir.",
        "I've set the system volume to {level} percent.",
        "Volume adjusted to {level} percent. Is that satisfactory, Sir?",
        "System volume is now at {level} percent.",
        "Done. Volume is now {level} percent, Sir.",
        "Volume level {level} percent achieved, Sir.",
        "Audio output adjusted to {level} percent as directed."
    ],
    "increase": [
        "Volume increased by {amount} percent, now at {level} percent.",
        "I've raised the volume by {amount} percent. Current level: {level} percent.",
        "Audio is now louder by {amount} percent, bringing us to {level} percent.",
        "Volume up by {amount} percent, Sir. Now at {level} percent total.",
        "I've increased the volume as requested. Now at {level} percent.",
        "Volume has been amplified by {amount} percent to {level} percent total.",
        "Audio levels increased by {amount}. New volume: {level} percent.",
        "Volume adjustment complete: {amount} percent increase to {level} percent total.",
        "I've turned it up by {amount} percent. Current volume is {level} percent.",
        "Audio output increased by {amount} percent as requested. Now at {level} percent."
    ],
    "decrease": [
        "Volume reduced by {amount} percent, now at {level} percent.",
        "I've lowered the volume by {amount} percent. Current level: {level} percent.",
        "Audio is now quieter by {amount} percent, bringing us to {level} percent.",
        "Volume down by {amount} percent, Sir. Now at {level} percent total.",
        "I've decreased the volume as requested. Now at {level} percent.",
        "Volume has been reduced by {amount} percent to {level} percent total.",
        "Audio levels decreased by {amount}. New volume: {level} percent.",
        "Volume adjustment complete: {amount} percent decrease to {level} percent total.",
        "I've turned it down by {amount} percent. Current volume is {level} percent.",
        "Audio output decreased by {amount} percent as requested. Now at {level} percent."
    ]
}

# Brightness control response prompts
brightness_responses = {
    "set": [
        "Brightness has been set to {level} percent, Sir.",
        "I've adjusted the brightness to {level} percent, Sir.",
        "Screen brightness is now at {level} percent, as requested.",
        "Brightness level is now {level} percent, Sir.",
        "I've set the system brightness to {level} percent.",
        "Brightness adjusted to {level} percent. Is that comfortable for your eyes, Sir?",
        "System brightness is now at {level} percent.",
        "Done. Brightness is now {level} percent, Sir.",
        "Brightness level {level} percent achieved, Sir.",
        "Display brightness adjusted to {level} percent as directed."
    ],
    "increase": [
        "Brightness increased by {amount} percent, now at {level} percent.",
        "I've raised the brightness by {amount} percent. Current level: {level} percent.",
        "Screen is now brighter by {amount} percent, bringing us to {level} percent.",
        "Brightness up by {amount} percent, Sir. Now at {level} percent total.",
        "I've increased the brightness as requested. Now at {level} percent.",
        "Brightness has been amplified by {amount} percent to {level} percent total.",
        "Display brightness increased by {amount}. New level: {level} percent.",
        "Brightness adjustment complete: {amount} percent increase to {level} percent total.",
        "I've brightened it by {amount} percent. Current brightness is {level} percent.",
        "Screen brightness increased by {amount} percent as requested. Now at {level} percent."
    ],
    "decrease": [
        "Brightness reduced by {amount} percent, now at {level} percent.",
        "I've lowered the brightness by {amount} percent. Current level: {level} percent.",
        "Screen is now dimmer by {amount} percent, bringing us to {level} percent.",
        "Brightness down by {amount} percent, Sir. Now at {level} percent total.",
        "I've decreased the brightness as requested. Now at {level} percent.",
        "Brightness has been reduced by {amount} percent to {level} percent total.",
        "Display brightness decreased by {amount}. New level: {level} percent.",
        "Brightness adjustment complete: {amount} percent decrease to {level} percent total.",
        "I've dimmed it by {amount} percent. Current brightness is {level} percent.",
        "Screen brightness decreased by {amount} percent as requested. Now at {level} percent."
    ]
}

# Battery status messages
battery_messages = {
    "high": [
        "Battery is well charged and ready to go, Sir. Current level: {percent}%.",
        "Power levels are optimal at {percent}%. We're good to go.",
        "Battery is in good condition at {percent}%, no need to worry about charging.",
        "All charged up at {percent}% and ready for action, Sir.",
        "Power situation is looking good at {percent}%. We're set."
    ],
    "medium": [
        "Battery is at a moderate level of {percent}%.",
        "You still have a decent amount of power left at {percent}%.",
        "Battery is holding up fine for now at {percent}%.",
        "We're running on adequate power at {percent}%, Sir.",
        "Battery levels are acceptable at {percent}% for the moment."
    ],
    "low": [
        "Battery is getting low at {percent}%, might want to plug in soon.",
        "Power is running low at {percent}%, consider charging soon.",
        "Battery needs attention in the near future. Currently at {percent}%.",
        "I'd recommend finding a power source soon, Sir. Battery at {percent}%.",
        "We're running on limited power at {percent}%. Might be time to charge."
    ],
    "critical": [
        "Battery is critically low at {percent}%, please connect to power immediately.",
        "Power levels are dangerously low at {percent}%, charge now to avoid shutdown.",
        "Critical battery level detected: {percent}%. Urgent charging required.",
        "Sir, we need power now. System at {percent}%, shutdown is imminent.",
        "Emergency power situation at {percent}%. Please connect to a charger immediately."
    ],
    "charging": [
        "Battery is currently charging, power level at {percent}%.",
        "Power is being replenished. Current level: {percent}%.",
        "The battery is charging up nicely at {percent}%.",
        "We're plugged in and charging, Sir. Battery at {percent}%.",
        "Power levels are increasing. Currently at {percent}% and charging."
    ]
}

def get_volume_response(action, level=None, amount=None):
    """
    Get a random response for volume actions
    action: 'set', 'increase', or 'decrease'
    level: current volume level after change
    amount: amount changed (for increase/decrease)
    """
    if action not in volume_responses:
        return f"Volume {action}d."
    
    response = random.choice(volume_responses[action])
    
    if action == "set" and level is not None:
        return response.format(level=level)
    elif (action == "increase" or action == "decrease") and level is not None and amount is not None:
        return response.format(amount=amount, level=level)
    else:
        return f"Volume {action}d."

def get_brightness_response(action, level=None, amount=None):
    """
    Get a random response for brightness actions
    action: 'set', 'increase', or 'decrease'
    level: current brightness level after change
    amount: amount changed (for increase/decrease)
    """
    if action not in brightness_responses:
        return f"Brightness {action}d."
    
    response = random.choice(brightness_responses[action])
    
    if action == "set" and level is not None:
        return response.format(level=level)
    elif (action == "increase" or action == "decrease") and level is not None and amount is not None:
        return response.format(amount=amount, level=level)
    else:
        return f"Brightness {action}d."

def get_battery_response(percent, power_plugged=False, time_left=None):
    """
    Get a random response for battery status
    percent: battery percentage
    power_plugged: whether the device is plugged in
    time_left: estimated time left (string format)
    """
    # Determine status message category
    if power_plugged:
        status = "charging"
    elif percent >= 80:
        status = "high"
    elif 50 <= percent < 80:
        status = "medium"
    elif 20 <= percent < 50:
        status = "low"
    else:
        status = "critical"
    
    # Get a random message from the appropriate category
    message = random.choice(battery_messages[status]).format(percent=percent)
    
    # Add time information if available
    if time_left:
        if power_plugged:
            message += f" Approximately {time_left} until fully charged."
        else:
            message += f" Approximately {time_left} of battery life remaining."
            
    return message