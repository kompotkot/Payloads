"""
> python3 LinkDiscovery-Scanner.py https://google.com
Внедрить многопоточность
"""


import requests, sys


urlBody = str(sys.argv[1])

lst1 = '/root/Documents/GitHub/Payloads/folders/folders-payloads-admin.txt'
lst2 = '/root/Documents/GitHub/Payloads/folders/folders-payloads-debug.txt'
lst3 = '/root/Documents/GitHub/Payloads/folders/folders-payloads-other.txt'
lst4 = '/root/Documents/GitHub/Payloads/subdomains/subdomains-payloads-total.txt'


def getResponse(someUrl):
	try:
		response = requests.get(someUrl, timeout=10)
		response.raise_for_status()
		stat = str(response.status_code)
		return stat
	except requests.exceptions.RequestException as err:
		stat = str(response.status_code)
		return stat
		#return err


def urlChanger(someUrl, folderList, toFile='3-LinkDiscovery.txt'):
	totalLines = len(open(folderList).readlines())	#Get total number of lines for our counter
	cnt = 1

	tof = open(toFile, 'w')

	with open(folderList) as fp:
		for line in fp:
			a = str(line.strip())

			sys.stdout.write("\r" + str(cnt) + ' of ' + str(totalLines))	#Flushing counter
			sys.stdout.flush()

			if cnt == 1:	#Example to check request misstakes
				print("\n" + str(getResponse(someUrl + '/' + a)), someUrl + '/' + a)
			else:
				if getResponse(someUrl + '/' + a) != '404':
					req = str(getResponse(someUrl + '/' + a))
					print("\n" + req, someUrl + '/' + a)
					tof.write(req + ' ' + someUrl + '/' + a + '\n')		#Write success url to file

			cnt += 1

	tof.close()
	print('End of scan')


urlChanger(urlBody, lst1)
