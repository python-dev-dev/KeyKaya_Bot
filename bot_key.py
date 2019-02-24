
import telebot
import threading
from time import sleep
from telebot import types
from generar_clave import ayuda_key
from generar_clave import generate_key
from SoporteTexto import msn_info
from datetime import datetime

'''
REQUERIMIENTOS:

pip install pyTelegramBotAPI
'''



BOT_TOKEN = "YOUR_TOKEN"
BOT_INTERVAL = 3
BOT_TIMEOUT = 30
bot = telebot.TeleBot(BOT_TOKEN)


# FUNCIONDE DE ESCUCHA | BOTONES
def listener(mensaje_telegram):
    for mensaje in mensaje_telegram:

        chat_id = mensaje.chat.id
        nombre = mensaje.chat.first_name
        usuario = mensaje.chat.username
        lenaguaje = mensaje.from_user.language_code
        fecha = str(datetime.now().strftime("%Y-%m-%d"))
        hora = str(datetime.now().strftime("%H:%M"))

        if mensaje.content_type == 'text':
            if mensaje.text == 'GENERAR CLAVE 🔑':
                # GENERA 
                clave = str(generate_key())
                bot.send_message(chat_id, "Espere un momento por favor 😊")
                bot.send_message(chat_id, clave )
                print("ID: ", str(chat_id), "\t NOMBRE: ", str(nombre) , "\t USUARIO: ", str(usuario), "\t IDIOMA: ", str(lenaguaje))
                print("-------------------------------------------------------------------------------------")
            elif mensaje.text == 'TIPS 📑':
                bot.send_message(chat_id, str(ayuda_key()))

            elif mensaje.text == 'INFO ℹ':
                bot.send_message(chat_id, msn_info,parse_mode='HTML',disable_web_page_preview=True)


# METODO DE ESCUCHA
bot.set_update_listener(listener)


def bot_polling():
    print("EMPEZANDO BOT ...")
    while True:
        try:
            print("NUEVA INSTANCIA DE BOT INICIADA")
            #bot = telebot.TeleBot(BOT_TOKEN) #Generate new bot instance
            botactions(bot) #If bot is used as a global variable, remove bot as an input param
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("FALLÓ EL SONDEO DEL BOT, REINICIANDO EN {}sec. ERROR:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("BOT TERMINADO")
            break #End loop




#ACCIONES DEL BOT
def botactions(bot):

    @bot.message_handler(commands=["start"])
    def command_start(message):
        msn =  "Bienvenid@ "+ message.chat.first_name+ "😊 a KeyKaya, un generador de claves seguras"
        chat_id = message.chat.id
        bot.send_message(chat_id, msn)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
        itembtn1 = types.KeyboardButton('GENERAR CLAVE 🔑')
        itembtn2 = types.KeyboardButton('TIPS 📑')
        itembtn3 = types.KeyboardButton('INFO ℹ')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(chat_id, "Elija una opción", reply_markup=markup)




# CORRIENDO CON HILO
polling_thread = threading.Thread(target=bot_polling)
polling_thread.daemon = True
polling_thread.start()


#EJECUCION PRINCIPAL MIENTRAS CORRE EN EL HILO
if __name__ == "__main__":
    while True:
        try:
            sleep(120)
        except KeyboardInterrupt:
            break
