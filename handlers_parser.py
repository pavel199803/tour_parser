import json
import random
import time

import urllib.request
from datetime import datetime, timedelta

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, URLInputFile, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

headers = [
    'ОТЕЛЬ, КОТОРЫЙ ТОЧНО ЗАПОМНИТСЯ ВАМ🔥',

    'ВЫ ИСКАЛИ ИМЕННО ЭТОТ🔝🤩 ОТЕЛЬ',

    '📍Пора ставить новые точки на карте! Отель из ежедневной подборки от наших тревел-экспертов:',

    'Искали повод для отпуска? Это он! Пора выбирать даты вылета🏝️',

    'Выбираете, какой курорт будет следующим? Ловите наше новое предложение🌅',

    'Почему вы еще не купили тур ТУДА?🗺️😍',

    'Скорее успевайте забронировать этот тур👇🏼',

    'Только посмотрите, какие цены на этот тур!🤩🔥',

    'Ты все еще просто смотришь?) Скорее бронируй даты тура🏝️',

    'Осторожно! Тут шокирующие цены на туры🤯👇🏼',

    'Это что за цены😍 «ВАУ!», говорим мы👇🏼',

    'WOW! Это же новый тур от Маркет Слетать ждет именно тебя🤩',

    'Полетели в отпуск?) Да, вот так просто👇🏼🏝️',

    'Устали от рабочей рутины? Скорее бронируйте тур🔥',

    'Где отдохнуть в следующий раз? Выбирать вам, а мы поможем с идеями👇🏼😍',

    'Вот это да! Новый тур от Маркет Слетать🤩',

    'Вы это видели?? Поделитесь туром с другом, вместе отдыхать веселее🗺',

]


