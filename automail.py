import yagmail
import os
import datetime
from PIL import Image

def send_automail(message):
    # Example logic to send an email
    print(f"Sending email with message: {message}")
    # Implement actual email sending logic here

    # Get today's date
    date = datetime.date.today().strftime("%B %d, %Y")

    # Change directory to 'Attendance' and get the newest file
    path = 'Attendance'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    filename = newest

    # Read the HTML template
    template_path = '../template.html'  # Adjust this path if template.html is in a different directory
    with open(template_path, 'r') as file:
        template = file.read()

    # Prompt user for the recipient email address
    recipient_email = input("Enter the recipient email address: ")

    # Prompt user for the email subject
    subject = input("Enter the email subject: ")

    # Prompt user for the email body
    body_text = input("Enter the email body: ")

    # Replace placeholders with actual values
    body_html = template.replace('{{date}}', date).replace('{{body}}', body_text)

    # Resize the logo
    logo_path = '../logo.png'  # Original logo path
    width = 150  # Desired width
    logo = Image.open(logo_path)
    aspect_ratio = logo.width / logo.height
    height = int(width / aspect_ratio)  # Maintain aspect ratio
    logo_resized = logo.resize((width, height), Image.Resampling.LANCZOS)
    resized_logo_path = '../logo_resized.png'  # Path for resized logo
    logo_resized.save(resized_logo_path)

    # Setup Yagmail with OAuth2 or normal SMTP
    yag = yagmail.SMTP("finixiaglobal@gmail.com", "kgid llmv lyoe rhvg")

    # Send the mail
    try:
        yag.send(
            to=recipient_email,  # User input email address
            subject=subject,  # User input email subject
            contents=[
                body_html, 
                yagmail.inline(resized_logo_path)
            ],  # Email body in HTML with embedded logo
            attachments=[filename]  # File attached
        )
        print("Heyy buddy, Email Sent successfully!!")
    except Exception as e:
        print(f"Failed to send email: {e}")
