import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP server configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587

# Sender and recipient information
sender_email = "arturylab@gmail.com"
sender_password = "*** *** *** ***"
recipient_email = "arturylab@gmail.com"

# Email content
subject = "Test email from Python"
body = "Hello from Python!"

# Create the email message
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = recipient_email
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login(sender_email, sender_password)  # Log in to the server
    server.sendmail(sender_email, recipient_email, message.as_string())  # Send the email
    print("Email sent successfully!")
except Exception as e:
    # Print any error messages to stdout
    print(f"Error: {e}")
finally:
    # Close the connection to the SMTP server
    server.quit()