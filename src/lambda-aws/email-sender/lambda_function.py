import json
import smtplib
import os
from email.message import EmailMessage


def handler(event, context):
    """
    Lambda function to process SNS events and send email notifications.
    """
    try:
        for record in event.get("Records", []):
            sns_message = record["Sns"]["Message"]
            message_dict = json.loads(sns_message)

            user_email = message_dict.get("email")

            if not user_email:
                continue  # or log error if needed

            msg = EmailMessage()
            msg.set_content('Hello, Congrats you successfully signed up!')
            msg['Subject'] = "Welcome to our platform!"
            msg['From'] = os.environ["FROM_EMAIL"]
            msg['To'] = user_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(os.environ["FROM_EMAIL"], os.environ["APP_PASSWORD"])
                smtp.send_message(msg)

        return {"success": True}

    except Exception as err:
        print(f"Error processing event: {err}")
        raise
