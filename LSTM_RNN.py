from __future__ import division
import sys
import os
import time
import QueryRecommender as QR
from bitmap import BitMap
import math
import heapq
import TupleIntent as ti
import ParseConfigFile as parseConfig

import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm
import matplotlib.pyplot as plt
import keras
from keras.datasets import imdb
from keras.preprocessing import sequence
from keras import regularizers
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Activation, SimpleRNN, Dense, TimeDistributed, Flatten, LSTM, Dropout, GRU
'''
# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back):
        a = dataset[i:(i+look_back)]
        dataX.append(a)
        dataY.append(dataset[(i + 1): (i + 1 + look_back)])
    return np.array(dataX), np.array(dataY)

def create_input_output_pairs(dataset, timesteps):
    dataX, dataY = [], []

    for i in range(len(dataset) - timesteps):
        if dataset[i][0] != dataset[i + timesteps][0]:
            continue

        instance_x = []
        for j in range(i, i + timesteps):
            row_x = []
            for c in dataset[j][2]:
                row_x.extend(c)
            instance_x.append(row_x)
        dataX.append(instance_x)


        row_y = []
        for c in dataset[i + timesteps][2]:
            row_y.extend(c)
        dataY.append(row_y)

    return np.array(dataX), np.array(dataY)

def create_training_dataset2(dataset):
    dataX, dataY = [], []

    current_session = dataset[0][0]
    start_index = 0

    for i in range(1, len(dataset)):
        if dataset[i][0] != current_session:
            current_session = dataset[i][0]
            start_index = i
        else:

            instance_x = []
            instance_y = []
            for j in reversed(range(start_index, i)):
                row_x = []
                for c in dataset[j][2]:
                    row_x.extend(c)
                instance_x.insert(0, row_x)

                row_y = []
                for c in dataset[j + 1][2]:
                    row_y.extend(c)
                instance_y.insert(0, row_y)

                dataX.append(instance_x)
                dataY.append(instance_y)

    return np.array(dataX), np.array(dataY)

def create_training_dataset(dataset):
    session_dict = {}
    dataX, dataY = [], []

    for i in range(len(dataset)):
        if dataset[i][0] not in session_dict:
            session_dict[dataset[i][0]] = []
            session_dict[dataset[i][0]].append(dataset[i][2])
        else:
            session_dict[dataset[i][0]].append(dataset[i][2])

            session_data = session_dict[dataset[i][0]]

            row_y = []
            for c in session_data[len(session_data) - 1]:
                row_y.extend(c)

            instance_x = []
            #instance_y = []
            for j in range(len(session_data) - 1):
                row_x = []
                for c in session_data[j]:
                    row_x.extend(c)
                instance_x.append(row_x)

            dataX.append(instance_x)
            #dataY.append(instance_y)
            dataY.append([row_y])

    return np.array(dataX), np.array(dataY)

#start of main block where execution will begin
if __name__ == '__main__':

    # fix random seed for reproducibility
    np.random.seed(2000)

    #open the file having intent vectors
    file_name = 'InterleavedSessions/NYCBitFragmentIntentSessions'
    obj = pd.read_csv(file_name, sep=";", header=None)
    data = obj.values

    #processing data to remove unnecessary parts
    m, n = data.shape
    records = []
    sequences = []
    for index in range(m):
        parts = data[index][0].split(", ")
        session_parts = parts[0].split(" ")
        query_parts = parts[1].split(" ")
        records.insert(index, [session_parts[1], query_parts[1], data[index][2]])
        sequences.insert(index, data[index][2])

    records = np.array(records)
    sequences = np.array(sequences)

    # split into train and test sets
    train_size = int(len(records) * 0.806)
    test_size = len(records) - train_size
    train, test = records[0:train_size], records[train_size:len(records)]

    x_train, y_train = create_training_dataset(train)
    x_test, y_test = create_training_dataset(test)

    n_features = len(x_train[0][0])
    print(n_features)
    #n_features = 256
    #n_timesteps = 5



    model=Sequential()
    model.add(LSTM(n_features, input_shape = (None, n_features), return_sequences = True))
    model.add(SimpleRNN(n_features, input_shape=(None, n_features), return_sequences=True))
    model.add(GRU(n_features, input_shape=(None, n_features), return_sequences=True))
    #model.add(Dropout(0.1))
    model.add(Dense(n_features, activation  =  "sigmoid"))
    model.compile(loss = "binary_crossentropy", optimizer = "rmsprop", metrics=['accuracy'])


    #model.fit(x_train.reshape, y_train, epochs=5, batch_size = 1)

    for i in range(len(x_train)):
        sample_input = np.array(x_train[i])
        sample_output = np.array(y_train[i])
        model.fit(sample_input.reshape(1, sample_input.shape[0], sample_input.shape[1]), sample_output.reshape(1, sample_output.shape[0], sample_output.shape[1]), epochs = 1)

    #k = 3
    k = len(x_test) - 1
    test_sample = np.array(x_test[k])
    prediction = model.predict(test_sample.reshape(1, test_sample.shape[0], test_sample.shape[1]))
    #print(np.array(y_test[k]).astype(np.int), "\n")
    test_output = np.array(y_test[k])
    print(np.array(test_output[test_output.shape[0] - 1]).astype(np.int), "\n")
    #labels = (prediction > 0.05).astype(np.int)
    print(prediction[0][prediction.shape[1] - 1])

    similarity = []
    index_values = []
    for i in range(len(x_test)):
        test_sample = np.array(x_test[i])
        prediction = model.predict(test_sample.reshape(1, test_sample.shape[0], test_sample.shape[1]))
        prediction = prediction[0][prediction.shape[1] - 1]
        actual_vector = np.array(y_test[i])
        actual_vector = np.array(actual_vector[actual_vector.shape[0] - 1]).astype(np.int)
        cos_sim = dot(prediction, actual_vector)/(norm(prediction) * norm(actual_vector))
        similarity.insert(i, cos_sim)
        index_values.insert(i, i)

    #print(similarity)
    plt.plot(index_values, similarity)
    plt.xlabel("Serial of test samples")
    plt.ylabel("Similarity")
    plt.title("Cosine Similarity")
    plt.show()

'''

