from flask_mail import Message

### class for Email controling
class EmailControl:
    def __init__(self, mail):
        self.mail = mail

    def send_email(self, sender, recipients, subject, content, html=None):
        msg = Message(subject,
                      sender=sender,
                      recipients=recipients,
                      body=content,
                      html=html)
        self.mail.send(msg)
