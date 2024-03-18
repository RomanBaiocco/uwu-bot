import json

# Function to log messages in JSON format
def log_message(level, message, **kwargs):
    log_entry = json.dumps({
        "level": level.upper(),
        "message": message,
        **kwargs
    })
    print(log_entry)