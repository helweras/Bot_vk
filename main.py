import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Bot_Vk import VkBot

my_bot = VkBot()

vk_session = vk_api.VkApi(token=VkBot.token)  # Создали сессию для работы а именно авторизовали бота с помощью токена
longpoll = VkLongPoll(vk_session)  # Создали экз. класса для ослеживания всех входящих уведомдений от нашего бота


keyboard = my_bot.create_keyboard().get_keyboard()  # Преобразование в json - формат

vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text.lower()
        user_id = event.user_id
        user_info = vk.users.get(user_ids=user_id, fields=['domain'])
        # Обработка полученного сообщения
        if message:
            vk.messages.send(user_id=user_id,
                             message=message,
                             random_id=0,
                             keyboard=keyboard)
        if message == 'вступить в беседу':
            vk.messages.send(user_id=user_id,
                             message=f'{user_id}, хочет вступить в беседу',
                             random_id=0)
