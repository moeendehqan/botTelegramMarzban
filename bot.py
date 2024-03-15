import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import Function
bot = telebot.TeleBot('7042096088:AAEIU8Kx7AW12gF5-Ra2rnlURTKqsZiFWLo')
chat_id_admin = '62066305'
pck = Function.packing()
bot.delete_webhook()


def apply_pay_renew_info(message):
    sub = Function.sub_by_chat_lates_get(message.chat.id)
    if sub == False:
        bot.send_message(message.chat.id, 'چنین کاربری یافت نشد')
    else:
        get_price = Function.GetPrice(dic['data_limit_gig'],dic['timing'])
        Function.ReNow(sub)
        text = f'اشتراک شما تمدید شد.\n'
        text = text + f'اطلاعات پرداخت شما بعدا توسط پشتیبانی بررسی خواهد'
        bot.send_message(message.chat.id, text)
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
        text_for_admin = f'اطلاعات تمدید:\n'
        text_for_admin = text_for_admin + f'از کاربر {username}'
        text_for_admin = text_for_admin + 'مبلغ: '+ str(get_price['price'])+'\n'+'مدت: '+str(get_price['date'])+'\n'+'حجم: '+str(get_price['gig'])+'\n'
        Function.reNew_to_db(username, get_price['gig'], get_price['date'], sub, get_price['price'], message.chat.id)
        bot.send_message(chat_id_admin, text_for_admin)
        bot.forward_message(chat_id=chat_id_admin, from_chat_id=message.chat.id, message_id=message.message_id)


