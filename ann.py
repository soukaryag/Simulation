import sklearn as sk
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd

def load_data():
    return pd.read_csv("data.csv")

data = load_data()
train_set, test_set = train_test_split(data, test_size=0.2, random_state=42)

# print(train_set)
# print(test_set)

data_temp = train_set.drop("mov", axis=1)
y_train = train_set["mov"].copy()

data_test_temp = test_set.drop("mov", axis=1)
y_test = test_set["mov"].copy()

num_pipeline = Pipeline([
        ('std_scaler', StandardScaler())
    ])

X_train = (num_pipeline.fit_transform(data_temp))
X_test = (num_pipeline.fit_transform(data_test_temp))


import tensorflow as tf
config = tf.contrib.learn.RunConfig(tf_random_seed=42)

feature_cols = tf.contrib.learn.infer_real_valued_columns_from_input(X_train)
dnn_clf = tf.contrib.learn.DNNClassifier(hidden_units=[5,6,5], n_classes=5, feature_columns=feature_cols, config=config)
dnn_clf = tf.contrib.learn.SKCompat(dnn_clf)
dnn_clf.fit(X_train, y_train, batch_size=100, steps=10000)


# from sklearn.tree import DecisionTreeRegressor
# dnn_clf = DecisionTreeRegressor(random_state=42)
# dnn_clf.fit(X_train, y_train)

def fit(this):
    global dnn_clf
    a = np.array(this)
    a = a.reshape(1, -1)
    a = (num_pipeline.fit_transform(a))
    y_pred = dnn_clf.predict(a)
    return int(y_pred['classes'][0])



for q in range(4):
    for w in range(4):
        print(fit([q,4-q,w,4-w]))
