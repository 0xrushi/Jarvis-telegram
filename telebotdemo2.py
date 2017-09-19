from telegram.ext import Updater, CommandHandler,MessageHandler,Filters
from gtts import gTTS
#import telepot
import os
import speech_recognition as sr
from time import gmtime, strftime
import requests ,sys

def start(bot, update):
    update.message.reply_text('Hello World!')
    print(bot.get_me())

def mysendaudio(st,bot,update):
    tts = gTTS(text=st)
    tts.save("test.mp3")
    bot.send_audio(chat_id=update.message.chat_id, audio=open('test.mp3', 'rb'))
    os.system('rm -rf test.mp3')

def hello(bot, update):
    update.message.reply_text('Hello {}'.format(update.message.from_user))
    tts = gTTS(text='Good morning'+update.message.from_user.first_name, lang='en')
    tts.save("test.mp3")
    bot.send_audio(chat_id=update.message.chat_id, audio=open('test.mp3', 'rb'))
    os.system('rm -rf test.mp3')
    print(update.message)

def unknown(bot, update):
    #bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")
    update.message.reply_text('Sorry, I didnt understand that command')


def receive_audio(bot,update):
    print("audio received")
    file = bot.getFile(update.message.voice.file_id)
    print ("file_id: " + str(update.message.voice.file_id))
    currt=strftime("%Y-%m-%d %H:%M:%S", gmtime())
    file.download('voice.ogg')
    new_file_name='apple'+str(currt)+'.wav'
    #temp='ffmpeg -i voice.ogg '+new_file_name
    #os.system(temp)
    os.system('ffmpeg -i "%s" "%s"' % ('voice.ogg', new_file_name))

    os.system('rm -rf voice.ogg')
    print("audio converted")
    r = sr.Recognizer()

    with sr.WavFile(new_file_name) as source:
        audio = r.record(source)

    try:
        print("before")
        value = r.recognize_google(audio)
        print(value)
        print("after")
        process_audio(value,bot,update)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

    #print(update)


def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
    print(update)

def process_audio(mystr,bot,update):
    #print("inside processaudio mystr is "+mystr)
    print(update.message.chat_id)
    myl=mystr.split()
    if(myl[0]=='jarvis'):
        if (all(map(lambda w: w in mystr, ('weather', 'now')))):
            print('inside audio')
            mysendaudio("Can i get your location ",bot,update)
            myloc=receive_audio2(bot,update)
            print("myloc received "+myloc)
            st=MyWeather.get_weather(myloc)
            print(st)


t='KEY'
updater = Updater(t)
#bt=telepot.Bot(t)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('hello', hello))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.voice, receive_audio))


echo_handler = MessageHandler(Filters.text, echo)
updater.dispatcher.add_handler(echo_handler)

updater.start_polling()
updater.idle()
