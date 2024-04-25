import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from Bot_Vk import VkBot

vk_session = vk_api.VkApi(token=VkBot.token)  # Создали сессию для работы а именно авторизовали бота с помощью токена
longpoll = VkLongPoll(vk_session)  # Создали экз. класса для ослеживания всех входящих уведомдений от нашего бота
my_bot = VkBot(vk_session.get_api())
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text
        user_id = event.user_id
        my_bot.answer_for_all(message, user_id)
