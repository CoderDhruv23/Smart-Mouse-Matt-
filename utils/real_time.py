from datetime import datetime

def get_real_time(query):
    query = query.lower()
    now = datetime.now()
    
    if "time" in query:
        return f"The current time is {now.strftime('%I:%M %p')}."
    elif "date" in query:
        return f"Today's date is {now.strftime('%B %d, %Y')}."
    elif "today" in query:
        return f"Today is {now.strftime('%A, %B %d, %Y')}."
    else:
        return None  # Let Gemini handle other queries