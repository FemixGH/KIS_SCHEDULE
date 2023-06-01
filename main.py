from vk_api.keyboard import VkKeyboard, VkKeyboardColor

from exel import *
from schedule import *
from weather import *

# Устанавливаем параметры для подключения к VK API
token = 'vk1.a.kNPB4DdK-yJVXRimG-A6RZ6xaMzaUt9inPbhiywknCv4q1l5SKBdh6Ir_srrvVi7mUP7JqTen5b8C5mRzvJqY1WyOAPO_R9Fi_PvOe_9dvdDoC-peeAGEg2HBKhbogUFGtR-2VxHeHGHwbzf6yvsNUG1VZ9BsDEXe3nDXGSPCQw0qaRXma1S8w3Vg55Rv9s-CuoBVbOZbM5BzNPdj7hZ4A'  # Ваш токен VK API
# Создаем клавиатуру
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Расписание на сегодня', color=VkKeyboardColor.POSITIVE)
keyboard.add_button('Расписание на завтра', color=VkKeyboardColor.NEGATIVE)
keyboard.add_line()  # Добавляем новую строку
keyboard.add_button('На эту неделю', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('На следующую неделю', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()  # Добавляем новую строку
keyboard.add_button('Какая неделя?', color=VkKeyboardColor.SECONDARY)
keyboard.add_button('Какая группа?', color=VkKeyboardColor.SECONDARY)
open_weather_token = "467e9329e78d70b728147eb922f99675"


def send_requirment():
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message="Введите свою группу",
        keyboard=keyboard.get_keyboard()
    )


def send_schedule(user_id, schedule):
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=f'Расписание:\n{schedule}',
        keyboard=keyboard.get_keyboard()
    )


def send_schedule_uneven(user_id, schedule):
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=f'Расписание на нечётную неделю:\n{schedule}',
        keyboard=keyboard.get_keyboard()
    )


def send_schedule_even(user_id, schedule):
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message=f'Расписание на чётную неделю:\n{schedule}',
        keyboard=keyboard.get_keyboard()
    )


def send_group_if_none(schedule_even, schedule_uneven):
    if (schedule_uneven is None) or (schedule_even is None):
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Такая группа не найдена',
            keyboard=keyboard.get_keyboard()

        )
        return False
    else:
        return True


def group_is_none():
    vk.messages.send(
        user_id=event.user_id,
        random_id=get_random_id(),
        message='Такая группа не найдена',
        keyboard=keyboard.get_keyboard()

    )


def send_schedule_about_day(schedule_uneven, schedule_even, user_id):
    formatted_schedule_uneven = '\n'.join([' '.join(lesson_info) for lesson_info in schedule_uneven])
    formatted_schedule_even = '\n'.join([' '.join(lesson_info) for lesson_info in schedule_even])
    send_schedule_uneven(user_id, formatted_schedule_uneven)
    send_schedule_even(user_id, formatted_schedule_even)


user_group = ''
temp_user_group = ''
file_path = ''
from datetime import datetime, timedelta


