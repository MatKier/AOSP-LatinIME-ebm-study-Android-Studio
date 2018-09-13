import pandas as pd
import numpy as np
import math as maths
import matplotlib.pyplot as plt
import os

usecols_ = ["x", "y", "offsetX", "offsetY", "keyCenterX", "keyCenterY", "holdTime", "flightTime", "pressure"]
usecols = ["offsetX", "offsetY", "keyCenterX", "keyCenterY", "holdTime", "flightTime", "pressure"]

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

path_ = "C:/Users/mathi/OneDrive/Bachelor Stuff/Hauptstudie/Pilot/KeyStrokeLog/"
path = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Pilot/KeyStrokeLog/"
targetGroupPath = path + "ID_targetValues/"

pidList = os.listdir(path)
pidList.remove("ID_targetValues")
pidList.remove("read csv.py")

#One iteration = one Participant
for pid in pidList:
	taskGroupPath = path + pid + "/"

	taskGroupList = os.listdir(taskGroupPath)

	taskPathDict = {}
	targetPathDict = {}
	for taskGroup in taskGroupList:
		taskDirs = [task  for task in sorted(os.listdir(taskGroupPath + taskGroup))]
		taskPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs]
		targetPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs if not taskDir == "17_user-created password"]

	# One iteration = one taskgroup
	for key in sorted(taskPathDict.keys()):
		#One iteration = one task (3 csv files per task)
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
					if targetCsv.at[index, 'holdTime'] == 80:
						tempDefaultHoldTimeError.append(meanDistanceToTargetRrow['holdTime'])
					elif targetCsv.at[index, 'holdTime'] == 300:
						tempLongHoldTimeError.append(meanDistanceToTargetRrow['holdTime'])
					# FlightTime Error
					if targetCsv.at[index, 'flightTime'] == 260:
						tempDefaultFlightTimeError.append(meanDistanceToTargetRrow['flightTime'])
					elif targetCsv.at[index, 'flightTime'] == 1000:
						tempLongFlightTimeError.append(meanDistanceToTargetRrow['flightTime'])
					# Area Error
					if targetCsv.at[index, 'pressure'] == 0.20:
						tempDefaultAreaError.append(meanDistanceToTargetRrow['pressure'])
					elif targetCsv.at[index, 'pressure'] == 0.45:
						tempBigAreaError.append(meanDistanceToTargetRrow['pressure'])
					# Offset
					# groupedCsvList contains the grouped values for the current task,
					#'[" offsetX", " offsetY"].get_group(index).reset_index(drop=True)' returns a dataframe containing the (grouped)offsets for the event at index
					offsets = groupedCsvList["offsetX", "offsetY"].get_group(index).reset_index(drop=True)
					# Calculates the average distance between the target-offset and the users' offset (3 points for each event(index))
					distSum = 0
					for j in range(len(offsets)):
						distSum += maths.hypot(targetCsv.at[index, 'offsetX'] - offsets.at[j, 'offsetX'], targetCsv.at[index, 'offsetY'] - offsets.at[j, 'offsetY'])
					avgDist = distSum / len(offsets)

					if targetCsv.at[index, 'offsetX'] == 0 and targetCsv.at[index, 'offsetY'] == 0:
						tempCenterOffsetError.append(avgDist)
					elif targetCsv.at[index, 'offsetX'] == -45 and targetCsv.at[index, 'offsetY'] == 0:
						tempLeftOffsetError.append(avgDist)
					elif targetCsv.at[index, 'offsetX'] == 45 and targetCsv.at[index, 'offsetY'] == 0:
						tempRightOffsetError.append(avgDist)
					elif targetCsv.at[index, 'offsetX'] == 0 and targetCsv.at[index, 'offsetY'] == -80:
						tempTopOffsetError.append(avgDist)
					elif targetCsv.at[index, 'offsetX'] == 0 and targetCsv.at[index, 'offsetY'] == 80:
						tempBottomOffsetError.append(avgDist)

				# Calculate the mean of all the event means of the current task
				# and add it to its corresponding list
				# HoldTime
				defaultHoldTimeError.append([np.mean(tempDefaultHoldTimeError), taskId, pid])
				longHoldTimeError.append([np.mean(tempLongHoldTimeError), taskId, pid])
				# FlightTime
				defaultFlightTimeError.append([np.mean(tempDefaultFlightTimeError), taskId, pid])
				longFlightTimeError.append([np.mean(tempLongFlightTimeError), taskId, pid])
				# Area
				defaultAreaError.append([np.mean(tempDefaultAreaError), taskId, pid])
				bigAreaError.append([np.mean(tempBigAreaError), taskId, pid])
				# Offset
				centerOffsetError.append([np.mean(tempCenterOffsetError), taskId, pid])
				leftOffsetError.append([np.mean(tempLeftOffsetError), taskId, pid])
				rightOffsetError.append([np.mean(tempRightOffsetError), taskId, pid])
				topOffsetError.append([np.mean(tempTopOffsetError), taskId, pid])
				bottomOffsetError.append([np.mean(tempBottomOffsetError), taskId, pid])
	print 'finishied ' + pid

