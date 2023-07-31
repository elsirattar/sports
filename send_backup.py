from backup import ExportAll
import json
from cryptography.fernet import Fernet
import smtplib,ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class SendBackup:
    def __init__(self):
        ExportAll()
        self.send_data()

    def send_data(self) -> object:
        key = b'uz74glQVUR4G09H98aXDpcTliuZ1eNp2FQrPXAM0MYM='
        fernet = Fernet(key)
        with open('mail_data.json', 'rb') as file:
            original = file.read()
        decrypted = fernet.decrypt(original)
        conf = json.loads(decrypted)
        print(conf)
        sender = conf['mail']
        password = conf['password']
        receivers = 'aalattar95@gmail.com'

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "نسخة من النظام"
        msg["From"] = sender
        msg["To"] = receivers
        filename = "backup.xlsx"

        # HTML Message Part
        html = """\
        <html>
            <body>
            <h1>أوج لحلول الأعمال</h1>
            <br>
            <h2>
               Click on <a href="https://fb.com/awgsolutions">Awg for Business solutions</a> 
               for contact with us.
            
            </h2>
          </body>
        </html>
        """

        part = MIMEText(html, "html")
        msg.attach(part)

        # Add Attachment
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        encoders.encode_base64(part)

        # Set mail headers
        part.add_header(
            "Content-Disposition",
            "attachment", filename=filename
        )
        msg.attach(part)

        # Create secure SMTP connection and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender, password)
            server.sendmail(
                sender, receivers, msg.as_string()
            )

        print('sent to '+ receivers)


if __name__ == '__main__':
    SendBackup()
