import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email():
    # Email credentials
    from_address = "mano.robotinskis@gmail.com"
    to_address = "virtualeventassistant@gmail.com"
    password = "uiwu ncpq zgvn getc"

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Scraper Results"

    # Email body
    body = "Please find the attached scraper results file."

    # Attach the body to the email
    msg.attach(MIMEText(body, 'plain'))

    # Attach the results.html file
    filename = "results.html"
    with open(filename, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f"attachment; filename={filename}")

    msg.attach(part)

    # Set up the SMTP server and send the email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Using Gmail's SMTP server
        server.starttls()  # Secure the connection
        server.login(from_address, password)
        server.sendmail(from_address, to_address, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
