import os
import joblib
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split


def extract_features(string):
    return {
        'contains_space': ' ' in string,
        'contains_hyphen': '-' in string,
        'pos0_isalpha': string[0].isalpha(),
        'pos4_isalpha': string[4].isalpha() if len(string) > 4 else False,
        'pos0_V': string[0] == 'V' if len(string) > 0 else False,
        'pos1_9': string[1:9].isdigit() if len(string) > 9 else False,  # Checks if characters 1 to 8 are digits
        'pos13': string[13] == 'B' if len(string) > 13 else False,
        'pos14': string[14] == 'S' if len(string) > 14 else False
    }


def train_ml_model_for_airbus_part_numbers():
    current_directory = os.getcwd()
    path2 = os.path.join(current_directory, "TestData", "SampleTRSSheets", "Airbus_Part_numbersDTree.csv")
    df_part = pd.read_csv(path2)

    # Apply feature extraction
    df_features = df_part['Code'].apply(lambda x: pd.Series(extract_features(x)))

    # path4 = r"C:\Users\Public\Airbus_Part_numbers_Features.csv"  # save file
    # df_features.to_csv(path4)

    X = df_features  # Features, note it is to be trained against extracted features
    y = df_part['part_class']  # Target class labels

    # Import the package train_test_split from sklearn.model_selection.
    # Split the dataset into Xtr, Xtest, Ytr, Ytest. Xtest and Ytest will form your held-out
    # test set. You will later split Xtr and Ytr into training and validation sets.

    # The function returns splits of each array passed in.
    # The proportion to be used as the training set is given by test_size
    Xtr, Xtest, ytr, ytest = train_test_split(X, y, test_size=0.2, random_state=10)
    # Use library, and test against training data.
    DT = DecisionTreeClassifier(max_depth=5)
    DT.fit(Xtr, ytr)  # Fit training data
    # y_prediction_DT = DT.predict(Xtest)  # predict against test data

    # Save the model to a file
    model_path = os.path.join(current_directory, "routers", "decision_tree_model.joblib")
    joblib.dump(DT, model_path)


def predict_airbus_part_number(possible_number_strings):
    # possible_number_strings is array of strings
    new_strings = pd.Series(possible_number_strings)
    new_features = new_strings.apply(lambda x: pd.Series(extract_features(x)))

    # Load the model from the file
    current_directory = os.getcwd()
    model_path = os.path.join(current_directory, "routers", "decision_tree_model.joblib")
    DT = joblib.load(model_path)

    predictions = DT.predict(new_features)
    new_prob = DT.predict_proba(new_features)
    # print(f"new_prob ===== {new_prob}")
    prediction = np.max(np.where(new_prob < 1, new_prob, np.nan), axis=1)
    # print(f"predictions ===== {prediction}")

    return prediction

# # predict against new data
# new_strings = pd.Series(['8817VB 95M', 'W9296S000', 'V92369097810-BS99', 'V923690810-BS11']) #you can change and test against random set
# new_features = new_strings.apply(lambda x: pd.Series(extract_features(x)))
# new_pred = DT.predict(new_features)
# print(list(zip(new_strings, new_pred)))
# new_prob = DT.predict_proba(new_features)
# print(np.max(np.where(new_prob < 1, new_prob, np.nan), axis=1))

