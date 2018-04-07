from simple_esn import SimpleESN
from sklearn.linear_model import Ridge
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from numpy import loadtxt, atleast_2d
import matplotlib.pyplot as plt
from pprint import pprint
from time import time
import numpy as np
import torch


if __name__ == '__main__':
    X = loadtxt('MackeyGlass_t17.txt')
    X = atleast_2d(X).T
    train_length = 2000
    test_length = 2000
    # data shape should be (lens_ts, n_features)
    train_input = X[:train_length]
    train_target = X[1:train_length+1]
    test_input = X[train_length:train_length+test_length]
    test_target = X[train_length+1:train_length+test_length+1]

    # # load data and make training set
    # data = torch.load('MackeyGlass_t17.txt')
    # # data shape should be (lens_ts, n_features)
    # train_input = data[0, :-1]
    # train_input=atleast_2d(train_input).T
    # train_target = data[0, 1:]
    # train_target=atleast_2d(train_target).T

    # test_input=data[-1,:-1]
    # test_input=atleast_2d(test_input).T
    # test_target=data[-1,1:]
    # test_target=atleast_2d(test_target).T

    # Simple training
    model_esn = SimpleESN(n_readout=1000, n_components=1000,
                          damping=0.3, weight_scaling=1.25)
    echo_train_state = model_esn.fit_transform(train_input)
    regr = Ridge(alpha=0.01)
    regr.fit(echo_train_state, train_target)

    # show the train result
    echo_train_target, echo_train_pred= train_target, regr.predict(echo_train_state)

    err_train = mean_squared_error(echo_train_target, echo_train_pred)

    data_figures = plt.figure(figsize=(12, 4))
    trainplot = data_figures.add_subplot(1, 3, 1)
    trainplot.plot(train_input[:], 'b')
    trainplot.set_title('training signal')

    echoplot = data_figures.add_subplot(1, 3, 2)
    # echoplot.plot(echo_train_state[0, :20])
    echoplot.plot(echo_train_state[:, :20])
    echoplot.set_title('Some reservoir activation')

    testplot = data_figures.add_subplot(1, 3, 3)
    testplot.plot(train_target[:], 'r', label='train signal')
    testplot.plot(echo_train_pred[:], 'g', label='prediction')
    testplot.set_title('Prediction (MSE %0.8f)' % err_train)

    testplot.legend(loc='upper right')
    plt.tight_layout(0.5)
    plt.savefig('MackeyGlass_ESN_Train_Prediction.png')

    # show the test result
    echo_test_state=model_esn.transform(test_input)
    echo_test_target, echo_test_pred = test_target, regr.predict(echo_test_state)
    
    err_test = mean_squared_error(echo_test_target, echo_test_pred)

    data_figures = plt.figure(figsize=(12, 4))
    trainplot = data_figures.add_subplot(1, 3, 1)
    trainplot.plot(test_input[:], 'b')
    trainplot.set_title('training signal')

    echoplot = data_figures.add_subplot(1, 3, 2)
    echoplot.plot(echo_test_state[:, :20])
    echoplot.set_title('Some reservoir activation')

    testplot = data_figures.add_subplot(1, 3, 3)
    testplot.plot(test_target[:], 'r', label='test signal')
    testplot.plot(echo_test_pred[:], 'g', label='prediction')
    testplot.set_title('Prediction (MSE %0.8f)' % err_test)

    testplot.legend(loc='upper right')
    plt.tight_layout(0.5)
    plt.savefig('MackeyGlass_ESN_Test_Prediction.png')
