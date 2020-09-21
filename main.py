import os
import random
import re
from typing import Iterable

import telebot

from memegenerator import make_meme

FIRST = [
    'Жизнь',
    'Брат',
    'Судьба',
    'Пацан',
    'Волк',
    'Друг',
    'Девушка',
    'Слово',
    'Свобода',
    'Двор',
    'Мама',
    'Тот, кто рядом',
    'Враг',
    'Отец',
    'Бродяга',
    'Мажор',
    'Машина',
    'Любовь',
    'Лох',
    'Шлюха',
    'Пуля',
    'Ствол'
]

SECOND = [
    'всегда',
    'никогда',
    'порой',
    'иногда',
    'когда-то',
    'само собой',
    'через 20 лет',
    'сегодня',
    'сейчас',
    'уже',
    'в натуре',
    'вряд ли',
]

THIRD = [
    'не',
    ''
]

FOURTH = [
    'поймет',
    'предаст',
    'полюбит',
    'будет',
    'пьет',
    'говорит',
    'бьет',
    'забудет',
    'поймет',
    'поимеет',
    'перед Богом',
    'с братвой',
    'убьет',
    'придет',
    'идет',
    'ответит'
]

FIFTH = [
    'за свою любовь',
    'вопреки всем',
    'за маму',
    'за пацанов',
    'меня',
    'как волк',
    'по-братски',
    'с друзьями',
    'пацанов',
    'тебя',
    'братву',
    'за себя',
    'за базар',
]

bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))


path_mapping = {
    4: 'wolf',
    6: 'girl',
    16: 'cars',
    17: 'girl',
    19: 'girl',
    'default': 'bros'
}


def get_image_for_meme(word):
    path = path_mapping.get(FIRST.index(word.capitalize()), path_mapping['default'])
    return os.path.join('images', path, random.choice(os.listdir(os.path.join('images', path))))


def generate(*args):
    return ' '.join(map(random.choice, args)).replace('  ', ' ').strip()


def generate_message(first=None, split=False):
    if first is None:
        first = FIRST
    if not split:
        return generate(first, SECOND, THIRD, FOURTH, FIFTH)
    else:
        return generate(first, SECOND, THIRD), generate(FOURTH, FIFTH)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Приветствую тебя, брат! Помни всегда одно:\n\n' + generate_message())


words = '|'.join(map(lambda x: x.lower(), FIRST))
REGEX = r'(' + words + ')'


@bot.message_handler(regexp=REGEX)
def patsan_message(message):
    if matches := re.findall(REGEX, message.text.lower()):
        word = matches[-1].capitalize()
        image = get_image_for_meme(word)
        upper, lower = generate_message(first=[word], split=True)
        img = make_meme(upper, lower, image)
        with open(img, 'rb') as file:
            bot.send_photo(message.chat.id, file)


if __name__ == '__main__':
    bot.polling()
