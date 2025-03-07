import subprocess


def add_reminder(title, list_name = "Compras"):
    script = f"""
    tell application "Reminders"
        tell list "{list_name}"
            make new reminder with properties {{name:"{title}"}}
        end tell
    end tell
    """
    subprocess.run(["osascript", "-e", script])
    print(f"Reminder '{title}' added to list '{list_name}'.")


def delete_reminder(title, list_name = "Compras"):
    script = f"""
    tell application "Reminders"
        tell list "{list_name}"
            delete (first reminder whose name is "{title}")
        end tell
    end tell
    """
    subprocess.run(["osascript", "-e", script])
    print(f"Reminder '{title}' deleted from list '{list_name}'.")


delete_reminder("Leche 🥛")
