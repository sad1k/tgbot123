from pathlib import Path
import requests
import os
from aiogram.types import ContentTypes
from loader import dp, bot, model
from data import config
from deepgram import Deepgram
from pydub import AudioSegment

async def audio_to_text(dest_name:str, dest_name2,  message):
    file_src = Path(dest_name)
    file_src2 = Path(dest_name2)
    audio = AudioSegment.from_mp3(file_src)

    audio.export(file_src2, format='wav')
    # load audio and pad/trim it to fit 30 seconds
    # Initializes the Deepgram SDK
    deepgram = Deepgram(config.DEEPGRAM_API_KEY)
    # Open the audio file
    with open(file_src2, 'rb') as audio:
        # ...or replace mimetype as appropriate
        source = {'buffer': audio, 'mimetype': 'audio/wav'}
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
    os.remove(file_src)
    # with sr.AudioFile(open(file_src2, 'rb')) as source:
    #     audio =r.record(source)
    # result = r.recognize_google(audio, language='ru-RU')
    await bot.send_message(chat_id=message.from_user.id, text = response['results']["channels"][0]["alternatives"][0]["transcript"])



@dp.message_handler(content_types=ContentTypes.AUDIO)
async def get_audio_message(message):
    await bot.send_message(chat_id=message.from_user.id, text = 'converting...')
    audio_id = await bot.get_file(message.audio.file_id)
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.BOT_TOKEN,
                                                               audio_id.file_path))
    fname = os.path.basename(audio_id.file_path)
    with open('E:\\tgbot123\\handlers\\users\\' + fname, 'wb') as f:
        f.write(doc.content)
    result = await audio_to_text('E:\\tgbot123\\handlers\\users\\' +fname, 'E:\\tgbot123\\handlers\\users\\' +fname[:-4] + '.wav',  message)
