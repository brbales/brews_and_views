# dependencies
from keras.models import load_model
import os
import numpy as np
import pandas as pd

# load model
model = load_model("beer_categories_3p_unscaled.h5")

# call user inputs from app
input_beer_params = []

# test model using example user input
probs = model.predict(np.array(input_beer_params))

# place test results in dataframe to manage form of final output
probs_df = pd.DataFrame(probs)

# transform dataframe to swap rows and columns, then reset index
probs_dfT = probs_df.T
prob_setup = probs_dfT.reset_index()

# rename columns to match meanings
prob_setup.rename(columns={"index": "class"}, inplace=True)
prob_setup.columns = ["class", "prob"]

# sort dataframe to establish top 3 predicted categories
probs_done = prob_setup.sort_values(by="prob", ascending=False)
probs_final = probs_done[:3]

# predict one hot encoded styles
encoded_predictions = model.predict_classes(np.array(user_input))

# decode the encoded styles
prediction_probs = probs_final["prob"]
prediction_labels = label_encoder.inverse_transform(probs_final["class"])

#print prediction and actual categories.
print(f"Predicted Pobabilties: {prediction_probs}")
print(f"Predicted classes: {prediction_labels}")

### END User Prediction