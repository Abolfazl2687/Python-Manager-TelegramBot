# Manager Bot
# Coded By : Dark-Programmer
# v5

import telebot
import jdatetime 
import time
from faker import Faker

#***************************************************var***********************************************

bot = telebot.TeleBot("TOKEN" , parse_mode='HTML' , disable_web_page_preview=True)

faker = Faker("fa_IR")

madmin = ['Channel' , 'Group' , 'Ⓐⓑσ_σⓔⓔ' , 'Telegram']

warnings_file = "warnings.txt"

f = open("Users.txt","r")
Users = f.read().split("\n")
f.close()

def check_user(id):
    if str(id) in Users:
        pass
    else:
        f = open("Users.txt","a")
        f.write("\n"+str(id))
        f.close()

#***************************************************should join***********************************************

channels = ["@Learn_Farsi_Language_Easily"]

def check_join(channels , user):
    for i in channels:
        is_member = bot.get_chat_member(i , user)
        if is_member.status in ["kicked","left"]: return False
    return True

#***************************************************Warnings***********************************************

def get_user_warnings(user_id):
    try:
        with open(warnings_file, "r") as file:
            lines = file.readlines()

            for line in lines:
                data = line.split(":")
                if len(data) == 2 and int(data[0]) == user_id:
                    return int(data[1])

    except FileNotFoundError:
        return 0

def save_user_warnings(user_id, warnings):
    lines = []
    updated = False

    try:
        with open(warnings_file, "r") as file:
            lines = file.readlines()

            for i, line in enumerate(lines):
                data = line.split(":")
                if len(data) == 2 and int(data[0]) == user_id:
                    lines[i] = f"{user_id}:{warnings}\n"
                    updated = True
                    break

    except FileNotFoundError:
        pass

    if not updated:
        lines.append(f"{user_id}:{warnings}\n")

    with open(warnings_file, "w") as file:
        file.writelines(lines)

#*****************************************************privet*********************************************

#keyborad button
keyboard_markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
keyboard_markup.add("ارسال پیام ناشناس" , "پیام به ادمین 💻" , "مشخصات فیک ℹ" , "دریافت چت آیدی 🔢")

#inline keybord button (add channel)
sponser = telebot.types.InlineKeyboardButton("اسپانسر" , url="https://t.me/Learn_Farsi_Language_Easily")
markup = telebot.types.InlineKeyboardMarkup()
markup.add(sponser)

#start
@bot.message_handler(commands=["start"] , chat_types=["private"])
def Welcome(message):
    check_user(message.chat.id)
    if check_join(channels , message.from_user.id) == True:
        bot.send_chat_action(message.chat.id , "typing")
        linkm = f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'
        welcom = f"""
        سلام {linkm} !

        چه کاری می تونم برات انجام بدم ؟

        """
        bot.send_message(message.chat.id , welcom , reply_markup=keyboard_markup)
    else:
        bot.send_message(message.chat.id , "کاربر گرامی برای استفاده از ربات باید در چنل های زیر عضو شوید و ربات را دوباره استارت کنید !" , reply_markup=markup , reply_to_message_id=message.message_id)

#stop
@bot.message_handler(func= lambda m: m.text =="down" , chat_types=["private"])
def ssh(message):
    if message.from_user.username == "Abooee2687":
        bot.reply_to(message , " Bot Is Turning Off ! ")
        bot.stop_bot()
    else:
        pass

#all
@bot.message_handler(func= lambda m: m.text =="all" , chat_types=["private"])
def all(message):
    if message.from_user.username == "Abooee2687":
        bot.reply_to(message , " متن را برای ارسال همگانی وارد کنید : ")
        bot.register_next_step_handler(message , sall)
    else:
        pass
def sall(message):
    s , ns = 0
    for cid in Users:
        try:
            bot.send_message(cid , message.text)
            s += 1
        except:
            ns += 1
    bot.reply_to(message , f"ارسال شد : {s} \n ارسال نشد : {ns}")

#admin
@bot.message_handler(func= lambda m: m.text == "پیام به ادمین 💻" or m.text == "/admin" , chat_types=["private"])
def admin(message):
    check_user(message.chat.id)
    bot.send_chat_action(message.chat.id , "typing")
    bot.reply_to(message , "پیام خود را برای اطلاع به ادمین ارسال کنید :")
    bot.register_next_step_handler(message , admin_s)