def handle_message(event):
    global user_group, file_path, temp_user_group
    user_id = event.user_id
    message = event.text.lower()
    day = what_day_is_it()
    current_week = get_current_week_number() - 4
    # print(current_week)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    message_words = message.split()
    # Получение текущей даты и времени
    now = datetime.now()

    # Получение даты следующего дня
    tomorrow = now + timedelta(days=1)

    # Получение дня недели для завтрашнего дня
    tomorrow_weekday = weekdays[tomorrow.weekday()]

    if check_group_format(message):
        file_path = create_file(message, links)
        user_group = capitalize_word(message)
        search_excel(file_path, user_group)
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Я запомнил, что ты из группы ' + user_group,
            keyboard=keyboard.get_keyboard()

        )
        print(user_group, " ")
    elif user_group == '' and (
            message == 'на следующую неделю' or message == 'на эту неделю' or message == 'какая группа?' or message == 'расписание на завтра' or message == 'расписание на сегодня' or message == 'Бот'):
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Введите номер группы',
            keyboard=keyboard.get_keyboard()
        )
    elif message == 'начать':
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Сперва введи номер своей группы, иначе магия не сработает)',
            keyboard=keyboard.get_keyboard()
        )

    elif len(message_words) < 3 and message_words[0] == 'бот' and check_group_format(message_words[1].strip()):
        user_group = capitalize_word(message_words[1])
        file_path = create_file(message_words[1], links)
        isSetGlobalNumber = False
        search_excel(file_path, user_group)
        print(user_group, " ")
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Показать расписание группы ' + user_group,
            keyboard=keyboard.get_keyboard()
        )


    elif message == 'бот':
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Показать расписание...',
            keyboard=keyboard.get_keyboard()
        )
    elif message == 'расписание на сегодня':
        schedule = get_day_schedule(file_path, day, current_week)
        if schedule is None:
            group_is_none()
        else:
            formatted_schedule = '\n'.join([' '.join(lesson_info) for lesson_info in schedule])
            send_schedule(user_id, formatted_schedule)
    elif message == 'расписание на завтра' and day == "Sunday":
        schedule = get_day_schedule(file_path, tomorrow_weekday, current_week + 1)
        if schedule == None:
            group_is_none
        else:
            formatted_schedule = '\n'.join([' '.join(lesson_info) for lesson_info in schedule])
            send_schedule(user_id, formatted_schedule)

    elif message == 'расписание на завтра' and day != "Sunday":
        schedule = get_day_schedule(file_path, tomorrow_weekday, current_week)
        if schedule == None:
            group_is_none
        else:
            formatted_schedule = '\n'.join([' '.join(lesson_info) for lesson_info in schedule])
            send_schedule(user_id, formatted_schedule)

    elif message == 'какая неделя?':
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Идёт" + " " + str(current_week - 1) + " " + "неделя",
            keyboard=keyboard.get_keyboard()
        )
    elif message == 'какая группа?':
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message="Показываю расписание группы" + " " + user_group,
            keyboard=keyboard.get_keyboard()
        )

    elif message == 'на эту неделю':
        week_schedule = get_week_schedule(file_path, current_week)
        if week_schedule is None:
            group_is_none
        else:
            formatted_week_schedule = '\n\n'.join([f'{day}:\n{schedule}' for day, schedule in week_schedule.items()])
            send_schedule(user_id, formatted_week_schedule)

    elif message == 'на следующую неделю':
        week_schedule = get_week_schedule(file_path, current_week + 1)
        if week_schedule is None:
            group_is_none
        else:
            formatted_week_schedule = '\n\n'.join([f'{day}:\n{schedule}' for day, schedule in week_schedule.items()])
            send_schedule(user_id, formatted_week_schedule)

    elif message == "бот " + "понедельник":
        schedule_uneven = get_day_schedule(file_path, "Monday", 2)
        schedule_even = get_day_schedule(file_path, "Monday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif message == "бот " + "вторник":
        schedule_uneven = get_day_schedule(file_path, "Tuesday", 2)
        schedule_even = get_day_schedule(file_path, "Tuesday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif message == "бот " + "среда":
        schedule_uneven = get_day_schedule(file_path, "Wednesday", 2)
        schedule_even = get_day_schedule(file_path, "Wednesday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif message == "бот " + "четверг":
        schedule_uneven = get_day_schedule(file_path, "Thursday", 2)
        schedule_even = get_day_schedule(file_path, "Thursday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif message == "бот " + "пятница":
        schedule_uneven = get_day_schedule(file_path, "Friday", 2)
        schedule_even = get_day_schedule(file_path, "Friday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif message == "бот " + "суббота":
        schedule_uneven = get_day_schedule(file_path, "Saturday", 2)
        schedule_even = get_day_schedule(file_path, "Saturday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    ############
    elif len(message_words) > 2 and message_words[0] == 'бот' and check_group_format(message_words[2].strip()) and \
            message_words[1] == "понедельник":
        temp_user_group = message_words[2]
        temp_file_path = create_file(temp_user_group, links)
        schedule_uneven = get_day_schedule(temp_file_path, "Monday", 2)
        schedule_even = get_day_schedule(temp_file_path, "Monday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif len(message_words) > 2 and message_words[0] == 'бот' and check_group_format(message_words[2].strip()) and \
            message_words[1] == "вторник":
        temp_user_group = message_words[2]
        temp_file_path = create_file(temp_user_group, links)
        schedule_uneven = get_day_schedule(temp_file_path, "Tuesday", 2)
        schedule_even = get_day_schedule(temp_file_path, "Tuesday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif len(message_words) > 2 and message_words[0] == 'бот' and check_group_format(message_words[2].strip()) and \
            message_words[1] == "среда":
        temp_user_group = message_words[2]
        temp_file_path = create_file(temp_user_group, links)
        schedule_uneven = get_day_schedule(temp_file_path, "Wednesday", 2)
        schedule_even = get_day_schedule(temp_file_path, "Wednesday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif len(message_words) > 2 and message_words[0] == 'бот' and check_group_format(message_words[2].strip()) and \
            message_words[1] == "четверг":
        temp_user_group = message_words[2]
        temp_file_path = create_file(temp_user_group, links)
        schedule_uneven = get_day_schedule(temp_file_path, "Thursday", 2)
        schedule_even = get_day_schedule(temp_file_path, "Thursday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif len(message_words) > 2 and message_words[0] == 'бот' and check_group_format(message_words[2].strip()) and \
            message_words[1] == "пятница":
        temp_user_group = message_words[2]
        temp_file_path = create_file(temp_user_group, links)
        schedule_uneven = get_day_schedule(temp_file_path, "Friday", 2)
        schedule_even = get_day_schedule(temp_file_path, "Friday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)

    elif len(message_words) > 2 and message_words[0] == 'бот' and check_group_format(message_words[2].strip()) and \
            message_words[1] == "суббота":
        temp_user_group = message_words[2]
        temp_file_path = create_file(temp_user_group, links)
        schedule_uneven = get_day_schedule(temp_file_path, "Saturday", 2)
        schedule_even = get_day_schedule(temp_file_path, "Saturday", 3)
        if send_group_if_none(schedule_even, schedule_uneven):
            send_schedule_about_day(schedule_uneven, schedule_even, user_id)


    elif message == "погода":
        city = "Москва"
        weather_message = get_weather(city, open_weather_token)
        if weather_message:
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message=weather_message,
                keyboard=keyboard.get_keyboard()
            )

    else:
        vk.messages.send(
            user_id=event.user_id,
            random_id=get_random_id(),
            message='Неизвестная команда',
            keyboard=keyboard.get_keyboard()
        )


# Создаем сессию для работы с VK API
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# Основной цикл для обработки сообщений
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        handle_message(event)
