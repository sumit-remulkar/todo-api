import webbrowser
import time


def open_browser():

    print("\nOpening browser preview...")

    # thoda wait taki servers start ho jaye
    time.sleep(5)

    webbrowser.open("http://localhost:5173")