def admin_s(message):
    bot.send_chat_action(message.chat.id , "typing")
    uid = message.chat.id
    bot.send_message(chat_id=5693860526 ,text=" ارسال شده از یکی از کاربران ربات : \n \n "+message.text+"\n \n چت ایدی کاربر : "+str(uid) )
    bot.reply_to(message , "ارسال شد.")

#fake
@bot.message_handler(func= lambda m: m.text == "مشخصات فیک ℹ" , chat_types=["private"])
def fake(message):
    check_user(message.chat.id)
    if check_join(channels , message.from_user.id) == True:
        bot.send_chat_action(message.chat.id , "typing")
        name = faker.name()
        username = faker.user_name()
        password = faker.password()
        gmail = faker.email()
        address = faker.address()
        bot.send_message(message.chat.id , f" نام : \n {name} \n نام کاربری : \n {username} \n پسورد : \n {password} \n ایمیل : \n {gmail} \n آدرس : \n {address}"  , reply_markup=markup , reply_to_message_id=message.id)
    else:
        bot.send_message(message.chat.id , "کاربر گرامی برای استفاده از ربات باید در چنل های زیر عضو شوید و ربات را دوباره استارت کنید !" , reply_markup=markup , reply_to_message_id=message.message_id)

#id
@bot.message_handler(func= lambda m: m.text == "دریافت چت آیدی 🔢" , chat_types=["private"])
def getwid(message):
    check_user(message.chat.id)
    if check_join(channels , message.from_user.id) == True:
        bot.send_chat_action(message.chat.id , "typing")
        bot.send_message(message.chat.id , "برای دریافت چت آیدی خودتان یک پیام بفرستید و برای دریافت چت آیدی شخص دیگر یک پیام از او فوروارد کنید کنید : " , reply_markup=markup , reply_to_message_id=message.message_id)
        bot.register_next_step_handler(message , id )
    else:
        bot.send_message(message.chat.id , "کاربر گرامی برای استفاده از ربات باید در چنل های زیر عضو شوید و ربات را دوباره استارت کنید !" , reply_markup=markup , reply_to_message_id=message.message_id)

def id(message):
    bot.send_chat_action(message.chat.id , "typing")
    try:
        bot.send_message(message.chat.id , f"چت آیدی برابر است با : \n \n {str(message.forward_from.id)}" , reply_markup=markup , reply_to_message_id=message.message_id)
    except:
        bot.send_message(message.chat.id , " چت ایدی برابر است با : \n \n "+str(message.chat.id)  , reply_markup=markup , reply_to_message_id=message.message_id)

#anonymous message
@bot.message_handler(func= lambda m: m.text == "ارسال پیام ناشناس" , chat_types=["private"])
def begin(message):
    check_user(message.chat.id)
    if check_join(channels , message.from_user.id) == True:
        bot.send_chat_action(message.chat.id , "typing")
        bot.send_message(message.chat.id , "لطفا چت آیدی فرد / گروه مورد نظر رو ارسال کنید : \n پیام تنها به کاربرانی که ربات را استارت کرده باشند ارسال خواهد شد!"  , reply_markup=markup , reply_to_message_id=message.message_id)
        bot.register_next_step_handler(message , getu)
    else:
        bot.send_message(message.chat.id , "کاربر گرامی برای استفاده از ربات باید در چنل های زیر عضو شوید و ربات را دوباره استارت کنید !" , reply_markup=markup , reply_to_message_id=message.message_id)

def getu(message):
    global tuser
    tuser = message.text
    bot.send_chat_action(message.chat.id , "typing")
    bot.send_message(message.chat.id , "لطفا پیام مورد نظر رو ارسال کنید : "  , reply_markup=markup)
    bot.register_next_step_handler(message , send)
def send(message):
    global tuser
    bot.send_chat_action(message.chat.id , "typing")
    try:
        bot.send_message(int(tuser) , message.text , reply_markup=markup)
        bot.send_message(message.chat.id , "ارسال شد." , reply_markup=markup , reply_to_message_id=message.message_id)
    except:
        bot.send_message(message.chat.id , "خطا در ارسال!" , reply_markup=markup , reply_to_message_id=message.message_id)

#else
@bot.message_handler(chat_types=["private"])
def elses(message):
    check_user(message.chat.id)
    bot.send_chat_action(message.chat.id , "typing")
    bot.send_message(message.chat.id , "اگر نظر یا پیشنهادی دارید به ادمین پیام دهید" , reply_markup=markup , reply_to_message_id=message.message_id)

#***************************************************Group manager***********************************************

