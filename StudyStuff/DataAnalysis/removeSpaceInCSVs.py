# Only needed for pilot study csvs 

import fnmatch
import os

matches = []
for root, dirnames, filenames in os.walk('KeyStrokeLog'):
    for filename in fnmatch.filter(filenames, '*.csv'):
        matches.append(os.path.join(root, filename))
		
for match in matches:
	tempLines = []
	with open(match, "r") as fin:
		for line in fin:
			tempLines.append(line.replace('; ', ';'))
		fin.close()
	with open(match, "w") as fout:
		fout.writelines(tempLines)
		fout.close()