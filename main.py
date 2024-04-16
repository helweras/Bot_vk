import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Bot_Vk import VkBot

vk_session = vk_api.VkApi(token=VkBot.token)  # Создали сессию для работы а именно авторизовали бота с помощью токена
longpoll = VkLongPoll(vk_session)  # Создали экз. класса для ослеживания всех входящих уведомдений от нашего бота

my_bot = VkBot(vk_session.get_api())
vk = my_bot.vk_session

keyboard = my_bot.create_keyboard().get_keyboard()  # Преобразование в json - формат


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text
        user_id = event.user_id
        # Обработка полученного сообщения
        if not my_bot.check_command(message):
            vk.messages.send(user_id=user_id,
                             message='такой команды нет',
                             random_id=0,
                             keyboard=keyboard)
        if message == 'Вступить в беседу':
            my_bot.app_in_chat(user_id)


            # vk.messages.send(user_id=my_bot.id_admin,
            #                  message=f'{my_bot.get_url_profile(user_id)}, хочет вступить в беседу',
            #                  random_id=0)
