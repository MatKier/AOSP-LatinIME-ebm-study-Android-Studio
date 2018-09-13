import pandas as pd
import numpy as np
import math as maths
import matplotlib.pyplot as plt
import os

usecolsResult = ["eventType", "keyValue", "x", "y", "offsetX", "offsetY", "keyCenterX", "keyCenterY", "holdTime", "flightTime", "pressure"]
usecolsTarget = ["eventType",  "keyValue", "offsetX", "offsetY", "keyCenterX", "keyCenterY", "holdTime", "flightTime", "pressure"]

path_ = "C:/Users/mathi/OneDrive/Bachelor Stuff/Hauptstudie/Pilot/KeyStrokeLog/"
path = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Pilot/KeyStrokeLog/"
targetGroupPath = path + "ID_targetValues/"

pidList = os.listdir(path)
pidList.remove("ID_targetValues")
pidList.remove("read csv.py")
pidList.remove("read csv - Kopie.py")

values = []

#One iteration = one Participant
for pid in pidList:
	# Build filepaths for all tasks for current pid
	taskGroupPath = path + pid + "/"
	taskGroupList = os.listdir(taskGroupPath)
	taskPathDict = {}
	targetPathDict = {}
	for taskGroup in taskGroupList:
		# Filter out user created tasks
		if taskGroup != "17_user-created password":
			taskDirs = [task  for task in sorted(os.listdir(taskGroupPath + taskGroup))]
			taskPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs if not taskDir == "17_user-created password"]
			targetPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs if not taskDir == "17_user-created password"]

	# One iteration = one taskgroup
	for key in sorted(taskPathDict.keys()):
		#One iteration = one task (3 csv files per task)
		for task in sorted(taskPathDict[key]):
			# last 3 csv files in <task> read as a list of dataframes
			taskResultList = [pd.read_csv(taskGroupPath + task + "/" + entry, sep=';', header=0, usecols=usecolsResult) for entry in [taskEntry for taskEntry in sorted(os.listdir(taskGroupPath + task), reverse=True) if taskEntry.startswith('valid')][:3]]
			# target df for that specific result
			targetDf = pd.read_csv(targetGroupPath + task + "/" + os.listdir(targetGroupPath + task)[0], sep=';', header=0, usecols=usecolsTarget)
			targetDf = targetDf.add_prefix('target_')
			# Combine resultDataframes with target DF (horizontally)
			for resultDf in taskResultList:
				resultAndTargetTempDF = pd.concat([resultDf, targetDf], axis = 1)
				resultAndTargetTempDF["task"] = task[-2:]
				resultAndTargetTempDF["pId"] = pid
				values.append(resultAndTargetTempDF)
	print "Finished " + pid
masterDF = pd.concat(values, axis=0)
masterDF['area_error'] = masterDF.apply(lambda row: np.absolute(row['pressure'] - row['target_pressure']), axis=1)
masterDF['htime_error'] = masterDF.apply(lambda row: np.absolute(row['holdTime'] - row['target_holdTime']), axis=1)
masterDF['ftime_error'] = masterDF.apply(lambda row: np.absolute(row['flightTime'] - row['target_flightTime']), axis=1)
masterDF['offset_error'] = masterDF.apply(lambda row: maths.hypot(row['offsetX'] - row['target_offsetX'], row['offsetY'] - row['target_offsetY']), axis=1)
print "Finished concat"

defaultAreaError = masterDF[(masterDF['eventType'] == "up") & (masterDF['target_pressure'] == 0.2)][['area_error', 'task', 'pId']]
bigAreaError = masterDF[(masterDF['eventType'] == "up") & (masterDF['target_pressure'] == 0.45)][['area_error', 'task', 'pId']]

defaultHoldTimeError = masterDF[(masterDF['target_holdTime'] == 80)][['htime_error', 'task', 'pId']]
longHoldTimeError = masterDF[(masterDF['target_holdTime'] == 300)][['htime_error', 'task', 'pId']]

defaultFlightTimeError = masterDF[(masterDF['target_flightTime'] == 260)][['ftime_error', 'task', 'pId']]
longFlightTimeError = masterDF[(masterDF['target_flightTime'] == 1000)][['ftime_error', 'task', 'pId']]

centerOffsetError = masterDF[(masterDF['target_offsetX'] == 0) & (masterDF['target_offsetY'] == 0)][['offset_error', 'task', 'pId']]
leftOffsetError = masterDF[(masterDF['target_offsetX'] == -45) & (masterDF['target_offsetY'] == 0)][['offset_error', 'task', 'pId']]
rightOffsetError = masterDF[(masterDF['target_offsetX'] == 45) & (masterDF['target_offsetY'] == 0)][['offset_error', 'task', 'pId']]
topOffsetError = masterDF[(masterDF['target_offsetX'] == 0) & (masterDF['target_offsetY'] == -80)][['offset_error', 'task', 'pId']]
bottomOffsetError = masterDF[(masterDF['target_offsetX'] == 0) & (masterDF['target_offsetY'] == 80)][['offset_error', 'task', 'pId']]