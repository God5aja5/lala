import telebot
import requests
from telebot import types
import time
import os
import json
from gatet2 import check_card

# Bot setup
token = '8153296702:AAFN1KOe_u3b2P4ZgWlsO6GfRsXUHx5uF64'
bot = telebot.TeleBot(token, parse_mode="HTML")
allowed_users = ['47987980465', '7579489523', '7749807563', '6099962760']
admin_user_ids = ['your_admin_id']  # Replace with actual admin IDs

@bot.message_handler(commands=["start"])
def start(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    bot.reply_to(message, "Available Gateways:\n/ch - Stripe Charge $1\n/pp - PayPal Charge $1\n/stop - Stop the current process\n\nSend /ch or /pp followed by the txt file to start checking.")

@bot.message_handler(commands=["add"])
def add_user(message):
    if str(message.chat.id) in admin_user_ids:
        try:
            new_user_id = message.text.split()[1]
            allowed_users.append(new_user_id)
            bot.reply_to(message, f"User ID {new_user_id} Has Been Added Successfully.✅\nCongratulations! Premium New User🎉✅ ")
            save_user_ids()
        except IndexError:
            bot.reply_to(message, "Please provide a valid user ID. Example: /add 123456789")
    else:
        bot.reply_to(message, "You do not have permission to add users.🚫")

@bot.message_handler(commands=["ch"])
def stripe_charge(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    bot.reply_to(message, "Send the txt file now for Stripe Charge $1")
    bot.register_next_step_handler(message, process_stripe_charge)

@bot.message_handler(commands=["pp"])
def paypal_charge(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    bot.reply_to(message, "Send the txt file now for PayPal Charge $1")
    bot.register_next_step_handler(message, process_paypal_charge)

@bot.message_handler(commands=["stop"])
def stop_process(message):
    if str(message.chat.id) not in allowed_users:
        bot.reply_to(message, "🚫 You cannot use the bot. Contact developers to purchase a bot subscription.")
        return
    with open("stop.stop", "w") as file:
        pass
    bot.reply_to(message, "Successfully stopped 🛑")

def process_stripe_charge(message):
    process_charge(message, "Stripe")

def process_paypal_charge(message):
    process_charge(message, "PayPal")

def process_charge(message, gateway):
    if not message.document:
        bot.reply_to(message, "Please send a valid txt file.")
        return

    ko = bot.reply_to(message, f"Processing {gateway} Card Checking ...⌛").message_id
    file_info = bot.get_file(message.document.file_id)
    file_content = bot.download_file(file_info.file_path)

    with open("combo.txt", "wb") as w:
        w.write(file_content)

    try:
        with open("combo.txt", 'r') as file:
            lino = file.readlines()
            total = len(lino)
            checked_count = 0

            for cc in lino:
                if os.path.exists("stop.stop"):
                    bot.reply_to(message, "Successfully stopped 🛑")
                    os.remove("stop.stop")
                    return

                data = {}
                try:
                    response = requests.get(f'https://bins.antipublic.cc/bins/{cc[:6]}')
                    data = response.json()
                except Exception as e:
                    print(f"API Error: {e}")

                brand = data.get('brand', 'Unknown')
                card_type = data.get('type', 'Unknown')
                country = data.get('country_name', 'Unknown')
                country_flag = data.get('country_flag', '🏳')
                bank = data.get('bank', 'Unknown')

                start_time = time.time()
                try:
                    last = check_card(cc)
                except Exception as e:
                    print(e)
                    last = "Error processing card"

                end_time = time.time()
                execution_time = end_time - start_time
                checked_count += 1

                mes = types.InlineKeyboardMarkup(row_width=1)
                mes.add(
                    types.InlineKeyboardButton(f"• {cc} •", callback_data='u8'),
                    types.InlineKeyboardButton(f"• STATUS : {last} ", callback_data='u8'),
                    types.InlineKeyboardButton(f"• TOTAL 🎉 : [ {total} ] •", callback_data='x'),
                    types.InlineKeyboardButton(f"[ STOP 🚫 ]", callback_data='stop')
                )

                bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=ko,
                    text=f'''Wait for processing
By ➜ <a href='t.me/BaignX'>BaignX</a> ''',
                    reply_markup=mes
                )

                if "CHARGE ✅" in last:
                    bot.reply_to(message, f'''
🔥 CHARGED 1$ !
CC: <code>{cc}</code>
Response: Thank You For Donation 🎉
Info: {cc[:6]} - {card_type} - {brand}
Country: {country} {country_flag}
Bank: {bank}
Time: {"{:.1f}".format(execution_time)}s
Bot By: <a href='t.me/BaignX'>BaignX</a>
{checked_count} / {total}''')
                else:
                    bot.reply_to(message, f"❌ Declined. {checked_count} / {total}")

    except Exception as e:
        print(e)

    bot.edit_message_text(chat_id=message.chat.id, message_id=ko, text='BEEN COMPLETED ✅\nBOT BY ➜ @BaignX')

@bot.callback_query_handler(func=lambda call: call.data == 'stop')
def stop_callback(call):
    with open("stop.stop", "w") as file:
        pass
    bot.answer_callback_query(callback_query_id=call.id, text="Process stopped!")

def save_user_ids():
    with open("allowed_users.txt", "w") as file:
        for user_id in allowed_users:
            file.write(f"{user_id}\n")

def load_user_ids():
    global allowed_users
    if os.path.exists("allowed_users.txt"):
        with open("allowed_users.txt", "r") as file:
            allowed_users = [line.strip() for line in file.readlines()]

load_user_ids()
bot.polling()
