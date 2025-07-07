# Training model for ASL

import pandas as pd

from keras.utils import to_categorical
from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

try:
    # loading the csv file
    df = pd.read_csv('sign_mnist_train.csv')

    # separating features
    x = df.drop("label", axis=1).values
    y = df["label"].values

    # normalizing pixels and reshaping it
    x = x / 255.0
    x = x.reshape(-1, 28, 28, 1)

    y = to_categorical(y, num_classes=25)

    # splitting data into training and validation sets
    x_train, x_val, y_train, y_val = train_test_split(x, y, test_size=0.1, random_state=42)

    # Building the AI model for translation

    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),

        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.3),

        Dense(25, activation='softmax') # 25 classes for letters
    ])

    # Compiling the model
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(x_train, y_train, epochs=15,
              batch_size=64, validation_data=(x_val, y_val))
    
    model.save('asl_alphabet_model.h5')
    print("✅ Model saved as 'asl_alphabet_model.h5'")

except Exception as err:
    print(f'Error found: {err}')