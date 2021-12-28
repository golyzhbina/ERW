from keras.metrics import MeanIoU
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate
from tensorflow.keras import Model

input_layer = Input(shape=(1150, 180, 1), batch_size=None)
conv1 = Conv2D(64, (3, 3), padding="same", activation="relu")(input_layer)
conv1_2 = Conv2D(32, (3, 3), padding="same", activation="relu")(conv1)
pool1 = MaxPooling2D(pool_size=(2, 2))(conv1_2)

conv2 = Conv2D(32, (3, 3), padding="same", activation="relu")(pool1)
pool2 = MaxPooling2D(pool_size=(5, 2))(conv2)
up2 = UpSampling2D(size=(5, 2))(pool2)

conc3 = concatenate([pool1, up2])
up3 = UpSampling2D(size=(2, 2))(conc3)
conv3 = Conv2D(16, (3, 3), padding="same", activation="relu")(up3)
pool3 = MaxPooling2D(pool_size=(5, 3))(conv3)

conv4 = Conv2D(1, (1, 1), padding="same", activation="sigmoid")(conv3)

model = Model(inputs=[input_layer], outputs=[conv4])
print(model.summary())

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=[MeanIoU(num_classes=50), "accuracy"])
model.save("model_u.h5")