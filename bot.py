import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import Function
bot = telebot.TeleBot('7042096088:AAEIU8Kx7AW12gF5-Ra2rnlURTKqsZiFWLo')
bot.delete_webhook()


def replay_status(message):
    sub = message.text
    dic = Function.UserGetUsage(sub)
    username = dic['username']
    used_traffic_gig = dic['used_traffic_gig']
    data_limit_gig = dic['data_limit_gig']
    used_traffic_rate = dic['used_traffic_rate']
    expire_jalali = dic['expire_jalali']
    expire_last_day = dic['expire_last_day']
    status = dic['status'].replace('active','فعال ✅').replace('disabled','غیرفعال ❌').replace('expired','منقضی ⛔').replace('limited','اتمام حجم 🚨')

    text = f"سلام {username}!\nوضعیت اشتراک شما:\n"
    text = text + f" - 🚀 حجم مصرف شده: {used_traffic_gig} گیگابایت\n"
    text = text + f" - 🚧 حجم باقی مانده: {data_limit_gig} گیگابایت\n"
    text = text + f" - 📶 درصد مصرف حجم: {used_traffic_rate} %\n"
    text = text + f" - 📆 تاریخ انقضا: {expire_jalali}\n"
    text = text + f" - ⏳ مدت اعتبار: {expire_last_day} روز\n"
    text = text + f" - 🛜 وضعیت: {status}\n"
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['start'])
def handle_start(message):
    Function.Message2db(message.json)
    text = '🤖🔓 خوش آمدید! من ربات "شکن پلاس" هستم. با من در ارتباط باشید و به راحتی از خدمات VPN برای حفظ حریم خصوصی و دسترسی به محتوای محدود شده استفاده کنید. اگر سوالی دارید یا نیاز به راهنمایی دارید، فقط بپرسید. من آماده‌ام که کمک کنم! 🤖🔓'
    keyboard = InlineKeyboardMarkup(row_width=1)
    Buy = InlineKeyboardButton("خرید اشتراک", callback_data='buy')
    Renew = InlineKeyboardButton("تمدید اشتراک", callback_data='renew')
    Status = InlineKeyboardButton("وضعیت اشتراک", callback_data='status')
    Help = InlineKeyboardButton("راهنمای استفاده", callback_data='help')
    keyboard.add(Buy, Renew, Status, Help)
    bot.reply_to(message, text, reply_markup=keyboard)

# Handler for callback data from inline keyboard
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'buy':
        bot.send_message(call.message.chat.id, "خرید")
    elif call.data == 'renew':
        bot.send_message(call.message.chat.id, "تمدید")
    elif call.data == 'status':
        msg = bot.send_message(call.message.chat.id, "توکن یا شناسه اشتراک خود را وارد کنید:")
        bot.register_next_step_handler(msg, replay_status)
    elif call.data == 'help':
        keyboard = InlineKeyboardMarkup(row_width=3)
        Android = InlineKeyboardButton("اندروید", callback_data='android')
        ios = InlineKeyboardButton("ای او اس", callback_data='ios')
        windows = InlineKeyboardButton("ویندوز", callback_data='windows')
        keyboard.add(Android, ios, windows)
        bot.send_message(call.message.chat.id, "راهنما", reply_markup=keyboard)

bot.polling()
