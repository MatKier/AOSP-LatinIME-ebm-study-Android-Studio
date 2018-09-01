import pandas as pd
import os

usecols_ = [" x", " y", " offsetX", " offsetY", " keyCenterX", " keyCenterY", " holdTime", " flightTime", " pressure"]
usecols = [" offsetX", " offsetY", " keyCenterX", " keyCenterY", " holdTime", " flightTime", " pressure"]

targetGroupPath = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Erster Durchgang/KeyStrokeLog/ID_targetValues/"
taskGroupPath = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Erster Durchgang/KeyStrokeLog/ID_0/"
taskGroupList = os.listdir(taskGroupPath)

taskPathDict = {}
targetPathDict = {}
for taskGroup in taskGroupList:
	taskDirs = [task  for task in sorted(os.listdir(taskGroupPath + taskGroup))]
	taskPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs]
	targetPathDict[taskGroup] = [(taskGroup + "/" + taskDir)  for taskDir in taskDirs if not taskDir == "17_user-created password"]

for key in sorted(taskPathDict.keys()):
	print key
	for task in sorted(taskPathDict[key]):
		# last 3 csv files in <task> read as a list of dataframes
		csvFileList = [pd.read_csv(taskGroupPath + task + "/" + entry, sep=';', header=0, usecols=usecols) for entry in [taskEntry for taskEntry in sorted(os.listdir(taskGroupPath + task), reverse=True) if taskEntry.startswith('valid')][:3]]
		# combines the 3 dataframes into one dataframe
		groupedCsvList = pd.concat(csvFileList).groupby(level=0)

		max = groupedCsvList.max()
		min = groupedCsvList.min()
		mean = groupedCsvList.mean()

		print task[-7:]
		if task[:2] != "17":
			targetCsv = pd.read_csv(targetGroupPath + task + "/" + os.listdir(targetGroupPath + task)[0], sep=';', header=0, usecols=usecols)
			print "Max distance to target"
			print targetCsv.subtract(max, fill_value=0)
			print "Min distance to target"
			print targetCsv.subtract(min, fill_value=0)
			print "Mean distance to target"
			print targetCsv.subtract(mean, fill_value=0)
		else :
			print "Max"
			print max
			print "Min"
			print min
			print "Mean"
			print mean