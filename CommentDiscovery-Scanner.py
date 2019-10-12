"""
> python3 CommentDiscovery-Scanner.py urllist.txt
"""
import requests
import sys
import time


urlList = str(sys.argv[1])
generatedFile = '3-CommentDiscovery.txt'


def getResponse(someUrl):
	try:
		r = requests.get(someUrl, timeout=5)
		r.raise_for_status()
		#return str(r.status_code)
		chars = []
		for i in r.text:
			chars.append(i)		# Get all body as list of chars
		return chars
	except requests.exceptions.RequestException as err:
		return str(r.status_code)
		#return err


def fileWriter(urlList, toFile=generatedFile):
	tof = open(toFile, 'w')

	with open(urlList) as fp:
		for line in fp:
			someComments = commentFilter(getResponse(line.strip()))		# strip() to delete \n
			tof.write(line + '\n' + someComments + '\n')

	tof.close()


def commentFilter(someLst):
	comment = ''

	for i in range(len(someLst)):
		cnt = 0
		if someLst[i] == '<' and someLst[i+1] == '!' and someLst[i+2] == '-' and someLst[i+3] == '-':	# Check when comment starts with <!--
			cnt = i + 3		# Change to 4 if you don't want to see '-' before each comment

			while someLst[cnt] != '-' or someLst[cnt+1] != '>':	# Check if comment end with -->
				comment += someLst[cnt]
				cnt += 1
			
			comment += '\n\n'

	return comment


def main():
	startTime = time.time()

	fileWriter(urlList)

	print(time.time() - startTime)		# Screen-speed timer


if __name__ == '__main__':
	main()
