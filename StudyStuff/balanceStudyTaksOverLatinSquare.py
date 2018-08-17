import xml.etree.ElementTree as ET

zero_f_c = 0;
zero_f_ls = ["3", "1", "2",
             "1", "2", "3",
             "2", "3", "1"]  
		   
one_f_c = 0;
one_f_ls = ["4", "3", "1", "2",
            "3", "4", "2", "1",
		    "1", "2", "4", "3",
		    "2", "1", "3", "4"]
		  
two_f_c = 0;
two_f_ls = ["1", "5", "3", "6", "4", "2",
            "3", "6", "4", "1", "2", "5",
			"5", "2", "6", "3", "1", "4",
			"6", "4", "1", "2", "5", "3",
			"2", "3", "5", "4", "6", "1",
			"4", "1", "2", "5", "3", "6"]

three_f_c = 0;
three_f_ls = ["4", "3", "1", "2",
              "3", "4", "2", "1",
		      "1", "2", "4", "3",
		      "2", "1", "3", "4"]
			

for i in range(12):
	tree = ET.parse('tasks.xml')
	root = tree.getroot()
	for featureGroup in root:
		if featureGroup.attrib["featureCount"] == "0":
			# Iterate over first and only taskGroup in this featureGroup
			for task in featureGroup[0]:
				task.set('numberOfReps', task.attrib["numberOfReps"])
				task.set('taskId',zero_f_ls[zero_f_c])
				zero_f_c += 1
				if zero_f_c >= len(zero_f_ls):
					zero_f_c = 0
			# Sort tasks inside featureGroup[0] (taskGroup) by taskId
			featureGroup[0][:] = sorted(featureGroup[0], key=lambda child: child.get('taskId'))
		if featureGroup.attrib["featureCount"] == "1":
			for taskGroup in featureGroup:
				taskGroup.set('groupId', one_f_ls[one_f_c])
				one_f_c += 1
				if one_f_c >= len(one_f_ls):
					one_f_c = 0
			# sort taskGroups inside featureGroup
			featureGroup[:] = sorted(featureGroup, key=lambda child: child.get('groupId'))
		if featureGroup.attrib["featureCount"] == "2":
			for taskGroup in featureGroup:
				taskGroup.set('groupId', two_f_ls[two_f_c])
				two_f_c += 1
				if two_f_c >= len(two_f_ls):
					two_f_c = 0
			# sort taskGroups inside featureGroup
			featureGroup[:] = sorted(featureGroup, key=lambda child: child.get('groupId'))
		if featureGroup.attrib["featureCount"] == "3":
			for taskGroup in featureGroup:
				taskGroup.set('groupId', three_f_ls[three_f_c])
				three_f_c += 1
				if three_f_c >= len(three_f_ls):
					three_f_c = 0
			# sort taskGroups inside featureGroup
			featureGroup[:] = sorted(featureGroup, key=lambda child: child.get('groupId'))
			
	# Give every task group its own unique id again
	feature_group_id = 1
	for featureGroup in root.iter('taskGroup'):
		featureGroup.set('groupId', str(feature_group_id))
		feature_group_id += 1
	
	# Give every task its own unique id again
	task_id = 1
	for task in root.iter('task'):
		task.set('taskId', str(task_id))
		task_id += 1
	tree.write('tasks_' + str(i) + '.xml')