def get_pay_renew_info(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    apply = InlineKeyboardButton("تایید ✅", callback_data='apply_renew')
    Home = InlineKeyboardButton("لغو ❌", callback_data='cancel_renew')
    keyboard.add(apply, Home)
    text = 'ایا از اطلاعات ارسال شده مطمعن هستید؟\n'
    text = text + 'پس از تایید اشتراک شما به صورت خودکار به صورت الحساب تمدید میشود و بعدا اطلاعات پرداخت توسط پشتیبانی بررسی میشود و  در صورت که اطلاعات اشتباه ثبت کرده باشید امکان تمدید از طریق ربات براش شما غیر فعال و فرایند تمدید هم لغو میشود'
    
    bot.reply_to(message, text=text, reply_markup=keyboard)
    
    




def replay_status(message):
    sub = message.text
    dic = Function.UserGetUsage(sub)
    if dic == False:
        bot.send_message(message.chat.id, 'اشتراک یافت نشد')
    else:
        Function.sub_by_chat_set(sub, message.chat.id)
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
        handle_start(message)


def replay_renew(message):
    sub = message.text
    dic = Function.UserGetUsage(sub)
    if dic == False:
        bot.send_message(message.chat.id, 'اشتراک یافت نشد')
    else:
        Function.sub_by_chat_set(sub, message.chat.id)
        username = dic['username']
        GetPrice = Function.GetPrice(dic['data_limit_gig'],dic['timing'])
        price = GetPrice['price']
        data_limit_gig = GetPrice['gig']
        expire_last_day = GetPrice['date']
        cartNumber = '6037697663883889'
        cartHolder = 'معین دهقان منشادی'
        status = dic['status'].replace('active','فعال ✅').replace('disabled','غیرفعال ❌').replace('expired','منقضی ⛔').replace('limited','اتمام حجم 🚨')
        text = f"سلام {username}!\n"
        text = text + f"وضعیت  {status}\n\n"
        text = text + "🚀 افزایش 🚀 \n"
        text = text + f"⏳ مدت: {expire_last_day} روز\n"
        text = text + f"📶 حجم: {data_limit_gig} گیگابایت\n"
        text = text + f'\n\n💰 مبلغ: {price} تومان\n💳 شماره کارت: {cartNumber}\nبه نام {cartHolder}\nواریز و رسید یا اطلاعاتی که حاوی تاریخ و ساعت تراکنش و کارت مبدا و مبلغ باشد را ارسال کنید'
        keyboard = InlineKeyboardMarkup(row_width=2)
        Home = InlineKeyboardButton("❌ لغو ❌", callback_data='home')
        keyboard.add(Home)
        msg = bot.send_message(message.chat.id, text, reply_markup=keyboard)
        bot.register_next_step_handler(msg, get_pay_renew_info)


@bot.message_handler(commands=['start'])
def handle_start(message):
    Function.start_to_db(message.json)
    text = '🤖🔓 خوش آمدید! من ربات "شکن پلاس" هستم. با من در ارتباط باشید و به راحتی از خدمات VPN برای حفظ حریم خصوصی و دسترسی به محتوای محدود شده استفاده کنید. اگر سوالی دارید یا نیاز به راهنمایی دارید، فقط بپرسید. من آماده‌ام که کمک کنم! 🤖🔓'
    keyboard = InlineKeyboardMarkup(row_width=1)
    Buy = InlineKeyboardButton("خرید اشتراک", callback_data='buy')
    Renew = InlineKeyboardButton("تمدید اشتراک", callback_data='renew')
    Status = InlineKeyboardButton("وضعیت اشتراک", callback_data='status')
    Help = InlineKeyboardButton("راهنمای استفاده", callback_data='help')
    keyboard.add(Buy, Renew, Status, Help)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


# Handler for callback data from inline keyboard
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'home':
        handle_start(call.message)
    elif call.data == 'buy':
        bot.send_message(call.message.chat.id, "با توجه به لیست زیر بسته خود را انتخاب کنید")
        keyboard = InlineKeyboardMarkup(row_width=2)
        for i in pck:
            gig = i['gig']
            date = i['date']
            price = i['price']
            name = f'حجم: {gig} گیگ - مدت: {date} روز - قیمت: {price} تومان'
            pack01 = InlineKeyboardButton(name, callback_data=i['num'])
            keyboard.add(pack01)
        bot.send_message(call.message.chat.id, "https://t.me/shekanplus/52", reply_markup=keyboard)
    elif call.data == 'renew':
        msg = bot.send_message(call.message.chat.id, "توکن یا شناسه اشتراک خود را وارد کنید:")
        bot.register_next_step_handler(msg, replay_renew)
    elif call.data == 'status':
        msg = bot.send_message(call.message.chat.id, "توکن یا شناسه اشتراک خود را وارد کنید:")

        bot.register_next_step_handler(msg, replay_status)
    elif call.data == 'help':
        keyboard = InlineKeyboardMarkup(row_width=1)
        Android = InlineKeyboardButton("📱 اندروید", callback_data='android')
        ios = InlineKeyboardButton("📱 ای او اس", callback_data='ios')
        windows = InlineKeyboardButton("🖥 ویندوز", callback_data='windows')
        Home = InlineKeyboardButton("❌ لغو ❌", callback_data='home')

        keyboard.add(Android, ios, windows, Home)
        bot.send_message(call.message.chat.id, "برای راهنمای اتصال به سرویس ها لطفا سیستم عامل خود را انتخاب کنید", reply_markup=keyboard)
    elif call.data == 'android':
        bot.send_message(call.message.chat.id, "https://t.me/shekanplus/45")
    elif call.data == 'ios':
        bot.send_message(call.message.chat.id, "https://t.me/shekanplus/61")
        bot.send_message(call.message.chat.id, "https://t.me/shekanplus/69")
    elif call.data == 'windows':
        bot.send_message(call.message.chat.id, "https://t.me/shekanplus/70")
    else:
        if type(call.data) == int:
            for i in pck:
                if int(i['num']) == int(call.data):
                    text = ''
                    bot.send_message(call.message.chat.id, i['num'])
                    break
        else:
            print(0)
            handle_start(call.message)





bot.polling()
