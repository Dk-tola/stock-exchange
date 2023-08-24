# https://realpython.com/python-send-email/

from email import message
import smtplib
import ssl
import random
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def authentication(email):
    codeGenerator = ""
    for i in range(0, 6):
        number = random.randint(0, 9)
        codeGenerator += str(number)

    verificationCode = str(codeGenerator)
    print(verificationCode)
    # Send the verification code

    smtp_server = "smtp-mail.outlook.com"
    port = 587  # For starttls
    sender_email = "group16stock@Outlook.com"
    receiver_email = email
    password = "YashMVP16"

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)

        # TODO: Send email here
        message = MIMEMultipart("alternative")
        message[
            "Subject"
        ] = "Bully Stock Exchange Website - Two Factor Authentification"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        How are you? I AM IN THE TEXT
        Real Python has many great tutorials:
        www.realpython.com"""
        html = """\
        <html>
            <body>
            <p>Hello,<br><br>
                Your security code is:<br>
                {}<br><br>
                The code expires in 60 seconds. Do not share this code with anyone.<br>
                If you are not expecting this email, please change your password immediately.<br><br>
                Contact us:
                <a href="mailto:group16stock@Outlook.com">group16stock@Outlook.com</a>
            </p>
            </body>
        </html>
        """.format(
            verificationCode
        )

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("EMAIL SENT")
    except Exception as error:
        # Print any error messages to stdout
        print("ERROR:")
        print(error)
        print("---------------------------")
    finally:
        print("COMPLETE")
        try:
            server.quit()  # Just in case error and still logged into server
        except Exception as e:
            return

    return str(verificationCode)
