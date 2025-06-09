# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv
# load_dotenv()

# from scrapper import scrape_dawn_articles

# # ==== CONFIGURATION ====
# myEmail = os.environ.get("EMAIL_ADDRESS")
# myPassword = os.environ.get("EMAIL_PASSWORD")
# gemini_api_key = os.environ.get("GEMINI_API_KEY")

# prompt = "Explain the basics of attention mechanism in transformers."

# # ==== GENERATE TEXT FROM GEMINI ====
# genai.configure(api_key=gemini_api_key)

# model = genai.GenerativeModel("gemini-2.0-flash")
# response = model.generate_content(prompt)

# gemini_text = response.text.strip()

# # ==== EMAIL SETUP ====
# smtp_server = "smtp.gmail.com"
# smtp_port = 587

# msg = MIMEMultipart()
# msg['Subject'] = 'Gemini API Response'
# msg['From'] = myEmail
# msg['To'] = "demo.abdullah.dev@gmail.com"

# body = f"Prompt:\n{prompt}\n\nGemini's Response:\n{gemini_text}"
# msg.attach(MIMEText(body, 'plain'))

# # ==== SEND EMAIL ====
# server = smtplib.SMTP(smtp_server, smtp_port)
# server.starttls()
# server.login(myEmail, myPassword)
# server.sendmail(myEmail, msg['To'], msg.as_string())
# server.quit()

# print("Email sent successfully.")


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import google.generativeai as genai
import os
from dotenv import load_dotenv
from scrapper import scrape_dawn_articles
from datetime import datetime

load_dotenv()

# ==== CONFIGURATION ====
myEmail = os.environ.get("EMAIL_ADDRESS")
myPassword = os.environ.get("EMAIL_PASSWORD")
gemini_api_key = os.environ.get("GEMINI_API_KEY")

# ==== SETUP GEMINI ====
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# ==== SCRAPE ARTICLES ====
articles = scrape_dawn_articles()  # Uses today’s date by default

# ==== GENERATE PROMPT + GEMINI RESPONSES ====
email_body = ""

for article in articles:
    title = article["title"]
    content = article["content"]

    prompt = f"""
Read this article and provide two distinct lists based on its content, strictly following the format below:

1. Words: List all good vocabulary words from the article, along with a concise meaning for each. Format each entry as "word: meaning", and place each complete entry on a new line. Do not use any bullet points, dashes, or other special formatting. 
2. Phrases and Idioms: List different phrases and idioms found in the article, along with a concise meaning for each. Format each entry as "phrase: meaning", and place each complete entry on a new line. Do not use any bullet points, dashes, or other special formatting. 

Title: {title}
Content: {content}
""".strip()

    try:
        response = model.generate_content(prompt)
        gemini_text = response.text.strip()
    except Exception as e:
        gemini_text = f"Error generating response: {e}"

    # email_body += f"\n\n=== Article: {title} ===\n\nPrompt:\n{prompt}\n\nGemini's Response:\n{gemini_text}\n"
    email_body += f"\n\n=== Article: {title} ===\n\n{gemini_text}\n"

# ==== EMAIL SETUP ====
msg = MIMEMultipart()
msg['Subject'] = f"Gemini Vocabulary Report - {datetime.today().strftime('%Y-%m-%d')}"
msg['From'] = myEmail
msg['To'] = "demo.abdullah.dev@gmail.com"

msg.attach(MIMEText(email_body, 'plain'))

# ==== SEND EMAIL ====
smtp_server = "smtp.gmail.com"
smtp_port = 587

server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(myEmail, myPassword)
server.sendmail(myEmail, msg['To'], msg.as_string())
server.quit()

print("Email sent successfully.")
