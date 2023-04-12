from pathlib import Path
import requests
import os
from aiogram.types import ContentTypes
from loader import dp, bot
from data import config
import speech_recognition as sr
from pydub import AudioSegment

async def audio_to_text(dest_name:str, dest_name2:str, message):
    r = sr.Recognizer()
    AudioSegment.converter = "C:\\FFmpeg\\bin\\ffmpeg.exe"
    file_src = Path(dest_name)
    file_src2 = Path(dest_name2)
    audio = AudioSegment.from_mp3(file_src)

    audio.export(file_src2, format='wav')
    with sr.AudioFile(open(file_src2, 'rb')) as source:
        audio =r.record(source)
    result = r.recognize_google(audio, language='ru-RU')
    await bot.send_message(chat_id=message.from_user.id, text = result)



@dp.message_handler(content_types=ContentTypes.AUDIO)
async def get_audio_message(message):
    audio_id = await bot.get_file(message.audio.file_id)
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.BOT_TOKEN,
                                                               audio_id.file_path))
    fname = os.path.basename(audio_id.file_path)
    with open('E:\\aiogram-bot-template1\\handlers\\users\\' + fname, 'wb') as f:
        f.write(doc.content)
    result = await audio_to_text('E:\\aiogram-bot-template1\\handlers\\users\\' +fname,'E:\\aiogram-bot-template1\\handlers\\users\\' + fname[:-4] + '.wav', message)