@router.message(CommandStart())
async def get_tours_day(massage: Message, bot: Bot):
    massage_counter = 0
    while True:
        destination = 'tours_of_the_day.json'  # скачиваем json файл с хостинга
        url = 'https://market-sletat.ru/tours_of_the_day.json'
        urllib.request.urlretrieve(url, destination)
        # url = 'https://market-sletat.ru/tours_of_the_day.json'
        # response = requests.get(url)
        counter = 0

        with open('tours_of_the_day.json', encoding='utf-8') as file:  # вызов json словаря
            tours_dict = json.load(file)
            for key in tours_dict:  # перебор json словаря
                newline_char = '\n'
                price = f"{key['price']}"
                changed_price = f"{price[:-3]} {price[-3:]}"  # отделяем 3 знака в стоимости
                date_start = key['date_start']
                date_start = date_start.replace('-', '.')
                for n, i in enumerate(key['includes'], 0):  # переименновываем includes
                    if i == "Перелет":
                        key['includes'][n] = f"🛩️ Авиаперелет"
                    elif i == "Мед страховка":
                        key['includes'][n] = f"📘 Мед.страховка"
                    elif i == 'Проживание':
                        key['includes'][n] = f"🌐 Проживание в отеле (номер: {key['room_type']})"
                    elif i == 'Питание':
                        key['includes'][n] = f"🥣 Питание ({key['meals']})"
                    elif i == 'Трансфер':
                        key['includes'][n] = f"🚙 Трансфер"
                    elif i == 'Оздоровление':
                        key['includes'][n] = f"🏥 Оздоровление"
                    elif i == 'Лечение':
                        key['includes'][n] = f"👨🏼‍⚕️ Лечение)"
                    elif i == 'Экскурсия':
                        key['includes'][n] = f"🏰 Экскурсия"
                    elif i == 'Топливный сбор':
                        key['includes'][n] = f"💸 Топливный сбор"
                    elif i == 'Новогодний ужин':
                        key['includes'][n] = f"🎄 Новогодний ужин"
                random_header = random.choice(headers)  # генерация заголовка
                random_tour_photo = random.choice(key['tour_photo'])

                inline_tg = InlineKeyboardButton(  # инлайн кнопки
                    text="Наш Канал",
                    url='https://t.me/marketsletatspb'
                )
                inline_chat_bot = InlineKeyboardButton(
                    text="ТурАссистент",
                    url='https://t.me/assistant_market_sletat_bot'
                )
                inline_buy = InlineKeyboardButton(
                    text="Подробнее",
                    url=f"https://market-sletat.ru/tours-day/{key['id']}"
                )
                keyboard = InlineKeyboardMarkup(row_width=2,  # инициализируем инлайн клавиатуру 
                                                inline_keyboard=[
                                                    [inline_buy],
                                                    [inline_tg, inline_chat_bot]
                                                ])
                url = URLInputFile(f"https://market-sletat.ru{random_tour_photo}")  # генерация картинки
                await bot.send_photo(chat_id=-1002034874974,
                                     # отправляем сообщение с нужными элементами и вызываем инлайн клавиатуру
                                     photo=url,
                                     caption=f"<b>{random_header}</b>{newline_char}{newline_char}"  # 443453297  -1002034874974
                                             f"⭐️<b>{key['hotel']} {key['stars']}*</b>{newline_char}"
                                             f"({key['country']}, {key['resort']}){newline_char}{newline_char}"
                                             f"🛫 Вылет из <b>{key['depart_city']} "
                                             f"{date_start[-2:]}.{date_start[-5:-3]}</b> ({key['nights']} ночей){newline_char}"
                                             f"💷 <b>{changed_price} руб/чел</b> (при 2-ухместном размещении){newline_char}{newline_char}"
                                             f"<b>В стоимость тура входит:</b>{newline_char}"
                                             f"<i>{newline_char.join(key['includes'])}</i>{newline_char}{newline_char}"
                                             f"<b>📞<a href='tel:+78126705911'>8-(812)-670-59-11</a></b>{newline_char}{newline_char}"
                                             f"<b>Для бронирования и фиксации стоимости тура жмите на кнопку ниже👇🏼</b>",
                                     parse_mode='HTML',
                                     reply_markup=keyboard
                                     )

                current = datetime.now()  # Текущее время в местном часовом поясе
                late_time = current.replace(hour=22, minute=15, second=0, microsecond=0)  # остановка в 22:00
                if late_time <= current:
                    break
                else:
                    counter += 1
                    if counter == 3:  # условие для того чтобы постил по 2 поста
                        counter -= counter
                        time.sleep(3000)  # задержка 50 мин
        if massage_counter == 0:
            await bot.send_message(
                chat_id=-1002034874974,
                text=f"Путешественники!👋🏼 У нас всегда есть что-то новое и захватывающее, чтобы предложить "
                     f"вам, поэтому обязательно следите за нашими обновлениями! Однако, сегодня мы "
                     f"<u>хотим представить вам нашего верного помощника</u> — <b>ТурАссистента!</b>⭐️\n\n"
                     f"Этот <b>уникальный</b> бот создан для того, чтобы облегчить вашу жизнь и сэкономить ваше время при подборе тура."
                     f"<u>В два клика вы сможете заполнить анкету или связаться с нашим опытным экспертом</u>👩🏼‍💼, "
                     f"который поможет вам выбрать идеальный тур в соответствии с вашими предпочтениями и "
                     f"пожеланиями. И все это <b>менее чем за две минуты!</b>🔝\n\n"
                     f"Не упустите свой шанс получить <u>персональную подборку</u> лучших туров! <i>Переходите в бот</i> 👉🏼 "
                     f"<b>@assistant_market_sletat_bot</b> 👈🏼 и начните свое захватывающее путешествие прямо сейчас!"
            )
            massage_counter += 1
        else:
            await bot.send_message(
                chat_id=-1002034874974,
                text=f"Дорогие любители путешествий, мы каждый день стараемся удивлять вас новыми турами, но сегодня "
                     f"<u>хотим представить нашего незаменимого помощника</u> - ТурАссистента⭐️\n\n"
                     f"Этот <b>уникальный</b> бот поможет вам связаться с нашими экспертами или заполнить форму для "
                     f"поиска идеального тура <b>менее чем за 2 минуты</b>⤵️\n\n"
                     f"<b><a href='https://t.me/assistant_market_sletat_bot'>Перейдите в бот, "
                     f"чтобы получить персонализированную подборку туров, составленную специально для вас.</a></b> "
                     f"Не упустите возможность сделать свое следующее путешествие незабываемым!"
            )
            massage_counter -= 1
        future = current.replace(hour=14, minute=30, second=0, microsecond=0)  # повторный вызов в 14:30 каждого дня
        if future <= current:
            future += timedelta(days=1)

        print((future - current).seconds)
        time.sleep((future - current).seconds)

        # старые сообщения 
        # tours = (
        #    f"<b>{random_header}</b>\n\n"
        #    f"⭐️<b>{key['hotel']}</b>\n ({key['country']}, {key['resort']})\n\n"
        #    f"🛫 Вылет из <b>{key['depart_city']} {date_start[-2:]}.{date_start[-5:-3]}</b> ({key['nights']} ночей)\n"
        #    f"💷 <b>{key['price']} руб/чел</b> (при 2-ухместном размещении)\n\n"
        #    f"<b>В стоимость тура входит:</b>\n"
        #    f"<i>{'\n'.join(key['includes'])}</i>\n\n"
        #    f"Подписывайтесь на полезные каналы <i>«Маркет Слетать»:</i>\n\n"
        #    f"1️⃣<i><a href='https://t.me/marketsletatspb'>"
        #    f"Новости туризма, наши счастливые клиенты и интересные посты</a></i>🗺️\n"
        #    f"2️⃣<i><a href='https://t.me/assistant_market_sletat_bot'>Если предложение вам не подошло, "
        #    f"заполните анкету в нашем боте и мы подберем тур по вашим параметрам</a></i>✔️\n\n"
        #    f"Для бронирования и фиксации стоимости на тур свяжитесь с нами:\n"
        #    f"🖥️ <b><a href='https://market-sletat.ru/tours-day/{key['id']}'>"
        #    f"Изучить тур на сайте и оставить заявку</a></b>\n"
        #    f"📞 <b>8-(812)-670-59-11</b>",
        # )

        # await bot.send_message(chat_id=-1002034874974,
        #                       text=f"<b>Подписывайтесь на полезные каналы <i>«Маркет Слетать»:</i></b>\n\n"
        #                            f"1️⃣<i><a href='https://t.me/marketsletatspb'>"
        #                            f"Новости туризма, наши счастливые клиенты и "
        #                            f"интересные посты</a></i>🗺️\n"
        #                            f"2️⃣<i><a href='https://t.me/assistant_market_sletat_bot'>"
        #                            f"Если предложение вам не подошло, "
        #                            f"заполните анкету в нашем боте и мы подберем тур по вашим параметрам</a></i>✔️\n\n",
        #                       parse_mode="HTML", disable_web_page_preview=True
        #                       )