offset_means = (np.nanmean([error[0] for error in centerOffsetError]),
				np.nanmean([error[0] for error in leftOffsetError]),
				np.nanmean([error[0] for error in rightOffsetError]),
				np.nanmean([error[0] for error in topOffsetError]),
				np.nanmean([error[0] for error in bottomOffsetError]))
offset_std = (np.nanstd([error[0] for error in centerOffsetError]),
			  np.nanstd([error[0] for error in leftOffsetError]),
			  np.nanstd([error[0] for error in rightOffsetError]),
			  np.nanstd([error[0] for error in topOffsetError]),
			  np.nanstd([error[0] for error in bottomOffsetError]))

fig, ax = plt.subplots()

index = np.arange(len(offset_means))
bar_width = 0.35

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects = ax.bar(index, offset_means, bar_width,
			   alpha=opacity, color='g',
			   yerr=offset_std, error_kw=error_config)

ax.set_xlabel('Offset direction')
ax.set_ylabel('Error')
ax.set_title('Offset error by offset direction')
ax.set_xticks(index)
ax.set_xticklabels(('Center', 'Left', 'Righ', 'Top', 'Bottom'))
ax.legend()

fig.tight_layout()
plt.show()

area_means = (np.nanmean([error[0] for error in defaultAreaError]),
			  np.nanmean([error[0] for error in bigAreaError]))
area_std = (np.nanstd([error[0] for error in defaultAreaError]),
			np.nanstd([error[0] for error in bigAreaError]))

fig, ax = plt.subplots()

index = np.arange(len(area_means))
bar_width = 0.75

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects = ax.bar(index, area_means, bar_width,
			   alpha=opacity, color='b',
			   yerr=area_std, error_kw=error_config)

ax.set_xlabel('Area characteristic')
ax.set_ylabel('Error')
ax.set_title('Area error by area characteristic')
ax.set_xticks(index)
ax.set_xticklabels(('Default', 'Big'))
ax.legend()

fig.tight_layout()
plt.show()

flight_time_means = (np.nanmean([error[0] for error in defaultFlightTimeError]),
					 np.nanmean([error[0] for error in longFlightTimeError]))
flight_time_std = (np.nanstd([error[0] for error in defaultFlightTimeError]),
				   np.nanstd([error[0] for error in longFlightTimeError]))

fig, ax = plt.subplots()

index = np.arange(len(area_means))
bar_width = 0.75

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects = ax.bar(index, flight_time_means, bar_width,
			   alpha=opacity, color='r',
			   yerr=flight_time_std, error_kw=error_config)

ax.set_xlabel('Flight time characteristic')
ax.set_ylabel('Error')
ax.set_title('Flight time error by flight time characteristic')
ax.set_xticks(index)
ax.set_xticklabels(('Default', 'Long'))
ax.legend()

fig.tight_layout()
plt.show()

hold_time_means = (np.nanmean([error[0] for error in defaultHoldTimeError]),
				   np.nanmean([error[0] for error in longHoldTimeError]))
hold_time_std = (np.nanstd([error[0] for error in defaultHoldTimeError]),
				 np.nanstd([error[0] for error in longHoldTimeError]))

fig, ax = plt.subplots()

index = np.arange(len(area_means))
bar_width = 0.75

opacity = 0.4
error_config = {'ecolor': '0.3'}

rects = ax.bar(index, hold_time_means, bar_width,
			   alpha=opacity, color='y',
			   yerr=hold_time_std, error_kw=error_config)

ax.set_xlabel('Hold time characteristic')
ax.set_ylabel('Error')
ax.set_title('Hold time error by hold time characteristic')
ax.set_xticks(index)
ax.set_xticklabels(('Default', 'Long'))
ax.legend()

fig.tight_layout()
plt.show()