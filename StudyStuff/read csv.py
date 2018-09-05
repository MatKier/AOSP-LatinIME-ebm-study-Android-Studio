import pandas as pd
import numpy as np
import math as maths
import os

usecols_ = [" x", " y", " offsetX", " offsetY", " keyCenterX", " keyCenterY", " holdTime", " flightTime", " pressure"]
usecols = [" offsetX", " offsetY", " keyCenterX", " keyCenterY", " holdTime", " flightTime", " pressure"]

targetGroupPath = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Erster Durchgang/KeyStrokeLog/ID_targetValues/"
targetGroupPath_ = "C:\Users\mathi\OneDrive\Bachelor Stuff\Hauptstudie\Erster Durchgang\KeyStrokeLog\ID_targetValues/"

taskGroupPath = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Erster Durchgang/KeyStrokeLog/ID_0/"
taskGroupPath_ = "C:\Users\mathi\OneDrive\Bachelor Stuff\Hauptstudie\Erster Durchgang\KeyStrokeLog\ID_0/"
taskGroupList = os.listdir(taskGroupPath)

defaultHoldTimeError = []
longHoldTimeError = []

defaultFlightTimeError = []
longFlightTimeError = []

defaultAreaError = []
bigAreaError = []

centerOffsetError = []
leftOffsetError = []
rightOffsetError = []
topOffsetError = []
bottomOffsetError = []

taskPathDict = {}
targetPathDict = {}
for taskGroup in taskGroupList:
	taskDirs = [task  for task in sorted(os.listdir(taskGroupPath + taskGroup))]
	taskPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs]
	targetPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs if not taskDir == "17_user-created password"]

for key in sorted(taskPathDict.keys()):
	#print key
	# One iteration = one task (3 csv files per task)
	for task in sorted(taskPathDict[key]):
		# last 3 csv files in <task> read as a list of dataframes
		csvFileList = [pd.read_csv(taskGroupPath + task + "/" + entry, sep=';', header=0, usecols=usecols) for entry in [taskEntry for taskEntry in sorted(os.listdir(taskGroupPath + task), reverse=True) if taskEntry.startswith('valid')][:3]]
		# combines the 3 dataframes into one group
		groupedCsvList = pd.concat(csvFileList).groupby(level=0)
		mean = groupedCsvList.mean()

		if task[:2] != "17":
			targetCsv = pd.read_csv(targetGroupPath + task + "/" + os.listdir(targetGroupPath + task)[0], sep=';', header=0, usecols=usecols)
			meanDistanceToTarget = targetCsv.subtract(mean, fill_value=0)

			# Temp lists for calculating the mean error of all events for the current task and feature
			tempDefaultHoldTimeError = []
			tempLongHoldTimeError = []
			tempDefaultFlightTimeError = []
			tempLongFlightTimeError = []
			tempDefaultAreaError = []
			tempBigAreaError = []
			tempCenterOffsetError = []
			tempLeftOffsetError = []
			tempRightOffsetError = []
			tempTopOffsetError = []
			tempBottomOffsetError = []

			taskId = task[-2:]
			# Iterate over the mean error of all touch events in this task and add the mean error for every event to its corresponding tempList
			# One iteration = one touch event (up or down)
			for index, meanDistanceToTargetRrow in meanDistanceToTarget.iterrows():
				# HoldTime Error
				if targetCsv.at[index, ' holdTime'] == 80:
					tempDefaultHoldTimeError.append(meanDistanceToTargetRrow[' holdTime'])
				elif targetCsv.at[index, ' holdTime'] == 300:
					tempLongHoldTimeError.append(meanDistanceToTargetRrow[' holdTime'])
				# FlightTime Error
				if targetCsv.at[index, ' flightTime'] == 260:
					tempDefaultFlightTimeError.append(meanDistanceToTargetRrow[' flightTime'])
				elif targetCsv.at[index, ' flightTime'] == 1000:
					tempLongFlightTimeError.append(meanDistanceToTargetRrow[' flightTime'])
				# Area Error
				if targetCsv.at[index, ' pressure'] == 0.20:
					tempDefaultAreaError.append(meanDistanceToTargetRrow[' pressure'])
				elif targetCsv.at[index, ' pressure'] == 0.45:
					tempBigAreaError.append(meanDistanceToTargetRrow[' pressure'])
				# Offset
				# groupedCsvList contains the grouped values for the current task,
				#'[" offsetX", " offsetY"].get_group(index).reset_index(drop=True)' returns a dataframe containing the (grouped)offsets for the event at index
				offsets = groupedCsvList[" offsetX", " offsetY"].get_group(index).reset_index(drop=True)
				# Calculates the average distance between the target-offset and the users' offset (3 points for each event(index))
				distSum = 0
				for j in range(len(offsets)):
					distSum += maths.hypot(targetCsv.at[index, ' offsetX'] - offsets.at[j, ' offsetX'], targetCsv.at[index, ' offsetY'] - offsets.at[j, ' offsetY'])
				avgDist = distSum / len(offsets)

				if targetCsv.at[index, ' offsetX'] == 0 and targetCsv.at[index, ' offsetY'] == 0:
					tempCenterOffsetError.append(avgDist)
				elif targetCsv.at[index, ' offsetX'] == -45 and targetCsv.at[index, ' offsetY'] == 0:
					tempLeftOffsetError.append(avgDist)
				elif targetCsv.at[index, ' offsetX'] == 45 and targetCsv.at[index, ' offsetY'] == 0:
					tempRightOffsetError.append(avgDist)
				elif targetCsv.at[index, ' offsetX'] == 0 and targetCsv.at[index, ' offsetY'] == -80:
					tempTopOffsetError.append(avgDist)
				elif targetCsv.at[index, ' offsetX'] == 0 and targetCsv.at[index, ' offsetY'] == 80:
					tempBottomOffsetError.append(avgDist)

			# Calculate the mean of all the event means of the current task
			# and add it to its corresponding list
			# HoldTime
			defaultHoldTimeError.append([np.mean(tempDefaultHoldTimeError), taskId])
			longHoldTimeError.append([np.mean(tempLongHoldTimeError), taskId])
			# FlightTime
			defaultFlightTimeError.append([np.mean(tempDefaultFlightTimeError), taskId])
			longFlightTimeError.append([np.mean(tempLongFlightTimeError), taskId])
			# Area
			defaultAreaError.append([np.mean(tempDefaultAreaError), taskId])
			bigAreaError.append([np.mean(tempBigAreaError), taskId])
			# Offset
			centerOffsetError.append([np.mean(tempCenterOffsetError), taskId])
			leftOffsetError.append([np.mean(tempLeftOffsetError), taskId])
			rightOffsetError.append([np.mean(tempRightOffsetError), taskId])
			topOffsetError.append([np.mean(tempTopOffsetError), taskId])
			bottomOffsetError.append([np.mean(tempBottomOffsetError), taskId])

print 'suc'