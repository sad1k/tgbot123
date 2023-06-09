from pathlib import Path
import requests
import os
from aiogram.types import ContentTypes
from loader import dp, bot, model
from data import config
import whisper
from pydub import AudioSegment
import subprocess


async def split_audio(input_file, output_dir, segment_duration, message):
    """Split an audio file into segments of a given duration."""
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Use ffprobe to get the duration of the input file
    duration = float(subprocess.check_output(['ffprobe', '-i', input_file, '-show_entries', 'format=duration', '-v', 'quiet', '-of', 'csv=p=0']))
    # Calculate the number of segments needed
    num_segments = int(duration // segment_duration) + 1
    # Use ffmpeg to split the input file into segments
    text = ''
    flag = False
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, duration)
        if ('oga' in input_file):
            flag = True
            output_file = os.path.join(output_dir, 'output{}.'.format(i)+['mp3','oga'][flag])
        else:
            output_file = os.path.join(output_dir, 'output{}.mp3'.format(i))
        subprocess.run(['ffmpeg', '-i', input_file, '-ss', str(start_time), '-t', str(end_time - start_time), '-c', 'copy', output_file], check=True)
        text += audio_to_text('E:\\tgbot123\\handlers\\users\\' + 'output{}.'.format(i)+['mp3','oga'][flag])
        os.remove(output_dir + 'output{}.'.format(i)+['mp3','oga'][flag])
    await bot.send_message(chat_id=message.from_user.id, text=text)




def audio_to_text(dest_name:str):
    file_src = Path(dest_name)
    # audio = AudioSegment.from_mp3(file_src)
    #
    # audio.export(file_src2, format='wav')
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(file_src)
    result = model.transcribe(audio, fp16=False, condition_on_previous_text=False)
    # with sr.AudioFile(open(file_src2, 'rb')) as source:
    #     audio =r.record(source)
    # result = r.recognize_google(audio, language='ru-RU')
    return result['text']



@dp.message_handler(content_types=ContentTypes.AUDIO)
async def get_audio_message(message):
    await bot.send_message(chat_id=message.from_user.id, text = 'converting...')
    audio_id = await bot.get_file(message.audio.file_id)
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.BOT_TOKEN,
                                                               audio_id.file_path))
    fname = os.path.basename(audio_id.file_path)
    with open('E:\\tgbot123\\handlers\\users\\' + fname, 'wb') as f:
        f.write(doc.content)

    await bot.send_message(chat_id=message.from_user.id, text=await split_audio('E:\\tgbot123\\handlers\\users\\' +fname, 'E:\\tgbot123\\handlers\\users\\', 60, message))

@dp.message_handler(content_types=ContentTypes.VOICE)
async def get_voice_message(message):
    await bot.send_message(chat_id=message.from_user.id, text = 'converting...')
    voice_id = await bot.get_file(message.voice.file_id)
    doc = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.BOT_TOKEN,
                                                               voice_id.file_path))
    fname = os.path.basename(voice_id.file_path)
    with open('E:\\tgbot123\\handlers\\users\\' + fname, 'wb') as f:
        f.write(doc.content)
    await split_audio('E:\\tgbot123\\handlers\\users\\' +fname,'E:\\tgbot123\\handlers\\users\\', 60, message)
