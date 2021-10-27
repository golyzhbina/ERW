import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D
from tensorflow.keras.metrics import MeanIoU
from tensorflow.keras import Model
from numpy import array
from os import listdir
from os.path import join


# preparing data
way_to_original = r"E:\folder_J\images"
way_to_edited = r"E:\folder_J\images_e"


def load_images(way: str, lst_of_name: list) -> array:

    images = []
    for name in lst_of_name:
        image = load_img(join(way, name),
                         color_mode="grayscale",
                         target_size=(1150, 180))
        image = img_to_array(image) / 255
        images.append(image)

    return array(images)


images_name = listdir(way_to_original)

x_train = load_images(way_to_original, images_name)
y_train = load_images(way_to_edited, images_name)

input_layer = Input(input_shape=(1150, 180, 1))
conv1 = Conv2D(64, (3, 3), padding="same", activation="relu")(input_layer)      # 1150 * 180 * 64
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)                                   # 575 * 90 * 64

conv2 = Conv2D(32, (3, 3), padding="same", activation="relu")(pool1)            # 575 * 90 * 64 * 32
pool2 = MaxPooling2D(pool_size=(5, 2))(conv2)                                   # 115 * 45 * 64 * 32

conv3 = Conv2D(16, (3, 3), padding="same", activation="relu")(pool2)            # 115 * 45 * 64 * 32 * 16
pool3 = MaxPooling2D(pool_size=(5, 3))(conv3)                                          # 23 * 15 * 64 * 32 * 16

conv4 = Conv2D(1, (1, 1), padding="same", activation="sigmoid")(pool3)                # 23 * 15 * 64 * 32 * 16

model = Model(inputs=[input_layer], outputs=[conv4])
print(model.summary())
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[MeanIoU(num_classes=50)])
his = model.fit(x_train, y_train,batch_size=30, epochs=15, validation_split=0.1)
plt.plot(his.history['loss'])
plt.plot(his.history['val_loss'])
plt.show()





