import vk_api
import requests
from keras.models import load_model
from keras_preprocessing.image import load_img
from numpy import asarray, expand_dims, array, reshape
from PIL import Image
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from info import token_group
from random import randint


class MyBot:

    def __init__(self):

        self.vk = vk_api.VkApi(token=token_group)
        self.longpoll = VkBotLongPoll(self.vk, group_id="209793179")
        self.flag_greet = False
        self.flag_new_mess = True
        self.image = None
        print("Бот готов!")
        self.longpoll_cycle()

    def longpoll_cycle(self):

        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                if event.message['text'].lower() == 'всего доброго!':
                    self.write_msg("230874519", 'До свидания! Умнейте и приходите.'
                                                ' Если вы хотите вернуться назад - пишите "Возвращаемся!"')
                elif event.message['text'].lower() == 'поехали!':
                    self.write_msg("230874519", 'Отлично! Присылайте томографию своего композита, посмотрим. '
                                                'Если вы хотите вернуться назад - пишите "Возвращаемся!"')
                elif event.message['text'].lower() == 'возвращаемся!':
                    self.write_msg("230874519", 'Добрейший денёчек! '
                                                'Этот бот является посредником между пользователем и написанной '
                                                'нейросетью, которая предназначена для определения структурных '
                                                'деффектов в композиционных меатриалах. Если вы не поняли и '
                                                'половины слов в предыдущем предложении, то предлагаю мирно пройти '
                                                'мимо, и все будут счастливы!'
                                                'Готовы продолжить? Если да - напишите "Поехали!", если нет - напишите '
                                                '"Всего доброго!"')

                elif event.message['attachments'][0]['type'] == 'photo':
                    self.write_msg("230874519", "Понял, принял, ща все будет")
                    self.load_image(event.message['attachments'][0]['photo']['sizes'][-1]['url'])

                else:
                    if self.flag_greet:
                        self.write_msg("230874519", 'Что-что? Не понимаю вас... Давай е расскажу о доступных командах!'
                                                    '\n"Поехали!" - начать работу, вам предложат отправить свое фото.'
                                                    '\n"Всего доброго!" - попрощаться с ботом и продолжить диалог.'
                                                    '\n"Возращаемся!" - получить приветственное сообщение.')
                if not self.flag_greet:
                    self.write_msg("230874519", 'Добрейший денёчек! '
                                                'Этот бот является посредником между пользователем и написанной '
                                                'нейросетью, которая предназначена для определения структурных '
                                                'деффектов в композиционных материалах. Если вы не поняли и '
                                                'половины слов в предыдущем предложении, то предлагаю мирно пройти '
                                                'мимо, и все будут счастливы!'
                                                'Готовы продолжить? Если да - напишите "Поехали!", если нет - напишите '
                                                '"Всего доброго!"')

                    self.flag_greet = True
                print(event.message)

    def write_msg(self, user_id, message):
        self.vk.method("messages.send", {"user_id": user_id, "message": message, "random_id": randint(1, 1000)})

    def serch_defect(self, img):

        model = load_model(r"..\nerual_network\model_u.h5")
        answer = model.predict(img)
        self.arr_to_img(answer)

    def load_image(self, address):

        img = requests.get(address)
        out = open("img.jpg", "wb")
        out.write(img.content)
        out.close()
        self.img_to_arr()

    def img_to_arr(self):
        self.image = load_img("img.jpg",
                              color_mode="grayscale",
                              target_size=(1150, 180))
        img_arr = asarray(self.image)
        img_arr = img_arr / 255
        img_arr = expand_dims(img_arr, axis=0)
        self.serch_defect(img_arr)

    def arr_to_img(self, arr):

        arr = array(arr)
        arr = reshape(arr, (1150, 180))
        for i in range(len(arr)):
            arr[i] = array(list(map(lambda x: round(x * 255, 0), arr[i])))
        img_ans = Image.fromarray(arr)
        img_ans = img_ans.convert("L")
        img_ans.save("img_ans.jpg")
        self.send_img()

    def send_img(self):
        upload = vk_api.VkUpload(self.vk)
        photo = upload.photo_messages('img_ans.jpg')
        owner_id = photo[0]['owner_id']
        photo_id = photo[0]['id']
        access_key = photo[0]['access_key']
        attachment = f'photo{owner_id}_{photo_id}_{access_key}'
        self.vk.method("messages.send", {"user_id": "230874519", "random_id": randint(1, 1000), "attachment": attachment})

my_bot = MyBot()