#sing
@bot.channel_post_handler(func= lambda message: True)
def sign(message):
    signt = f'<a href="https://t.me/{str(message.chat.username)}">{message.chat.title}</a>'
    etext = f" {message.text} \n \n 👉 {signt}"
    bot.edit_message_text(etext, chat_id=message.chat.id, message_id=message.message_id)

#accept join request
@bot.chat_join_request_handler(func= lambda r: True)
def accept(r):
    if r.from_user.is_bot == False:
        linkm = f'<a href="https://t.me/{r.from_user.username}">{r.from_user.first_name}</a>'
        bot.approve_chat_join_request(r.chat.id , r.from_user.id)
        bot.send_message(r.chat.id , f"کاربر {linkm} \n درخواست جوین به گروه با موفقیت قبول شد !" , reply_markup=markup)
    else:
        bot.decline_chat_join_request(r.chat.id , r.from_user.id)

#join
@bot.message_handler(chat_types=["supergroup"] , content_types=["new_chat_members"])
def gwelcome(message):
    bot.send_chat_action(message.chat.id , "typing")
    linkm = f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'
    bot.reply_to(message , f"کاربر {linkm} \nبه گروه خوش آمدید ! ")

#time
@bot.message_handler(func= lambda message: message.text == "تاریخ" , chat_types=["supergroup"])
def tarikh(message):
    bot.send_chat_action(message.chat.id , "typing")
    miladtest = str(time.ctime()).split(" ")
    milad = str(miladtest[0])+" "+str(miladtest[1])+" "+str(miladtest[2])+" "+str(miladtest[4])
    shams = jdatetime.date.fromgregorian(day= time.gmtime().tm_mday , month= time.gmtime().tm_mon , year= time.gmtime().tm_year)
    bot.send_message(message.chat.id , f"تاریخ میلادی : \n {milad} \n \n تاریخ شمسی: \n {str(shams)}" , reply_markup=markup , reply_to_message_id=message.message_id)

