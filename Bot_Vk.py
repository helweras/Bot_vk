import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import bs4


class VkBot:
    id_admin = 218357667
    token = (
        'vk1.a.ikAzLDwaYyt7Nr8c1Le7mWQVGyV9viLNxmvpGPiITZZtNFStz67hoSezzdz6gKOkIlBEWu2HiRjg6CNLuZNxCtEoWozxSvKCh3Jb'
        'v7i4ejpDXqDTqrt0lPe_bhGiHvj4IZIVYNOt33u8G2IZDATKO3xViGi25bMOr7wH4HHJWN1-iMMSzPOmeqr_hR2S1i-'
        'JYw1ueLwx0iQHFYIW-_Z_Ow')

    collect_butt = []
    user_incl_chat = []

    def __init__(self, vk_session: vk_api.vk_api.VkApiMethod):
        self.collect_butt.append(ButtonForBot(color=VkKeyboardColor.POSITIVE, label='Вступить в беседу'))
        self.collect_butt.append(ButtonForBot(color=VkKeyboardColor.SECONDARY, label='Партнерство'))
        self.collect_butt.append(
            ButtonForBot(color=VkKeyboardColor.SECONDARY, label='Предложения/сотрудничество', last=True))
        self.vk_session = vk_session

    def create_keyboard(self):
        '''Создание клавиатуры бота. Обращение к атрибуту экземпляра класса VkBot
        collect_butt в которм находятся экземпляры класса ButtonForBot'''
        my_keyboard = VkKeyboard(one_time=True)  # Создали клавиатуру для бота
        for butt in self.collect_butt:
            if not butt.last:
                my_keyboard.add_button(butt.label, color=butt.color)
                my_keyboard.add_line()
            else:
                my_keyboard.add_button(butt.label, color=butt.color)
        return my_keyboard

    def create_keyboard_for_admin(self):
        pass

    @staticmethod
    def get_url_profile(user_id):
        return f"https://vk.com/id{user_id}"

    def check_command(self, message):
        for butt in self.collect_butt:
            if message == butt.label:
                return True
        return False

    def app_in_chat(self, user_id):
        if user_id not in self.user_incl_chat:
            self.user_incl_chat.append(user_id)
            self.vk_session.messages.send(
                user_id=user_id,
                message='жди ответа',
                random_id=0,
                keyboard=self.create_keyboard().get_keyboard()
            )
        else:
            self.vk_session.messages.send(
                user_id=user_id,
                message='Ожидай долбаеб',
                random_id=0,
                keyboard=self.create_keyboard().get_keyboard()
            )

    def start_longpoll(self):
        pass


class ButtonForBot:
    color = None
    label = None

    def __init__(self, color, label, last=False):
        self.color = color
        self.label = label
        self.last = last
