from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.error import BadRequest
from collections import defaultdict

TOKEN = "7579775071:AAGYmbOSZTiMbed3MnfTzVm6kob3a5eO4q0"
CHANNEL_ID = "@freeminingsitebysakin"

user_referrals = defaultdict(set)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.username or ""

    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status not in ["member", "administrator", "creator"]:
            await update.message.reply_text(f"🚫 আপনি আমাদের চ্যানেলে জয়েন করেননি!
👉 প্রথমে জয়েন করুন: {CHANNEL_ID}")
            return
    except BadRequest:
        await update.message.reply_text(f"❗ চ্যানেল চেক করতে ব্যর্থ!
দয়া করে আগে চ্যানেলে জয়েন করুন:
{CHANNEL_ID}")
        return

    # Referral tracking
    if context.args:
        referrer_id = context.args[0]
        if referrer_id != str(user_id):
            user_referrals[referrer_id].add(user_id)

    referral_count = len(user_referrals[str(user_id)])

    if referral_count >= 5:
        await update.message.reply_text("✅ চ্যানেল ও রেফার চেক কমপ্লিট হয়েছে!
🎉 আপনি বট ব্যবহার করতে পারবেন।")
    else:
        remaining = 5 - referral_count
        await update.message.reply_text(
            f"✅ চ্যানেল চেক ✅
❗ আপনাকে বট শেয়ার করতে হবে আরও {remaining} জনকে।
"
            f"👇 রেফার লিংক:
https://t.me/{context.bot.username}?start={user_id}"
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
