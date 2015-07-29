#!/usr/bin/python

# getIdfSeries.py

import os
import csv

def toStr(num):
	if(num >= 10):
		return str(num)
	else:
		return '0'+str(num)

def main():
	# ----- these need to be set to target the correct day
	fileYear = 2014
	fileMonth = 12
	fileDay = 4

	MIN_HOURS = 0
	MAX_HOURS = 23
	# ----- 

	dayStr_FileStem = toStr(fileYear)+'_'+toStr(fileMonth)+'_'+toStr(fileDay)
	dayStr_DateStem = toStr(fileYear)+'-'+toStr(fileMonth)+'-'+toStr(fileDay)

	startHour = MIN_HOURS
	endHour = startHour+2

	neededHours = [1,2,3,5,6,7]

	while endHour <= MAX_HOURS:
		idfOutFileName = dayStr_FileStem+'_'+toStr(startHour+1)+toStr(endHour)
		startTime = dayStr_DateStem+' '+toStr(startHour)+':00'
		endTime = dayStr_DateStem+' '+toStr(endHour)+':00'


		outFileWriter = open('input20141204','w')
		outFileWriter.write(idfOutFileName)
		outFileWriter.write('\n')		
		outFileWriter.write(startTime)
		outFileWriter.write('\n')
		outFileWriter.write(endTime)
		outFileWriter.write('\n')

		outFileWriter.close()

		print(idfOutFileName)
		print(startTime)
		print(endTime)
		print('\n')

		os.system("time ./main.py < input20141204")

		startHour += 1
		endHour += 1


if __name__ == '__main__':
	main()

