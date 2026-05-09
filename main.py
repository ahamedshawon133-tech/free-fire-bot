from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import random

# তোমার টেলিগ্রাম বট টোকেন
BOT_TOKEN = "8623859862:AAGt7p-QqOrPqecSNgUHlAbAl7n_zQFJPEU"

# ইউজারের ডাইমন্ড সেভ করার জন্য
user_diamonds = {}

# AI চ্যাটের জন্য কিছু রিপ্লাই
ai_replies = {
    "হ্যালো": ["হ্যাঁ বলো ভাই! কেমন আছো?", "আরে! আমি ভালো আছি তুমি কেমন?"],
    "কেমন আছো": ["আমি ভালো আছি! তুমি কেমন আছো?", "আলহামদুলিল্লাহ ভালো আছি 😊"],
    "তুমি কে": ["আমি তোমার ফ্রি ফায়ার ডাইমন্ড বট 🤖"],
    "কৌতুক": ["একটা মশা বিয়ে করলো মাছিকে... এখন ওদের বাচ্চা হবে মশি 😂", "শিক্ষক: 2+2 কত? ছাত্র: 22 স্যার!"],
    "ধন্যবাদ": ["স্বাগতম ভাই ❤️", "আরো কিছু লাগবে?"],
    "bye": ["আচ্ছা ভাই ভালো থেকো 👋", "ঠিক আছে পরে কথা হবে"]
}

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    user_id = update.effective_user.id
    if user_id not in user_diamonds:
        user_diamonds[user_id] = 100
    await update.message.reply_text(f"হ্যালো {user_name}! 👋\nআমি তোমার ডাইমন্ড + AI বট। /help লিখে সব কমান্ড দেখো")

# /help কমান্ড
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **বট কমান্ড লিস্ট**\n\n"
        "/start - বট শুরু করা\n"
        "/help - সাহায্য দেখা\n"
        "/game - গেম খেলা 50 ডাইমন্ড\n"
        "/balance - ডাইমন্ড ব্যালেন্স দেখা\n"
        "/shop - শপ মেনু দেখা\n"
        "/buy 50 - 50 ডাইমন্ড কেনা\n"
        "\n💬 স্ল্যাশ ছাড়াই চ্যাট করো\n"
        "উদাহরণ: কেমন আছো, কৌতুক বলো, তুমি কে"
    )

# /game কমান্ড
async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    diamonds = user_diamonds.get(user_id, 0)

    if diamonds >= 50:
        user_diamonds[user_id] = diamonds - 50
        remaining = user_diamonds[user_id]
        await update.message.reply_text(f"""
তুমি আমার সাথে গেম খেলতে হলে 
আমার দেওয়া UID: 10953663150 তে চলে আসো
খেলা হবে ফ্রি ফায়ার 🔥

৫০ ডাইমন্ড কাটা হলো
বর্তমান ব্যালেন্স: {remaining} 💎
        """)
    else:
        await update.message.reply_text(f"তোমার ডায়মন্ড নেই 😢\nবর্তমান ব্যালেন্স: {diamonds} 💎\nডায়মন্ড পেতে /shop টাইপ করো")

# /balance কমান্ড
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    diamonds = user_diamonds.get(user_id, 0)
    await update.message.reply_text(f"তোমার ডায়মন্ড ব্যালেন্স: {diamonds} 💎")

# /shop কমান্ড
async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🛒 শপ মেনু
10 ডায়মন্ড = 10 টাকা
50 ডায়মন্ড = 45 টাকা
100 ডায়মন্ড = 80 টাকা

কিনতে /buy 50 টাইপ করো
    """)

# /buy কমান্ড
async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        await update.message.reply_text("লিখো: /buy 50")
        return
    try:
        amount = int(context.args[0])
        user_diamonds[user_id] = user_diamonds.get(user_id, 0) + amount
        new_balance = user_diamonds[user_id]
        await update.message.reply_text(f"✅ {amount} ডায়মন্ড যোগ হলো!\nবর্তমান ব্যালেন্স: {new_balance} 💎")
    except ValueError:
        await update.message.reply_text("সঠিক নাম্বার লিখো। যেমন: /buy 50")

# AI চ্যাট - স্ল্যাশ ছাড়া
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.lower()
    reply = "আমি বুঝতে পারিনি 😅। কেমন আছো, কৌতুক বলো এগুলো লিখে দেখো"
    
    for key, responses in ai_replies.items():
        if key in user_msg:
            reply = random.choice(responses)
            break
    
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
 
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("game", game))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("বট চালু হয়েছে...")
    app.run_polling() 

if __name__ == "__main__":
    main()
