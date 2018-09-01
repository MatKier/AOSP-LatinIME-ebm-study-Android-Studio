import pandas as pd
import os

usecols = [" x", " y", " offsetX", " offsetY", " keyCenterX", " keyCenterY", " holdTime", " flightTime", " pressure"] 

taskGroupPath = "E:/OneDrive/Bachelor Stuff/Hauptstudie/Erster Durchgang/KeyStrokeLog/ID_0/"
taskGroupList = os.listdir(taskGroupPath)

taskPathDict = {}
for taskGroup in taskGroupList:
	taskPathDict[taskGroup] = [(taskGroupPath + taskGroup + "/" + task)  for task in sorted(os.listdir(taskGroupPath + taskGroup))]

for key in sorted(taskPathDict.keys()):
	print key
	for task in sorted(taskPathDict[key]):	
		# last 3 csv files in <task> read as a list of dataframes
		csvFileList = [pd.read_csv(task + "/" + entry, sep=';', header=0, usecols=usecols) for entry in [taskEntry for taskEntry in sorted(os.listdir(task), reverse=True) if taskEntry.startswith('valid')][:3]]
		# combines the 3 dataframes into one dataframe
		groupedCsvList = pd.concat(csvFileList).groupby(level=0)
		
		print task[-7:]
		print "Max"
		print(groupedCsvList.max())
		print "Min"
		print(groupedCsvList.min())
		print "Mean"
		print(groupedCsvList.mean())