#add admin
@bot.message_handler(func= lambda message: message.text == "ادمین" , chat_types=["supergroup"])
def add_admin(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        bot.send_chat_action(message.chat.id , "typing")
        bot.promote_chat_member(message.chat.id , message.reply_to_message.from_user.id , False , True , True , True , True , True , True , False , False , False , False , False , False)
        bot.send_message(message.chat.id , f"کاربر {linkm} \n با موفقیت ادمین شد ! " , reply_markup=markup , reply_to_message_id=message.message_id)

#remove admin
@bot.message_handler(func= lambda message: message.text == "حذف ادمین" , chat_types=["supergroup"])
def remove_admin(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        bot.send_chat_action(message.chat.id , "typing")
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        bot.promote_chat_member(message.chat.id , message.reply_to_message.from_user.id , False , False , False , False , False , False , False , False , False , False , False , False , False)
        bot.send_message(message.chat.id , f"کاربر {linkm} \n با موفقیت حذف ادمین شد ! " , reply_markup=markup , reply_to_message_id=message.message_id)

#pin
@bot.message_handler(func= lambda message: message.text == "پین" , chat_types=["supergroup"])
def pin(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        bot.send_chat_action(message.chat.id , "typing")
        bot.pin_chat_message(message.chat.id , message.reply_to_message.message_id)
        bot.reply_to(message , "پین شد.")

#unpin
@bot.message_handler(func= lambda message: message.text == "حذف پین" , chat_types=["supergroup"])
def unpin(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        bot.send_chat_action(message.chat.id , "typing")
        bot.unpin_chat_message(message.chat.id , message.reply_to_message.message_id)
        bot.reply_to(message , "پین حذف شد.")

#ban
@bot.message_handler(func= lambda message: message.text == "بن" , chat_types=["supergroup"])
def ban(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins and str(message.reply_to_message.from_user.id) != "5693860526":
        bot.send_chat_action(message.chat.id , "typing")
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        bot.ban_chat_member(message.chat.id , message.reply_to_message.from_user.id , revoke_messages=True)
        bot.reply_to(message , f"کاربر {linkm} \n با موفقیت بن شد.")

#unban
@bot.message_handler(func= lambda message: message.text == "حذف بن" and str(message.reply_to_message.from_user.id) != "5693860526" , chat_types=["supergroup"])
def unban(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        bot.send_chat_action(message.chat.id , "typing")
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        bot.unban_chat_member(message.chat.id , message.reply_to_message.from_user.id)
        bot.reply_to(message , f"کاربر {linkm} \n با موفقیت حذف بن شد.")

#silent
@bot.message_handler(func= lambda message: "سکوت" in message.text and str(message.reply_to_message.from_user.id) != "5693860526" , chat_types=["supergroup"])
def silent(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        try:
            a = message.text.split(" ")
            st = int(a[1])
            bot.send_chat_action(message.chat.id , "typing")
            linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
            bot.restrict_chat_member(message.chat.id , message.reply_to_message.from_user.id ,until_date=time.time() + (st*60) , can_send_messages=False , can_send_media_messages=False , can_send_polls=False , can_send_other_messages=False , can_add_web_page_previews=False)
            bot.reply_to(message , f"کاربر {linkm} \n با موفقیت به مدت {str(st)} دقیقه سکوت شد.")
        except: pass

#un silent
@bot.message_handler(func= lambda message: message.text == "ازاد" and str(message.reply_to_message.from_user.id) != "5693860526", chat_types=["supergroup"])
def unsilent(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        bot.send_chat_action(message.chat.id , "typing")
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        bot.restrict_chat_member(message.chat.id , message.reply_to_message.from_user.id , can_send_messages=True , can_send_media_messages=True , can_send_polls=True , can_send_other_messages=True , can_add_web_page_previews=True)
        bot.reply_to(message , f"کاربر {linkm} \n با موفقیت حذف سکوت شد.")

#Alert
@bot.message_handler(func=lambda message: message.text == "اخطار" and str(message.reply_to_message.from_user.id) != "5693860526", chat_types=["supergroup"])
def Alert(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:  
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        user_warnings = get_user_warnings(message.reply_to_message.from_user.id)
        if user_warnings == None:
            user_warnings = 0
        user_warnings += 1
        if user_warnings == 5:
            bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id , until_date=time.time() + 3600)
            bot.reply_to(message , f"کاربر {linkm} \n [ {str(user_warnings)} ] اخطار دریافت کرده است و برای 1 ساعت در حالت سکوت قرار گرفت.")
        elif user_warnings == 10:
            bot.kick_chat_member(message.chat.id , message.reply_to_message.from_user.id)
            bot.reply_to(message , f"کاربر {linkm} \n [ {str(user_warnings)} ] اخطار دریافت کرده است و از گروه بن شد.")
        else:
            bot.reply_to(message , f"کاربر {linkm} \n [ {str(user_warnings)} ] اخطار دریافت کرده است \n \n 5 اخطار=سکوت , 10 اخطار=بن")
        save_user_warnings(message.reply_to_message.from_user.id , user_warnings)  

#UnAlert
@bot.message_handler(func=lambda message: message.text == "حذف اخطار" and str(message.reply_to_message.from_user.id) != "5693860526", chat_types=["supergroup"])
def UnAlert(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        linkm = f'<a href="https://t.me/{message.reply_to_message.from_user.username}">{message.reply_to_message.from_user.first_name}</a>'
        user_warnings = get_user_warnings(message.reply_to_message.from_user.id)
        if user_warnings != None:
            user_warnings = 0
        save_user_warnings(message.reply_to_message.from_user.id , user_warnings)
        bot.reply_to(message , f"کاربر {linkm} \n [ {str(user_warnings)} ] اخطار دریافت کرده است \n \n 5 اخطار=سکوت , 10 اخطار=بن")

#Invite Link
@bot.message_handler(func=lambda message: message.text == "لینک" , chat_types=["supergroup"])
def get_link(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        link = bot.export_chat_invite_link(message.chat.id)
        bot.send_chat_action(message.chat.id , "typing")
        bot.reply_to(message , str(link))
    else:
        pass

#Links
@bot.message_handler(chat_types=["supergroup"])
def link(message):
    gadmin = bot.get_chat_administrators(message.chat.id)
    admins = [admin.user.first_name for admin in gadmin] + madmin
    if str(message.from_user.first_name) in admins:
        pass
    else:
        if message.entities:
            for entity in message.entities:
                if entity.type == 'url':
                    bot.send_chat_action(message.chat.id , "typing")
                    linkm = f'<a href="https://t.me/{message.from_user.username}">{message.from_user.first_name}</a>'
                    bot.send_message(message.chat.id , f"کاربر {linkm} . \n ارسال لینک در این گروه ممنوع می باشد ! " , reply_markup=markup)
                    bot.delete_message(message.chat.id , message.message_id)
                    break

#*************************************************Run*************************************************

bot.infinity_polling(skip_pending=False)
