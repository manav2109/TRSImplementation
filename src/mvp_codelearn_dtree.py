# -*- coding: utf-8 -*-
"""MVP_codelearn_DTree.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1H9WYjLvNf1IeCucBeWigy45zaUnsdB3S

## Part (a)
Import the data and save the data into a variable `X` and the targets into a variable `Y`.
"""

# Commented out IPython magic to ensure Python compatibility.
# Import suitable packages, load the dataset, and save data and targets into variables X and Y
# import packages
##TODO##
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
# %matplotlib inline

"""Load the data

"""

path2 = "/content/drive/MyDrive/MVP/Airbus_Part_numbersDTree.csv"
from google.colab import drive
drive.mount('/content/drive')

df_part = pd.read_csv(path2)
print(df_part)
#print(df_part.head())
print(df_part.iloc[:,0])
print(df_part.iloc[:,1])
print(df_part.shape)

# path3 = "/content/drive/MyDrive/MVP/Airbus_Part_numbersML.csv"  #save file
# df_part.to_csv(path3, index=False)

"""Feature Extraction Function"""

def extract_features(string):
    return {
        'contains_space': ' ' in string,
        'contains_hyphen': '-' in string,
        'pos0_isalpha': string[0].isalpha(),
        'pos4_isalpha': string[4].isalpha() if len(string) > 4 else False,
        'pos0_V': string[0] == 'V' if len(string) > 0 else False,
        'pos1_9': string[1:9].isdigit() if len(string) > 9 else False,  # Checks if characters 1 to 8 are digits
        'pos13': string[13] == 'B' if len(string) > 13 else False,
        'pos14': string[14] == 'S' if len(string) > 13 else False
    }

# Apply feature extraction
df_features = df_part['Code'].apply(lambda x: pd.Series(extract_features(x)))

path4 = "/content/drive/MyDrive/MVP/Airbus_Part_numbers_Features.csv"  #save file
df_features.to_csv(path4)

X = df_features  # Features
y = df_part['part_class']  # Target class labels

"""## Part (b)

Splt data 80:20
"""

# Import the package train_test_split from sklearn.model_selection.
# Split the dataset into Xtr, Xtest, Ytr, Ytest. Xtest and Ytest will form your held-out
# test set. You will later split Xtr and Ytr into training and validation sets.
from sklearn.model_selection import train_test_split

# The function returns splits of each array passed in.
# The proportion to be used as the training set is given by test_size
Xtr, Xtest, ytr, ytest = train_test_split (X, y, test_size=0.2,random_state=10)

#print(Xtr.shape, Xtest.shape)
#print(ytr.shape, ytest.shape)
# print(ytr[0:2])
# print(Xtr[3])
# print(np.linalg.norm(Xtr[3] - Xtr[5]))
#print(len(Xtr))
print(Xtr,Xtest)
#print(ytr,ytest)
print(Xtr.shape,Xtest.shape)

"""## Part (c)
Use library, and test against training data.

Check whether your predictions are the same as the predictions from `KNeighborsClassifier`.
"""

DT = DecisionTreeClassifier(max_depth=5)
DT.fit(Xtr, ytr)

y_pred_DT = DT.predict(Xtest)

print("DT_knn_test =", accuracy_score(y_pred_DT, ytest))  #accuracy score
#print(list(zip(Xtest, y_pred_DT)))
print(ytest)
print(y_pred_DT)
print(len(y_pred_DT))

y_prob = DT.predict_proba(Xtest)
print(np.max(y_prob, axis=1), y_pred_DT)
print(ytest[0:67])

new_strings = pd.Series(['8817VB 95M', 'W9296S000', 'V92369097810-BS99', 'V923690810-BS11'])
new_features = new_strings.apply(lambda x: pd.Series(extract_features(x)))
new_pred = DT.predict(new_features)
print(list(zip(new_strings, new_pred)))
new_prob = DT.predict_proba(new_features)
print(np.max(np.where(new_prob < 1, new_prob, np.nan), axis=1))