def createCharListFromIntent(prevIntent, configDict):
    intentStrList = None
    if configDict['BIT_OR_WEIGHTED'] == 'BIT':
        intentStr = prevIntent.tostring()
        for i in range(len(intentStr)):
            intentStrList.add(intentStr[i])
    elif configDict['BIT_OR_WEIGHTED'] == 'WEIGHTED':
        intentStrList = prevIntent.split(';')
    return intentStrList

def appendTrainingXY(sessIntentList, configDict, dataX, dataY):
    numQueries = len(sessIntentList)
    xList = []
    for i in range(numQueries-1):
        prevIntent = sessIntentList[i]
        intentStrList = createCharListFromIntent(prevIntent, configDict)
        xList.append(intentStrList)
    yList = createCharListFromIntent(sessIntentList[numQueries-1], configDict)
    dataX.append(xList)
    dataY.append(yList)
    return (dataX, dataY)

def updateRNNIncrementalTrain(modelRNN, x_train, y_train):
    for i in range(len(x_train)):
        sample_input = np.array(x_train[i])
        sample_output = np.array(y_train[i])
        modelRNN.fit(sample_input.reshape(1, sample_input.shape[0], sample_input.shape[1]), sample_output.reshape(1, sample_output.shape[0], sample_output.shape[1]), epochs = 1)
        return modelRNN

def initializeRNN(n_features, configDict):
    modelRNN = Sequential()
    assert configDict['RNN_BACKPROP_LSTM_GRU'] == 'LSTM' or configDict['RNN_BACKPROP_LSTM_GRU'] == 'BACKPROP' or configDict['RNN_BACKPROP_LSTM_GRU'] == 'GRU'
    if configDict['RNN_BACKPROP_LSTM_GRU'] == 'LSTM':
        modelRNN.add(LSTM(n_features, input_shape=(None, n_features), return_sequences=True))
    elif configDict['RNN_BACKPROP_LSTM_GRU'] == 'BACKPROP':
        modelRNN.add(SimpleRNN(n_features, input_shape=(None, n_features), return_sequences=True))
    elif configDict['RNN_BACKPROP_LSTM_GRU'] == 'GRU':
        modelRNN.add(GRU(n_features, input_shape=(None, n_features), return_sequences=True))
    # model.add(Dropout(0.1))
    modelRNN.add(Dense(n_features, activation="sigmoid"))
    modelRNN.compile(loss="binary_crossentropy", optimizer="rmsprop", metrics=['accuracy'])
    return modelRNN

