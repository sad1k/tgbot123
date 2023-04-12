from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
import os
import requests
import subprocess
import datetime
import speech_recognition as sr
from loader import dp
from aiogram import types

from states import Test

logfile = str(datetime.date.today()) + '.log'

def audio_to_text(dest_name: str):
    # Функция для перевода аудио, в формате ".vaw" в текст
    r = sr.Recognizer()  # такое вообще надо комментить?
    # тут мы читаем наш .vaw файл
    message = sr.AudioFile(dest_name)
    with message as source:
        audio = r.record(source)
    result = r.recognize_google(audio,
                                language="ru_RU")  # используя возможности библиотеки распознаем текст, так же тут можно изменять язык распознавания
    return result


@dp.message_handler(Command("test"))
# handler for the /convert command
def get_audio_messages(message):
    #Основная функция, принимает голосовуху от пользователя
    try:
        print("Started recognition...")
        #Ниже пытаемся вычленить имя файла, да и вообще берем данные с мессаги
        file_info = dp.get_file(message.voice.file_id)
        path = file_info.file_path  # Вот тут-то и полный путь до файла (например: voice/file_2.oga)
        fname = os.path.basename(path)  # Преобразуем путь в имя файла (например: file_2.oga)
        doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token,
                                                                             file_info.file_path))  # Получаем и сохраняем присланную голосвуху (Ага, админ может в любой момент отключить удаление айдио файлов и слушать все, что ты там говоришь. А представь, что такую бяку подселят в огромный чат и она будет просто логировать все сообщения [анонимность в телеграмме, ахахаха])
        with open(fname + '.oga', 'wb') as f:
            f.write(doc.content)  # вот именно тут и сохраняется сама аудио-мессага
        process = subprocess.run(['ffmpeg', '-i', fname + '.oga',
                                  fname + '.wav'])  # здесь используется страшное ПО ffmpeg, для конвертации .oga в .vaw
        result = audio_to_text(fname[:-3:] + '.wav')  # Вызов функции для перевода аудио в текст
        dp.send_message(message.from_user.id, format(result))  # Отправляем пользователю, приславшему файл, его текст
    except sr.UnknownValueError as e:
        # Ошибка возникает, если сообщение не удалось разобрать. В таком случае отсылается ответ пользователю и заносим запись в лог ошибок
        dp.send_message(message.from_user.id, "Прошу прощения, но я не разобрал сообщение, или оно поустое...")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(
                message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(
                message.from_user.username) + ':' + str(message.from_user.language_code) + ':Message is empty.\n')
    except Exception as e:
        # В случае возникновения любой другой ошибки, отправляется соответствующее сообщение пользователю и заносится запись в лог ошибок
        dp.send_message(message.from_user.id,
                         "Что-то пошло через жопу, но наши смелые инженеры уже трудятся над решением... \nДа ладно, никто эту ошибку исправлять не будет, она просто потеряется в логах.")
        with open(logfile, 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.today().strftime("%H:%M:%S")) + ':' + str(message.from_user.id) + ':' + str(
                message.from_user.first_name) + '_' + str(message.from_user.last_name) + ':' + str(
                message.from_user.username) + ':' + str(message.from_user.language_code) + ':' + str(e) + '\n')
