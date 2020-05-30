import numpy as np
from tensorflow import keras
from tensorflow.keras import layers

# Dane ze zbioru MNIST
num_classes = 10
input_shape = (28, 28, 1)

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

x_train = np.expand_dims(x_train.astype("float32") / 255, -1)
x_test = np.expand_dims(x_test.astype("float32") / 255, -1)

print("Kształt: ", x_train.shape)
print(x_train.shape[0], "przykładów treningowych")
print(x_test.shape[0], "przykładów testowych")

# Konwersja wyników
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# Model
model = keras.Sequential([
  keras.Input(shape=input_shape),
  layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
  layers.MaxPooling2D(pool_size=(2, 2)),
  layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
  layers.MaxPooling2D(pool_size=(2, 2)),
  layers.Flatten(),
  layers.Dropout(0.5),
  layers.Dense(num_classes, activation="softmax"),
])

model.summary()

# Uczenie maszynowe
train = input("Czy chcesz zacząć uczenie maszynowe? [T/n]")

if (train == "" or train.lower() == "t"):
  batch_size = 128
  epochs = 15

  model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

  model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

  score = model.evaluate(x_test, y_test, verbose=0)
  print("Strata: ", score[0])
  print("Poprawność: ", score[1])

  # Zapis gotowego modelu
  save = input("Czy chcesz zapisać model? [T/n]")

  if (save == "" or save.lower() == "t"):
    model.save('model.h5')