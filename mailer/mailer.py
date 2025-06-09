import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

myEmail = "ausama.bese22seecs@seecs.edu.pk"
myPassword = "hkjtsptwlxnwtbrr"  # Use app-specific password for Gmail

smtp_server = "smtp.gmail.com"
smtp_port = 587

# Create the multipart message
msg = MIMEMultipart()
msg['Subject'] = 'Test Email with PDF Attachment'
msg['From'] = myEmail
msg['To'] = "demo.abdullah.dev@gmail.com"

# Attach the body text
body = "This is a test email from Python script with PDF attachment."
msg.attach(MIMEText(body, 'plain'))

# Attach the PDF file
filename = "attention_transfomer.pdf"
with open(filename, "rb") as f:
    part = MIMEApplication(f.read(), _subtype="pdf")
    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
    msg.attach(part)

# Connect to SMTP server and send email
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(myEmail, myPassword)
server.sendmail(myEmail, msg['To'], msg.as_string())
server.quit()
