#!/usr/bin/env python3
"""
EXLONE – WhatsApp Appeal Bot (LEGITIMATE)
---------------------------------------
A Termux-friendly, GitHub-ready Python CLI tool that generates
professional WhatsApp appeal messages (NO spamming, NO automation abuse).
Author: EXLONE
Usage: python exlone_appeal_bot.py
"""

import webbrowser
import urllib.parse
import os
import json
import datetime
from textwrap import dedent

PROJECT_NAME = "exlone-appeal-bot"
DATA_DIR = "appeals"
LOG_FILE = os.path.join(DATA_DIR, "appeal_log.json")

WHATSAPP_SUPPORT = {
    "android": "https://www.whatsapp.com/contact/?subject=messenger",
    "ios": "https://www.whatsapp.com/contact/?subject=messenger"
}

# -------------------------------
# Tones and Explanations
# -------------------------------
TONE_TEXT = {
    "formal": {
        "temporary": (
            "My WhatsApp account was recently placed under a temporary restriction. "
            "I understand that automated systems help protect the platform, and I believe "
            "this restriction may have been triggered unintentionally. I use WhatsApp "
            "responsibly and respectfully, and I kindly request a review of my account."
        ),
        "permanent": (
            "My WhatsApp account appears to have been permanently banned. I respectfully "
            "request a careful review, as I have always aimed to comply with WhatsApp’s "
            "Terms of Service and policies. I would sincerely appreciate your reconsideration."
        )
    },
    "polite": {
        "temporary": (
            "My account was temporarily restricted, and I believe this may have occurred "
            "due to unusual activity or a system error. WhatsApp is important for my daily "
            "communication, and I kindly ask for a review and any guidance to avoid this again."
        ),
        "permanent": (
            "My account seems to have been permanently banned, and I am respectfully asking "
            "for a review. I genuinely believe this action was taken in error and I am fully "
            "willing to comply with all WhatsApp guidelines going forward."
        )
    },
    "very_polite": {
        "temporary": (
            "My WhatsApp account was recently restricted. I fully respect WhatsApp’s systems "
            "and community standards, and I believe this restriction may have been applied "
            "unintentionally. I kindly and humbly request a review of my account."
        ),
        "permanent": (
            "My WhatsApp account appears to have been permanently banned, and I am writing "
            "with utmost respect to request a careful review. I value WhatsApp greatly and "
            "have always tried to follow all policies. I would be sincerely grateful for your "
            "consideration and guidance."
        )
    }
}

def auto_explanation(appeal_type, tone):
    return TONE_TEXT[tone][appeal_type]

def generate_appeal(phone, platform, appeal_type, device, tone):
    explanation = auto_explanation(appeal_type, tone)
    message = dedent(f"""
    Hello WhatsApp Support Team,

    I am writing to respectfully request a review of my WhatsApp account associated with the phone number below.

    Phone Number: {phone}
    Platform: {platform.capitalize()}
    Device: {device}

    {explanation}

    I assure you that I will strictly comply with all WhatsApp policies and community guidelines going forward.

    Thank you very much for your time and consideration.

    Kind regards,
    EXLONE User
    """).strip()
    return message

DISCLAIMER = (
    "\nDISCLAIMER:\n"
    "This tool does NOT unban WhatsApp accounts automatically. "
    "It only helps generate professional appeal messages using "
    "official WhatsApp support channels. Spamming or misuse may "
    "result in permanent bans. Use responsibly.\n"
)

def ensure_storage():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

def save_log(entry):
    with open(LOG_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=4)

def export_to_txt(phone, appeal_text):
    filename = f"appeal_{phone.replace('+','')}.txt"
    with open(filename, "w") as f:
        f.write(appeal_text)
    return filename

def banner():
    print("=" * 65)
    print("   ███████╗██╗  ██╗██╗      ██████╗ ███╗   ██╗███████╗")
    print("   ██╔════╝╚██╗██╔╝██║     ██╔═══██╗████╗  ██║██╔════╝")
    print("   █████╗   ╚███╔╝ ██║     ██║   ██║██╔██╗ ██║█████╗  ")
    print("   ██╔══╝   ██╔██╗ ██║     ██║   ██║██║╚██╗██║██╔══╝  ")
    print("   ███████╗██╔╝ ██╗███████╗╚██████╔╝██║ ╚████║███████╗")
    print("   ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝")
    print("        LEGITIMATE WHATSAPP APPEAL BOT (PYTHON)")
    print("        No Spam • No Automation Abuse • Safe Use")
    print("=" * 65)

def main():
    ensure_storage()
    banner()
    print(DISCLAIMER)

    phone = input("Enter phone number (with country code): ").strip()

    print("\nSelect platform:")
    print("1. Android")
    print("2. iOS")
    platform_choice = input("> ").strip()
    platform = "android" if platform_choice == "1" else "ios"

    device = input("Enter device model (e.g. Samsung Galaxy A06): ").strip()

    print("\nSelect appeal type:")
    print("1. Temporary Ban Appeal")
    print("2. Permanent Ban Appeal")
    appeal_choice = input("> ").strip()
    appeal_type = "temporary" if appeal_choice == "1" else "permanent"

    print("\nSelect explanation tone:")
    print("1. Formal (recommended)")
    print("2. Polite")
    print("3. Very Polite")
    tone_choice = input("> ").strip()
    tone = {"1": "formal", "2": "polite", "3": "very_polite"}.get(tone_choice, "formal")

    print("\nPreview mode? (y/n)")
    preview = input("> ").lower().startswith("y")

    appeal_text = generate_appeal(phone, platform, appeal_type, device, tone)

    print("\n" + "-" * 55)
    print(" GENERATED APPEAL MESSAGE (PREVIEW) " if preview else " GENERATED APPEAL MESSAGE ")
    print("-" * 55)
    print(appeal_text)
    send_email = input("\nOpen Gmail with this appeal pre-written? (y/n): ").lower()

if send_email == "y":
    print("Opening Gmail draft...")
    open_gmail_draft(appeal_text)
else:
    print("You chose not to open Gmail.")

    print("\nSubmit your appeal here:")
    print(WHATSAPP_SUPPORT[platform])

    export = input("\nExport appeal to TXT file? (y/n): ").lower().startswith("y")
    if export:
        file_path = export_to_txt(phone, appeal_text)
        print(f"Appeal exported successfully: {file_path}")

    log_entry = {
        "phone": phone,
        "platform": platform,
        "appeal_type": appeal_type,
        "device": device,
        "timestamp": datetime.datetime.now().isoformat()
    }
    save_log(log_entry)

    print("\nAppeal saved locally.")
    print("Recommended: wait 24–48 hours before submitting another appeal.")
    print("This tool does NOT spam, automate, or bypass WhatsApp systems.")

if __name__ == "__main__":
    main()
    
def open_gmail_draft(appeal_text):
    recipient = "support@whatsapp.com"
    subject = "WhatsApp Account Review Request"

    body = appeal_text
    params = {
        "to": recipient,
        "subject": subject,
        "body": body
    }

    query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    mailto_link = f"mailto:?{query}"

    webbrowser.open(mailto_link)
