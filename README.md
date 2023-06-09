# tgbot123

ENG: Whisper is a general-purpose speech recognition model. It is trained on a large dataset of diverse audio and is also a multitasking model that can perform multilingual speech recognition, speech translation, and language identification.

RUS: Whisper - это модель распознавания речи общего назначения. Она обучена на большом наборе данных разнообразных аудиозаписей и является многозадачной моделью, которая может выполнять многоязычное распознавание речи, перевод речи и идентификацию языка.

# Approach
![image](https://github.com/sad1k/tgbot123/assets/91619133/3ccd24d6-d069-4e1d-b0b6-0602bf389024)


ENG: A Transformer sequence-to-sequence model is trained on various speech processing tasks, including multilingual speech recognition, speech translation, spoken language identification, and voice activity detection. These tasks are jointly represented as a sequence of tokens to be predicted by the decoder, allowing a single model to replace many stages of a traditional speech-processing pipeline. The multitask training format uses a set of special tokens that serve as task specifiers or classification targets.

RUS: Модель преобразования последовательности в последовательность обучается на различных задачах обработки речи, включая распознавание многоязычной речи, перевод речи, идентификацию разговорного языка и определение голосовой активности. Эти задачи совместно представляются в виде последовательности лексем, которые должны быть предсказаны декодером, что позволяет одной модели заменить многие этапы традиционного конвейера обработки речи. Формат многозадачного обучения использует набор специальных лексем, которые служат в качестве спецификаторов задач или целей классификации


https://github.com/openai/whisper

