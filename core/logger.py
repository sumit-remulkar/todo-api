import datetime

def log(message):

    timestamp = datetime.datetime.now().strftime("%H:%M:%S")

    print(f"[{timestamp}] {message}")

def log(agent, message):

    print(f"[{agent}] {message}")