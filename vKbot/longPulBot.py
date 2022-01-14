import vk_api
import requests
from keras.models import load_model
from keras_preprocessing.image import load_img
from numpy import asarray, expand_dims, array, reshape, uint8
from PIL import Image
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from info import token_group, group_id
from random import randint
import json


class MyBot:

    def __init__(self):

        self.vk = vk_api.VkApi(token=token_group)
        self.vk_api = self.vk.get_api()
        self.longpoll = VkBotLongPoll(self.vk, group_id=group_id)
        self.flag_greet = False
        self.flag_new_mess = True
        self.image = None
        print("Бот готов!")
        self.longpoll_cycle()

    def longpoll_cycle(self):

        for event in self.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                sender = event.message["from_id"]
                if 'всего доброго' in event.message['text'].lower():
                    self.write_msg(sender, 'До свидания! Умнейте и приходите.')
                elif 'поехали' in event.message['text'].lower():
                    self.write_msg(sender, 'Отлично! Присылайте томографию своего композита, посмотрим. ')

                elif 'привет' in event.message['text'].lower():
                    self.write_msg(sender, 'Добрейший денёчек! '
                                                'Этот бот является посредником между пользователем и написанной '
                                                'нейросетью, которая предназначена для определения структурных '
                                                'деффектов в композиционных меатриалах. Если вы не поняли и '
                                                'половины слов в предыдущем предложении, то предлагаю мирно пройти '
                                                'мимо, и все будут счастливы!'
                                                'Готовы продолжить? Если да - напишите "Поехали!", если нет - напишите '
                                                '"Всего доброго!"')

                elif event.message['attachments']:
                    if event.message["attachments"][0]['type'] == 'doc':
                        print(event.message)
                        self.write_msg(sender, "Понял, принял, ща все будет")
                        self.load_image(event.message['attachments'][0]['doc']['url'], sender)

                elif 'команды' in event.message['text'].lower():
                    self.write_msg(sender, '\n"Привет!" - узнать немного о боте.'
                                           '\n"Поехали!" - начать работу, вам предложат отправить свое фото.'
                                           '\n"Всего доброго!" - попрощаться с ботом и продолжить диалог.'
                                           '\n"Команды" - получить данный список команд.')
                else:
                    self.write_msg(sender, 'Что-что? Не понимаю вас... Давай е расскажу о доступных командах!'
                                           '\n"Привет!" - узнать немного о боте.'
                                            '\n"Поехали!" - начать работу, вам предложат отправить свое фото.'
                                            '\n"Всего доброго!" - попрощаться с ботом и продолжить диалог.'
                                            '\n"Команды" - получить данный список команд.')

    def write_msg(self, user_id, message):
        self.vk.method("messages.send", {"user_id": user_id, "message": message, "random_id": randint(1, 1000)})

    def load_image(self, address, sender):

        img = requests.get(address)
        out = open("img_original.jpg", "wb")
        out.write(img.content)
        out.close()
        self.img_to_arr(sender)

    def img_to_arr(self, sender):
        self.image = load_img("img_original.jpg",
                              color_mode="grayscale",
                              target_size=(1150, 180))
        img_arr = asarray(self.image)
        img_arr = img_arr / 255
        img_arr = expand_dims(img_arr, axis=0)
        self.serch_defect(img_arr, sender)

    def serch_defect(self, img, sender):

        model = load_model(r"..\nerual_network\model_u.h5")
        answer = model.predict(img)
        self.arr_to_img(answer, sender)

    def arr_to_img(self, arr, sender):

        arr = array(arr)
        arr = reshape(arr, (1150, 180))
        for i in range(len(arr)):
            arr[i] = array(list(map(lambda x: round(x * 255, 0), arr[i])))
        img_ans = Image.fromarray(arr)
        img_ans = img_ans.convert("L")
        img_ans.save("img_ans.jpg")
        self.send_img(sender, 'img_ans.jpg')
        self.detect_defect(sender)

    def draw_img(self, img):

        img_new = []
        for i in range(1150):
            img_new.append(list(map(list, img[i])))
            img_new[i].insert(0, [0, 0, 0, 0])
            img_new[i].append([0, 0, 0, 0])

        img_new.insert(0, [0, 0, 0, 0] * 180)
        img_new.append([0, 0, 0, 0] * 180)
        print(len(img_new), len(img_new[i]))

        new_layer = [[]] * 1152
        for i in range(1152):
            new_layer[i] = [[255, 255, 255, 0]] * 182

        for i in range(1, 1151):
            for j in range(1, 181):
                coords = [(i - 1, j - 1), (i, j - 1), (i - 1, j), (i, j), (i + 1, j + 1), (i + 1, j), (i, j + 1),
                          (i - 1, j + 1), (i + 1, j - 1)]

                for coord in coords:
                    if 100 <= img_new[i][j][0] <= 255:
                        new_layer[coord[0]][coord[1]] = array([225, 0, 0, 150])

        new_layer = new_layer[1:-1]
        new_layer = list(map(lambda x: x[1:-1], new_layer))

        new_layer = array(list(map(array, new_layer)))

        return new_layer

    def detect_defect(self, sender):
        img = Image.open(r"img_ans.jpg")
        img = img.convert("RGBA")
        img = asarray(img)
        mask = self.draw_img(img)
        new_img = Image.fromarray(mask.astype(uint8))
        new_img.save("img_mask.png")

        img_back = Image.open(r'img_original.jpg')
        img_back = img_back.convert("RGB")

        img_fore = Image.open('img_mask.png')
        img_fore = img_fore.convert("RGB")

        res = Image.blend(img_back, img_fore, 0.4)
        res.save("img_detect.png")
        self.send_img(sender, 'img_detect.png')

    def send_img(self, sender, name):
        result = json.loads(
            requests.post(self.vk_api.docs.getMessagesUploadServer(type='doc', peer_id=sender)['upload_url'],
                          files={'file': open(name, 'rb')}).text)
        jsonAnswer = self.vk_api.docs.save(file=result['file'], title='title', tags=[])

        self.vk_api.messages.send(
            peer_id=sender,
            random_id=0,
            attachment=f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"
        )


my_bot = MyBot()
