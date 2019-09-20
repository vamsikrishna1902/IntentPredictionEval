#!/bin/sh
#python QLearning_selOpConst.py -config configDir/BusTracker_QL_sustenance_configFile.txt
#python QLearning_selOpConst.py -config configDir/BusTracker_QL_configFile.txt
#python CF_SVD_selOpConst.py -config configDir/BusTracker_SVD_sustenance_configFile.txt
#python CFCosineSim_Parallel.py -config configDir/BusTracker_CF_COSINESIM_sustenance_configFile.txt
#python ActiveLearning_Parallel.py -config BusTracker_configFile.txt
python LSTM_RNN_Parallel_selOpConst.py -config configDir/BusTracker_Novel_GRU_trainTest_sustenance_0.8_configFile.txt
python CreateSQLLogs.py -config configDir/BusTracker_Novel_GRU_trainTest_sustenance_0.8_configFile.txt
#python ActiveLearning_Parallel.py -config configDir/BusTracker_configFile_1Fold_Random_Sample_1.0_Incremental_Weight_0.2_Top_3_Last_3.txt
#python ActiveLearning_Parallel.py -config configDir/BusTracker_configFile_1Fold_Random_Sample_1.0_Incremental_Weight_0.4_Top_3_Last_3.txt
#python ActiveLearning_Parallel.py -config configDir/BusTracker_configFile_1Fold_Random_Sample_1.0_Incremental_Weight_0.6_Top_3_Last_3.txt
#python ActiveLearning_Parallel.py -config configDir/BusTracker_configFile_1Fold_Random_Sample_1.0_Incremental_Weight_0.8_Top_3_Last_3.txt
#sudo shutdown
