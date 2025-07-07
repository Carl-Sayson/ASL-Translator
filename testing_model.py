# Test Model

import pandas as pd
import numpy as np
from keras.models import load_model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

try:
    # Load training data
    df = pd.read_csv("sign_mnist_train.csv")
    X = df.drop("label", axis=1).values / 255.0
    X = X.reshape(-1, 28, 28, 1)
    y = to_categorical(df["label"].values, num_classes=25)

    # Re-split to get validation data again
    _, X_val, _, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

    # Load trained model
    model = load_model("asl_alphabet_model.h5")

    # Pick a validation sample
    sample = X_val[13]
    true_label = np.argmax(y_val[12])

    # Predict
    prediction = model.predict(sample.reshape(1, 28, 28, 1))
    predicted_label = np.argmax(prediction)

    # Display
    plt.imshow(sample.reshape(28, 28), cmap='gray')
    plt.title(f"Predicted: {predicted_label}, Actual: {true_label}")
    plt.show()

except Exception as err:
    print(err)