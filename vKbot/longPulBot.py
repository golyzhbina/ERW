import vk_api
import requests
import json
from keras.models import load_model
from keras_preprocessing.image import load_img
from numpy import asarray, expand_dims, array, reshape, uint8, shape, hstack
from PIL import Image
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from info import token_group, group_id
from random import randint
from os import listdir, remove, rmdir, mkdir


class MyBot:

    def __init__(self):

        self.vk = vk_api.VkApi(token=token_group)
        self.vk_api = self.vk.get_api()
        self.longpol = VkBotLongPoll(self.vk, group_id=group_id)
        self.flag = False
        self.flag_crit = False
        print("Бот готов!")
        self.longpoll_cycle()

    def longpoll_cycle(self):

        for event in self.longpol.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                sender = event.message["from_id"]
                if 'всего доброго' in event.message['text'].lower():
                    self.write_msg(sender, 'До свидания!')
                elif 'поехали' in event.message['text'].lower():
                    self.write_msg(sender, 'Отлично! Присылайте томографию своего композита, посмотрим.')

                elif event.message['text'].lower() in ["хай", "хай!", "привет", "привет!", "здравствуйте",
                                                       "здравствуйте!", "добрый день", "добрый день!"]:
                    self.write_msg(sender, 'Добрейший денёчек! '
                                                'Этот бот является посредником между пользователем и написанной '
                                                'нейросетью, которая предназначена для определения структурных '
                                                'деффектов в композиционных меатриалах.'
                                                'Готовы продолжить? Если да - напишите "Поехали!", если нет - напишите '
                                                '"Всего доброго!"')
                    self.vk_api.messages.send(peer_id=sender, sticker_id=53747, random_id=randint(1, 1000))

                elif event.message['attachments']:
                    if event.message["attachments"][0]['type'] == 'doc':
                        self.write_msg(sender, "Понял, принял, все будет, но придется подождать")
                        self.load_image(event.message['attachments'], sender)

                elif 'команды' in event.message['text'].lower():
                    self.write_msg(sender, '\n"Привет!" - узнать немного о боте.'
                                           '\n"Поехали!" - начать работу, вам предложат отправить свое фото.'
                                           '\n"Всего доброго!" - попрощаться с ботом.'
                                           '\n"Команды" - получить данный список команд.')
                elif event.message['text'].lower() in ['да!', 'да', "отлично!", "отлично", "ага!", "ага", "здорово!",
                                                       "здорово", "круто!", "круто", "конечно!", "конечно", "естественно!",
                                                       "естественно"]:

                    self.write_msg(sender, "Благодарю!")
                    self.vk_api.messages.send(peer_id=sender, sticker_id=58768, random_id=randint(1, 1000))
                elif event.message['text'].lower() in ["не очень!", "не очень", "так себе", "так себе!", "нет", "нет!",
                                                       "не совсем!", "не совсем"]:
                    self.flag_crit = True
                    self.write_msg(sender, "Почему? Подскажите, пожалуйста, что доработать.")

                elif self.flag_crit:
                    pass

                else:
                    self.write_msg(sender, 'Что-что? Не понимаю вас... Давай е расскажу о доступных командах!'
                                           '\n"Привет!" - узнать немного о боте.'
                                            '\n"Поехали!" - начать работу, вам предложат отправить свое фото.'
                                            '\n"Всего доброго!" - попрощаться с ботом и продолжить диалог.'
                                            '\n"Команды" - получить данный список команд.')

    def write_msg(self, user_id, message):
        self.vk.method("messages.send", {"user_id": user_id, "message": message, "random_id": randint(1, 1000)})

    def load_image(self, docs, sender):

        for i in range(len(docs)):
            img = requests.get(docs[i]['doc']['url'])
            mkdir(rf"imgs\original\img{i}")
            out = open(rf"imgs\original\img{i}\img_original{i}.jpg", "wb")
            out.write(img.content)
            out.close()
        self.img_to_arr(sender)

    def img_to_arr(self, sender):
        names = sorted(listdir(r'imgs\original'))
        for i in range(len(names)):

            img = Image.open(fr"imgs\original\{names[i]}\img_original{i}.jpg")
            img = img.convert("RGB")
            arr = asarray(img)
            size = shape(img)

            if i == len(names) - 1:
                self.flag = True

            if size[1] % 180 > 0 or size[0] % 1150 > 0:
                dif = 180 - size[1] % 180
                dif_1 = [dif // 2, dif - dif // 2]

                dif = 1150 - size[0] % 1150
                dif_0 = [dif // 2, dif - dif // 2]

                size_new = (size[0] + dif_0[0] + dif_0[1], size[1] + dif_1[0] + dif_1[1])

                new_arr = []
                for k1 in range(size[0]):
                    lst = [array([50, 50, 50]) for _ in range(dif_1[0])] + list(arr[k1]) + [array([100, 100, 100])
                                                                                            for _ in range(dif_1[1])]
                    new_arr.append(array(lst))

                for _ in range(dif_0[0]):
                    new_arr.insert(0, array([array([100, 100, 100]) for _ in range(size_new[1])]))

                for _ in range(dif_0[1]):
                    new_arr.append(array([array([100, 100, 100]) for _ in range(size_new[1])]))

                new_arr = array(new_arr, dtype=object)
                img = Image.fromarray(new_arr.astype(uint8))
                names_crop = []

                for j in range(size_new[1] // 180):

                    img_new = img.crop((180 * j, 0, 180 * (1 + j), 1150))
                    img_new.save(fr'imgs\original\img{i}\img{i}{j}.png')
                    names_crop.append(fr'img{i}{j}.png')

                imgs_arr = []

                for name in names_crop:
                    image = load_img(fr"imgs\original\img{i}\{name}",
                                          color_mode="grayscale",
                                          target_size=(1150, 180))
                    img_arr = asarray(image)
                    img_arr = img_arr / 255
                    img_arr = expand_dims(img_arr, axis=0)
                    imgs_arr.append(img_arr)
                self.serch_defect(imgs_arr, sender, sorted(listdir(r'imgs\original')).index(names[i]), dif_0, dif_1)
            else:
                imgs_arr = []
                image = load_img(fr"imgs\original\{names[i]}\img_original{i}.jpg",
                                 color_mode="grayscale",
                                 target_size=(1150, 180))
                img_arr = asarray(image)
                img_arr = img_arr / 255
                img_arr = expand_dims(img_arr, axis=0)
                imgs_arr.append(img_arr)

                self.serch_defect(imgs_arr, sender, sorted(listdir(r'imgs\original')).index(names[i]))

    def serch_defect(self, imgs, sender, k, dif_0=None, dif_1=None):

        model = load_model(r"..\nerual_network\model_u.h5")
        answers = []
        for img in imgs:
            ans = model.predict(img)
            answers.append(ans)

        self.arr_to_img(answers, sender, k, dif_0, dif_1)

    def arr_to_img(self, arrs, sender, k, dif_0, dif_1):

        imgs = []

        for i in range(len(arrs)):
            arr = array(arrs[i])
            arr = reshape(arr, (1150, 180))
            for j in range(len(arr)):
                arr[j] = array(list(map(lambda x: round(x * 255, 0), arr[j])))
            imgs.append(arr)

        if dif_1 is not None and dif_0 is not None:

            img_ans = hstack(tuple(imgs))
            img_ans = img_ans[dif_0[0]: 1150 - dif_0[1], dif_1[0]: shape(img_ans)[1] - dif_1[1]]
        else:
            img_ans = imgs[0]
        img_ans = Image.fromarray(img_ans.astype(uint8))
        img_ans.save(fr"imgs\answer\img_ans{k}.jpg")

        self.detect_defect(sender, k)

    def draw_img(self, img):

        img_new = []
        for i in range(len(img)):
            img_new.append(list(map(list, img[i])))
            img_new[i].insert(0, [0, 0, 0, 0])
            img_new[i].append([0, 0, 0, 0])

        img_new.insert(0, [0, 0, 0, 0] * 180)
        img_new.append([0, 0, 0, 0] * 180)

        new_layer = [[]] * (len(img) + 2)
        for i in range(len(new_layer)):
            new_layer[i] = [[255, 255, 255, 0]] * (len(img[0]) + 2)

        for i in range(1, len(img) + 1):
            for j in range(1, len(img[0]) + 1):
                coords = [(i - 1, j - 1), (i, j - 1), (i - 1, j), (i, j), (i + 1, j + 1), (i + 1, j), (i, j + 1),
                          (i - 1, j + 1), (i + 1, j - 1)]

                for coord in coords:
                    if 100 <= img_new[i][j][0] <= 255:
                        new_layer[coord[0]][coord[1]] = array([225, 0, 0, 150])

        new_layer = new_layer[1:-1]
        new_layer = list(map(lambda x: x[1:-1], new_layer))

        new_layer = array(list(map(array, new_layer)))

        return new_layer

    def detect_defect(self, sender, k):
        names = listdir(fr'imgs\answer')
        for i in range(len(names)):
            img = Image.open(fr"imgs\answer\img_ans{i}.jpg")
            img = img.convert("RGBA")
            img = asarray(img)
            mask = self.draw_img(img)
            new_img = Image.fromarray(mask.astype(uint8))
            new_img.save(fr"imgs\mask\img_mask{i}.png")

            img_back = Image.open(fr"imgs\original\img{i}\img_original{i}.jpg")
            img_back = img_back.convert("RGB")

            img_fore = Image.open(fr"imgs\mask\img_mask{i}.png")
            img_fore = img_fore.convert("RGB")

            res = Image.blend(img_back, img_fore, 0.4)
            res.save(fr"imgs\detect\img_detect{i}.png")

        self.send_img(sender, k)

    def send_img(self, sender, k):

        name_ori = sorted(listdir(fr'imgs\original\img{k}'))[-1]
        name_ori = fr'imgs\original\img{k}\{name_ori}'

        name_answ = sorted(listdir(r'imgs\answer'))[k]
        name_answ = fr'imgs\answer\{name_answ}'

        name_det = sorted(listdir(r'imgs\detect'))[k]
        name_det = fr'imgs\detect\{name_det}'

        names_two = (name_ori, name_answ, name_det)

        answers = []
        for name in names_two:

            result = json.loads(
                requests.post(self.vk_api.docs.getMessagesUploadServer(type='doc', peer_id=sender)['upload_url'],
                              files={'file': open(name, 'rb')}).text)
            jsonAnswer = self.vk_api.docs.save(file=result['file'], title='title', tags=[])
            answers.append(f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}")

        self.vk_api.messages.send(
                peer_id=sender,
                random_id=0,
                attachment=answers)

        self.write_msg(sender, "Принимайте работу!")

        if self.flag:
            self.flag = False
            self.write_msg(sender, 'Вам понравилось?')
            self.clean_folders()

    def clean_folders(self):
        names, last_f = sorted(listdir('imgs'))[:-1], sorted(listdir('imgs'))[-1]
        for f in names:

            for name in listdir(fr'imgs\{f}'):
                remove(fr'imgs\{f}\{name}')

        for f in listdir(fr'imgs\{last_f}'):

            for name in listdir(fr'imgs\{last_f}\{f}'):
                remove(fr'imgs\{last_f}\{f}\{name}')

            rmdir(fr'imgs\{last_f}\{f}')

    def write_crit(self, text):
        with open(" criticism.txt", "a") as f:
            f.write(f"{text}\n\n")


my_bot = MyBot()
