# dependencies
from keras.models import load_model
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
import numpy as np
import pandas as pd

### START re-establish preprocessing standards
#import original data
all_beer_df = pd.read_csv("data/data_add_3param_cluster.csv", encoding="latin1")

#trim data to needed X colums
beer_char = all_beer_df[["ABV","IBU","Color"]]

#Set beer_char as X 
X=beer_char

#set y data
y=all_beer_df["Category"]

#create an array of unique values from the output dataset
style_array = pd.unique(y.values)

#set the count as the length of the output array
style_count = len(style_array)

# setup train and test split of orginal data
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, stratify=y)

# Step 1: Label-encode data set
label_encoder = LabelEncoder()
label_encoder.fit(y_train)
encoded_y_train = label_encoder.transform(y_train)
encoded_y_test = label_encoder.transform(y_test)

# Step 2: Convert encoded labels to one-hot-encoding
y_train_categorical = to_categorical(encoded_y_train)
y_test_categorical = to_categorical(encoded_y_test)
### END preprocessing

### START model processing for user prediction
def user_predict(params):
    # load model
    model = load_model("models/beer_categories_3p_unscaled.h5")

    # call user inputs from app
    input_beer_params = [params]

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
    encoded_predictions = model.predict_classes(np.array(input_beer_params))

    # decode the encoded styles
    prediction_probs = probs_final["prob"].tolist()
    prediction_labels = label_encoder.inverse_transform(probs_final["class"]).tolist()

    # establish prediction output as dictionary
    final_prediction = dict(zip(prediction_labels, prediction_probs))
    
    #print prediction categories and probabilities
    return final_prediction
    ### END user Prediction

if __name__ == '__main__':
    user_predict()