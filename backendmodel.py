import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def Model(data):
    df = pd.read_csv("maternalhealthriskdata.csv")

    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    le = LabelEncoder()
    y = le.fit_transform(y)

    X = np.array(X)
    y = np.array(y)
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= 0.2, random_state = 0)

    sc_X = StandardScaler()
    X_train = sc_X.fit_transform(X_train)

    rf = RandomForestClassifier(n_estimators=250, criterion='entropy', random_state=50)
    rf.fit(X_train, y_train)

    data = sc_X.transform(data)
    y_pred = rf.predict(data)

    return y_pred[0]

if (__name__ == "__main__"):
    y_pred = Model([[35, 100, 70, 6.1, 98, 66]])
    print(y_pred)