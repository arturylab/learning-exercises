import subprocess


def send_notes(content):
    """
    Send the content to the macOS Notes app using AppleScript.
    """
    apple_script = f"""
    tell application "Notes"
        make new note at folder "Python" with properties {{name:"Hello World Note", body:"{content}"}}
    end tell
    """
    try:
        subprocess.run(["osascript", "-e", apple_script], check=True)
        print("Note sent successfully")
    except subprocess.CalledProcessError as e:
        print("Error sending note:", e)
    

send_notes("Hello, this is a SECOND test note from Python!")