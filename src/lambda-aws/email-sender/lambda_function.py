import json
import smtplib
import os 
from email.message import EmailMessage


def handler(event, context):
    """
    Main Lambda handler function
    Parameters:
        event: Dict containing the Lambda function event data
        context: Lambda runtime context
    Returns:
        Dict containing status message
    """
    try:
        user_email = event.get("email")
        msg = EmailMessage()
        msg.set_content('Hello, Congrats you successfully signed!')
        msg['Subject'] = user_email
        msg['From'] = os.environ["FROM_EMAIL"]
        msg['To'] = user_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ["FROM_EMAIL"], os.environ["APP_PASSWORD"])
            smtp.send_message(msg)

        return {"success": True}

    except Exception as err:
        raise 
