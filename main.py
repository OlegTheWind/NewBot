import random
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
import time
from scrap_pikabu import *
import json
from token_VK import token

session = vk_api.VkApi(token=token)

def send_message(user_id, message, keyboard=None, attachment=None):
    keyboard = keyboard.get_keyboard() if keyboard else None
    session.method("messages.send", {
        "peer_id": user_id,
        "message": message,
        "random_id": 0,
        "keyboard": keyboard,
        "attachment": attachment,
    })

hello = ["привет", "хелоу", "здарова заебал", "hi", "здарова"]
_help = ["помоги", "хелп", "помощь", "команды"]
humor = ["поржать", "кекнуть", "пост", "посменятся", "смешные картинки", "посты"]
_connection = ["Не понял тебя", "Не понял вас", "Слушай сформулируй по правилам", "Ну как так то", "ай опять не то пишешь", "Задрал", "Gblfh"]
_team = ["стоп"]
_start = ["начать"]
_stop = ["остановить"]

stop_flag = False

def handle_message(user_id, message):
    global stop_flag
    keyboard = None
    if message in hello:
        send_message(user_id, random.choice(hello))
    elif message in _help:
        send_message(user_id, "Бот еще не доработан: \nПока он умеет здороваться и скидывать ссылку на пост.\nПомощь, Пост, Приветствие")
    elif message in humor:
        scrap_pars("https://pikabu.ru/best")
        stop_flag = False
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button("Остановить", color=VkKeyboardColor.NEGATIVE)
        send_message(user_id, "Отправляю изображения...", keyboard)
        parse_and_send_data(user_id)
    elif message in _team:
        stop_flag = True
        send_message(user_id, "Бот остановлен.")
    else:
        send_message(user_id, random.choice(_connection))


def parse_and_send_data(user_id, max_images=10):
    global stop_flag
    images_sent = 0

    with open("post_info.json", "r") as file:
        tag_list = json.load(file)

    for item in tag_list:
        if stop_flag or images_sent >= max_images:
            break

        tag = item["Тег"]
        image = item["изображение"]

        if image is None or image == "Нет изображения":
            continue

        if stop_flag:
            send_message(user_id, "Бот остановлен.")
            break

        send_image(user_id, image)
        images_sent += 1

        if images_sent < max_images:
            time.sleep(2)

    if images_sent == 0:
        send_message(user_id, "Нет доступных изображений")

    return stop_flag

def send_image(user_id, image_url):
    # Step 1: Download the image
    response = requests.get(image_url, stream=True)
    if response.status_code != 200:
        send_message(user_id, "Failed to download the image.")
        return

    upload = vk_api.upload.VkUpload(session)
    photo = upload.photo_messages(photos=response.raw)[0]

    attachment = f"photo{photo['owner_id']}_{photo['id']}"
    send_message(user_id, "Изображение:", attachment=attachment)

def main():
    longpoll = VkLongPoll(session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            message = event.text.lower()
            handle_message(user_id, message)

if __name__ == "__main__":
    main()