def refineTemporalPredictor(queryLinesSetAside, configDict, sessionDict, modelRNN):
    dataX = []
    dataY = []
    for line in queryLinesSetAside:
        (sessID, queryID, curQueryIntent) = QR.retrieveSessIDQueryIDIntent(line, configDict)
        if sessID in sessionDict:
            sessionDict[sessID].append(curQueryIntent)
        else:
            sessionDict[sessID] = []
            sessionDict[sessID].append(curQueryIntent)
        (dataX, dataY) = appendTrainingXY(sessionDict[sessID], configDict, dataX, dataY)
        n_features = len(dataX[0][0])
        if modelRNN is None:
            modelRNN = initializeRNN(n_features, configDict)
        else:
            modelRNN = updateRNNIncrementalTrain(modelRNN, dataX, dataY)
    return (modelRNN, sessionDict)

def predictTopKIntents(sessIntentList, modelRNN, configDict):
    # top-K is 1
    numQueries = len(sessIntentList)
    testX = []
    for i in range(numQueries - 1):
        prevIntent = sessIntentList[i]
        intentStrList = createCharListFromIntent(prevIntent, configDict)
        testX.append(intentStrList)
    predictedY = modelRNN.predict(testX.reshape(1, testX.shape[0], testX.shape[1]))
    predictedY = predictedY[0][predictedY.shape[1] - 1]
    return predictedY

def executeRNN(intentSessionFile, configDict):
    sessionDict = {}  # key is session ID and value is a list of query intent vectors; no need to store the query itself
    numEpisodes = 0
    queryLinesSetAside = []
    episodeResponseTime = {}
    startEpisode = time.time()
    outputIntentFileName = configDict['OUTPUT_DIR'] + "/OutputFileShortTermIntent_" + \
                           configDict['ALGORITHM']+"_"+ configDict["RNN_BACKPROP_LSTM_GRU"]+ \
                           configDict['INTENT_REP'] + "_" + \
                           configDict['BIT_OR_WEIGHTED'] + "_TOP_K_" + configDict['TOP_K'] + "_EPISODE_IN_QUERIES_" + \
                           configDict['EPISODE_IN_QUERIES']
    try:
        os.remove(outputIntentFileName)
    except OSError:
        pass
    numQueries = 0
    with open(intentSessionFile) as f:
        predictedY = None
        modelRNN = None
        for line in f:
            (sessID, queryID, curQueryIntent) = QR.retrieveSessIDQueryIDIntent(line, configDict)
            # Here we are putting together the predictedIntent from previous step and the actualIntent from the current query, so that it will be easier for evaluation
            elapsedAppendTime = 0.0
            if predictedY is not None:
                curIntentList = createCharListFromIntent(curQueryIntent, configDict)
                actual_vector = np.array(curIntentList)
                actual_vector = np.array(actual_vector[actual_vector.shape[0] - 1]).astype(np.int)
                cos_sim = dot(predictedY, actual_vector) / (norm(predictedY) * norm(actual_vector))
                elapsedAppendTime = QR.appendPredictedIntentsRNN(predictedY, cos_sim, sessID,
                                                                    queryID, curQueryIntent, numEpisodes,
                                                                    configDict, outputIntentFileName)
            numQueries += 1
            queryLinesSetAside.append(line)
            # -- Refinement is done only at the end of episode, prediction could be done outside but no use for CF and response time update also happens at one shot --
            if numQueries % int(configDict['EPISODE_IN_QUERIES']) == 0:
                numEpisodes += 1
                (modelRNN, sessionDict) = refineTemporalPredictor(queryLinesSetAside, configDict, sessionDict, modelRNN)
                del queryLinesSetAside
                queryLinesSetAside = []
            if modelRNN is not None:
                predictedY = predictTopKIntents(modelRNN, sessionDict[sessID], configDict)
            (episodeResponseTime, startEpisode) = QR.updateResponseTime(episodeResponseTime, numEpisodes,
                                                                            startEpisode, elapsedAppendTime)
    episodeResponseTimeDictName = configDict['OUTPUT_DIR'] + "/ResponseTimeDict_" + configDict['INTENT_REP'] + "_" + \
                                  configDict['BIT_OR_WEIGHTED'] + "_TOP_K_" + configDict[
                                      'TOP_K'] + "_EPISODE_IN_QUERIES_" + configDict['EPISODE_IN_QUERIES'] + ".pickle"
    QR.writeToPickleFile(episodeResponseTimeDictName, episodeResponseTime)
    return (outputIntentFileName, episodeResponseTimeDictName)







