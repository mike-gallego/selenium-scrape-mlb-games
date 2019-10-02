import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle

data = pd.read_csv('mlb_games_overview.csv')
data = data[['away', 'at_bats', 'runs', 'hits', 'rbis', 'walks', 'batting_average', 'on_base_percentage', 'slugging_percentage', 'win']]

predict = 'win'

x = np.array(data.drop([predict], 1))

y = np.array(data[predict])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)

'''
best = 0
for _ in range(20000):
    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.1)
    linear = linear_model.LinearRegression()
    linear.fit(x_train, y_train)
    acc = linear.score(x_test, y_test)

    if acc > best:
        best = acc
        print('The new best is: %s' % best)
        with open('mlb_prediction_model.pickle', 'wb') as f:
            pickle.dump(linear, f)
'''

pickle_in = open('mlb_prediction_model.pickle', 'rb')
linear = pickle.load(pickle_in)

predictions = linear.predict(x_test)

for x in range(len(predictions)):
    print(predictions[x], x_test[x], y_test[x])

