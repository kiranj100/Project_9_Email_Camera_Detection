import smtplib
import ssl
import imghdr
from email.message import EmailMessage

SENDER = "kiranjojan455@gmail.com"
PASSWORD = "jfkwrmbdlrgfumdb"
RECEIVER = "kiranjojan455@gmail.com"


def send_mail(image_path):
    print("Mail Send Successfully")

    email_message = EmailMessage()
    email_message["Subject"] = "New Customer Showed Up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        context = file.read()

    email_message.add_attachment(context, maintype="image",
                                 subtype=imghdr.what(None, context))

    email_server = smtplib.SMTP("smtp.gmail.com", 587)
    email_server.ehlo()
    email_server.starttls()
    email_server.login(SENDER, PASSWORD)
    email_server.sendmail(SENDER,RECEIVER, email_message.as_string())
    email_server.quit()


if __name__ == "__main__":
    send_mail(image_path="images")