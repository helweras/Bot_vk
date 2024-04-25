import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import choice


class ButtonForBot:
    '''Кнопка для клавиатуры бота'''
    color = None
    label = None
    butt_type = ''

    def __init__(self, color, label, butt_type, link='', last=False):
        self.color = color
        self.label = label
        self.last = last
        self.butt_type = butt_type
        if butt_type == 'Link Button' and not link:
            raise TypeError('кнопка типа Link Button не может быть созданна без ссылки')
        else:
            self.link = link


class VkBot:
    '''Бот для ВК'''
    funny_answer = ('Ожидайте, скорее всего администраторы жгут резину на стадионе',
                    'Подождите еще немного , скорее всего ваше сообщение везет девушка на Матизе',
                    'Ожидайте, быстрее будет только ваш бывший',
                    'Если еще раз нажмешь на эту кнопку, то на месте сиерры-кабриолета можешь оказаться именно ты',
                    'Ожидайте, мы не 2jz чтобы рассмотреть вашу заявку от 0-100 за 3 секунды',
                    'Еще не рассмотрели, ведь ты не бмв, в которой закончилось масло, чтобы сразу на тебя реагировать')
    id_admin = 377265761
    token = (
        'vk1.a.ikAzLDwaYyt7Nr8c1Le7mWQVGyV9viLNxmvpGPiITZZtNFStz67hoSezzdz6gKOkIlBEWu2HiRjg6CNLuZNxCtEoWozxSvKCh3Jb'
        'v7i4ejpDXqDTqrt0lPe_bhGiHvj4IZIVYNOt33u8G2IZDATKO3xViGi25bMOr7wH4HHJWN1-iMMSzPOmeqr_hR2S1i-'
        'JYw1ueLwx0iQHFYIW-_Z_Ow')

    collect_butt = []
    user_incl_chat = [1, 2, 3, 4, 5, 6, 7, 8]

    def __init__(self, vk_session: vk_api.vk_api.VkApiMethod):
        self.collect_butt.append(
            ButtonForBot(color=VkKeyboardColor.POSITIVE, label='Вступить в беседу', butt_type='Text Button'))
        self.collect_butt.append(
            ButtonForBot(color=VkKeyboardColor.NEGATIVE,
                         label='Мы в других соц сетях',
                         butt_type='Text Button')
        )
        self.collect_butt.append(
            ButtonForBot(color=VkKeyboardColor.SECONDARY, label='Наши партнеры', butt_type='Link Button',
                         link='https://vk.com/topic-222161246_49381075'))
        self.collect_butt.append(
            ButtonForBot(color=VkKeyboardColor.SECONDARY, label='предложения/реклама', butt_type='Link Button',
                         link='https://m.vk.com/write-222161246',
                         last=True))
        self.vk_session = vk_session

    def keyboard_add_button(self, keyboard: vk_api.keyboard.VkKeyboard, button: ButtonForBot, link: str):
        '''Функция определяет тип кнопки и в соответствии с ним добавляет ее в клавиатуру'''
        if button.butt_type == 'Link Button':
            keyboard.add_openlink_button(button.label, link=f'https://vk.com/im?sel={self.id_admin}')
        elif button.butt_type == 'Text Button':
            keyboard.add_button(button.label, color=button.color)

    def create_keyboard(self):
        '''Создание клавиатуры бота. Обращение к атрибуту экземпляра класса VkBot
        collect_butt в которм находятся экземпляры класса ButtonForBot'''
        my_keyboard = VkKeyboard(one_time=True)  # Создали клавиатуру для бота
        for butt in self.collect_butt:
            if not butt.last:
                self.keyboard_add_button(my_keyboard, butt,
                                         link=butt.link)  # Кнопки добавляются в зависимости от их типа
                my_keyboard.add_line()
            else:
                self.keyboard_add_button(my_keyboard, butt, link=butt.link)
        return my_keyboard.get_keyboard()  # Преобразование в json - формат

    @staticmethod
    def create_keyboard_for_admin():
        admin_keyboard = VkKeyboard(one_time=True)
        admin_keyboard.add_button(label='Посмотреть заявки', color=VkKeyboardColor.POSITIVE)
        return admin_keyboard.get_keyboard()

    def answer_for_admin(self):
        if self.user_incl_chat:
            self.vk_session.messages.send(
                user_id=self.id_admin,
                message=f'Всего заявок {len(self.user_incl_chat)}',
                random_id=0,
                keyboard=self.create_keyboard_for_admin()
            )
            for user in self.user_incl_chat:
                self.vk_session.messages.send(
                    user_id=self.id_admin,
                    message=self.get_url_profile(user),
                    random_id=0,
                    keyboard=self.create_keyboard_for_admin()
                )
        else:
            self.vk_session.messages.send(
                user_id=self.id_admin,
                message='Заявок нет',
                random_id=0,
                keyboard=self.create_keyboard_for_admin()
            )

    def answer_for_all(self, messages: str, user_id):
        if user_id == self.id_admin:
            if messages == 'Посмотреть заявки':
                self.answer_for_admin()
                self.user_incl_chat.clear()
            else:
                self.vk_session.messages.send(
                    user_id=self.id_admin,
                    message='Такой команды нет',
                    random_id=0,
                    keyboard=self.create_keyboard_for_admin()
                )
        else:
            if not self.check_command(messages):
                self.vk_session.messages.send(user_id=user_id,
                                              message='такой команды нет',
                                              random_id=0,
                                              keyboard=self.create_keyboard())
            if messages == 'Вступить в беседу':
                self.app_in_chat(user_id)
            elif messages == 'Мы в других соц сетях':
                inst = 'Инстаграм https://www.instagram.com/autolady_39?igsh=YzVkODRmOTdmMw==&utm_source=qr'
                self.vk_session.messages.send(user_id=user_id,
                                              message='Телеграмм канал https://t.me/autolady39',
                                              random_id=0,
                                              keyboard=self.create_keyboard())
                self.vk_session.messages.send(user_id=user_id,
                                              message=inst,
                                              random_id=0,
                                              keyboard=self.create_keyboard())

    @staticmethod
    def get_url_profile(user_id):
        '''Возвращает ссылку на профиль человека'''
        return f"https://vk.com/id{user_id}"

    def check_command(self, message):
        '''Проверяет есть ли команда отправленная в чат боту в списке разрешенных.
        Возвращает True если команда есть.'''
        for butt in self.collect_butt:
            if message == butt.label:
                return True
        return False

    def app_in_chat(self, user_id):
        '''Функция проверяет и добавляет в user_incl_chat (Активные заявки) id пользователя
        если его там нет и отправляет сообщение пользовател в зависимости от того есть он там
        или нет. Возвращает True если пользователя нет.'''
        flag = user_id not in self.user_incl_chat
        if flag:
            self.user_incl_chat.append(user_id)
            self.vk_session.messages.send(
                user_id=user_id,
                message='Ожидайте, Ваша заявка на рассмотрении',
                random_id=0,
                keyboard=self.create_keyboard()
            )
        else:
            self.vk_session.messages.send(
                user_id=user_id,
                message=choice(self.funny_answer),
                random_id=0,
                keyboard=self.create_keyboard()
            )
        return flag

    def start_longpoll(self):
        pass
