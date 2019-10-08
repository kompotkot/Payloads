import requests, sys


urlBody = str(sys.argv[1])
folders = 'test.txt'


def getResponse(someUrl):
	try:
		response = requests.get(someUrl, timeout=10)
		response.raise_for_status()
		stat = str(response.status_code)
		return stat
	except requests.exceptions.RequestException as err:
		return err
		#pass


def urlChanger(someUrl, folderList):
	totalLines = len(open(folderList).readlines())	#Enumerate lines for our counter
	cnt = 1
	with open(folderList) as fp:
		for line in fp:
			a = str(line.strip())

			#Flushing counter
			sys.stdout.write("\r" + str(cnt) + ' of ' + str(totalLines))
			sys.stdout.flush()
			
			if getResponse(someUrl + '/' + a) == '200':
				print("\n" + getResponse(someUrl + '/' + a), someUrl + '/' + a)

			cnt += 1



urlChanger(urlBody, folders)
#print(getResponse(urlBody))


