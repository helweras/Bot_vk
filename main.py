import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

admin = int(218357667)

token = (
    'vk1.a.ikAzLDwaYyt7Nr8c1Le7mWQVGyV9viLNxmvpGPiITZZtNFStz67hoSezzdz6gKOkIlBEWu2HiRjg6CNLuZNxCtEoWozxSvKCh3Jbv7i4'
    'ejpDXqDTqrt0lPe_bhGiHvj4IZIVYNOt33u8G2IZDATKO3xViGi25bMOr7wH4HHJWN1-iMMSzPOmeqr_hR2S1i-JYw1ueLwx0iQHFYIW-_Z_Ow')

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Вступить в беседу', VkKeyboardColor.SECONDARY)
keyboard.add_line()
keyboard.add_button('Партнерство', VkKeyboardColor.POSITIVE)
keyboard.add_line()
keyboard.add_button('Предложения/сотрудничество', VkKeyboardColor.POSITIVE)

keyboard = keyboard.get_keyboard()

vk = vk_session.get_api()

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        message = event.text.lower()
        user_id = event.user_id
        user_info = vk.users.get(user_ids=user_id, fields=['domain'])
        print(user_info)
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
