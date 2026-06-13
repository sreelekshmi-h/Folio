import requests
import smtplib
from email.mime.text import MIMEText
import os

from datetime import date;
def get_weather(city="Thiruvananthapuram"):
    url=f"https://wttr.in/{city}?format=3"
    try:
        response=requests.get(url,timeout=10)
        response.raise_for_status()
        return response.text.strip()
    except Exception as e:
        return f"Weather not available ({e})"

def get_quote():
    url="https://zenquotes.io/api/random"
    try:
        response=requests.get(url,timeout=10);
        response.raise_for_status()
        data=response.json();
        quote=data[0]["q"]
        author=data[0]["a"]
        return f'"{quote}"  - {author}'
    
    except Exception as e:
        return f"Quote unavailable ({e})"



def get_history():
    today = date.today()

    url = (
        f"https://api.wikimedia.org/feed/v1/wikipedia/en/onthisday/events/"
        f"{today.month:02d}/{today.day:02d}"
    )

    try:
        response = requests.get(
            url,
            headers={"User-Agent": "Pulse/1.0"},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        event = data["events"][0]
        return f"{event['year']}: {event['text']}"

    except Exception as e:
        return f"History unavailable ({e})"



def build_summary():
    today=date.today().strftime("%A , %d %B %Y")
    weather=get_weather()
    quote=get_quote()
    history=get_history()
    summary=f"""
=============================
PULSE-Daily Summary 
{today}

WEATHER
{weather}
    
TODAY'S QUOTE
{quote}

HISTORICAL EVENT
{history}
    
=============================
"""

    return summary

def run():
    summary=build_summary()
    print(summary)
    with open("daily_summary.txt","w",encoding="utf-8") as f:
        f.write(summary)
    send_email(summary) 
    print("Pulse ran Successfully")

if __name__=="__main__":
    run()

def send_email(summary_text):
    sender=os.environ.get("EMAIL_SENDER")
    password=os.environ.get("EMAIL_PASSWORD")
    receiver=os.environ.get("EMAIL_RECEIVER")
    msg=MIMEText(summary_text)
    msg["Subject"]="Pulse-Daily Summary"
    msg["From"]=sender
    msg["To"]=receiver

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:
        server.login(sender,password)
        server.send_message(msg)
    print("Email Sent.")


