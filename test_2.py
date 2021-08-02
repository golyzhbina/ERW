import numpy as np
from tensorflow import keras
import os
import matplotlib.pylab as plt

# названия объектов распознования
names = ["ship", "frog", "dog", "cat", "bird", "airplane", "automobile", "deer", "horse", "truck"]

# импорт и обработка названий в обучающей и тренировочной выборках
y_train_file = open(r'C:\Users\Lenovo\Downloads\NN\labels_train.txt', 'r')
y_train = np.array(list(map(lambda x: names.index(x), map(lambda x: x.strip(), y_train_file))))

y_test_file = open(r'C:\Users\Lenovo\Downloads\NN\labels_test.txt', 'r')
y_test = np.array(list(map(lambda x: names.index(x), map(lambda x: x.strip(), y_test_file))))

y_train_cat = keras.utils.to_categorical(y_train, 10)
y_test_cat = keras.utils.to_categorical(y_test, 10)

# обработка изображений, преобразование к массиву
names_of_images = os.listdir(r"C:\Users\Lenovo\Downloads\NN\Train")
dir_name = r"C:\Users\Lenovo\Downloads\NN\Train"
x_train = []
for filename in names_of_images:
    x_train.append(plt.imread(os.path.join(dir_name, filename)))

# x_train = list(map(lambda x: np.expand_dims(x_train[x], axis=0), range(len(x_train))))
x_train = np.array(x_train) / 255

names_of_images = os.listdir(r"C:\Users\Lenovo\Downloads\NN\Test")
dir_name = r"C:\Users\Lenovo\Downloads\NN\Test"
x_test = []
for filename in names_of_images:
    x_test.append(plt.imread(os.path.join(dir_name, filename)))

# x_test = list(map(lambda x: np.expand_dims(x_test[x], axis=0), range(len(x_test))))
x_test = np.array(x_test) / 255

model = keras.Sequential([keras.layers.Flatten(input_shape=(32, 32, 3)),
                          keras.layers.Dense(128, activation='relu'),
                          keras.layers.Dense(64, activation='relu'),
                          keras.layers.Dense(32, activation='relu'),
                          keras.layers.Dense(10, activation='softmax')])
print(model.summary())
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train_cat, batch_size=30, epochs=30, validation_split=0.1)
model.evaluate(x_test, y_test_cat)





