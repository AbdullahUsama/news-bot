import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# ==== CONFIGURATION ====
myEmail = os.environ.get("EMAIL_ADDRESS")
myPassword = os.environ.get("EMAIL_PASSWORD")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

prompt = "Explain the basics of attention mechanism in transformers."

# ==== GENERATE TEXT FROM GEMINI ====
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content(prompt)

gemini_text = response.text.strip()

# ==== EMAIL SETUP ====
smtp_server = "smtp.gmail.com"
smtp_port = 587

msg = MIMEMultipart()
msg['Subject'] = 'Gemini API Response'
msg['From'] = myEmail
msg['To'] = "demo.abdullah.dev@gmail.com"

body = f"Prompt:\n{prompt}\n\nGemini's Response:\n{gemini_text}"
msg.attach(MIMEText(body, 'plain'))

# ==== SEND EMAIL ====
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(myEmail, myPassword)
server.sendmail(myEmail, msg['To'], msg.as_string())
server.quit()

print("Email sent successfully.")
