import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(msg):
    # Email configuration
    sender_email = "imvelaga@gmail.com"
    receiver_email = ["shankar.velaga@gmail.com"]
    #receiver_email = ["shankar.velaga@gmail.com", "usvelaga@gmail.com"]
    #https://myaccount.google.com/apppasswords
    password = "zlrp nktq tpcr llvf"

    # Create a message object
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)
    message["Subject"] = "Python sent you an email"

    # Add body to email
    body_cons = "Hello, Python message: "+str(msg)
    body = body_cons
    message.attach(MIMEText(body, "plain"))

    # Establish a secure SMTP connection
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        # Login to the email server
        server.login(sender_email, password)
        # Send the email
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully!")