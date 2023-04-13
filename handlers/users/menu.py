from pathlib import Path
import requests
import os
from aiogram.types import ContentTypes
from loader import dp, bot, model
from data import config
import whisper

async def audio_to_text(dest_name:str, message):
    file_src = Path(dest_name)
    # audio = AudioSegment.from_mp3(file_src)
    #
    # audio.export(file_src2, format='wav')
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file_src)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    options = whisper.DecodingOptions(fp16=False, language='ru',)
    result = whisper.decode(model, mel, options)
    os.remove(file_src)
    # with sr.AudioFile(open(file_src2, 'rb')) as source:
    #     audio =r.record(source)
    # result = r.recognize_google(audio, language='ru-RU')
    await bot.send_message(chat_id=message.from_user.id, text = result.text)



@dp.message_handler(content_types=ContentTypes.AUDIO)
async def get_audio_message(message):
    await bot.send_message(chat_id=message.from_user.id, text = 'converting...')
    audio_id = await bot.get_file(message.audio.file_id)
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.BOT_TOKEN,
                                                               audio_id.file_path))
    fname = os.path.basename(audio_id.file_path)
    with open('E:\\tgbot123\\handlers\\users\\' + fname, 'wb') as f:
        f.write(doc.content)
    result = await audio_to_text('E:\\tgbot123\\handlers\\users\\' +fname, message)
