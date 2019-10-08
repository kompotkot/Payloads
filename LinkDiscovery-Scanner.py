"""
> python3 LinkDiscovery-Scanner.py https://google.com 1
"""
import requests
import sys
import time


urlBody = str(sys.argv[1])
lstNumber = sys.argv[2]

lstTest = '/root/Documents/Projects/TechGovSg/payloads.txt'
lst1 = '/root/Documents/GitHub/Payloads/folders/folders-payloads-admin.txt'
lst2 = '/root/Documents/GitHub/Payloads/folders/folders-payloads-debug.txt'
lst3 = '/root/Documents/GitHub/Payloads/folders/folders-payloads-other.txt'
lst4 = '/root/Documents/GitHub/Payloads/subdomains/subdomains-payloads-total.txt'

generatedFile = '3-LinkDiscovery-' + lstNumber + '.txt'


def getResponse(someUrl):
	try:
		response = requests.get(someUrl, timeout=5)
		response.raise_for_status()
		return str(response.status_code)
	except requests.exceptions.RequestException as err:
		return str(response.status_code)
		#return err


def urlChanger(someUrl, folderList, toFile=generatedFile):
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


def main():
	startTime = time.time()

	if lstNumber == '1':
		urlChanger(urlBody, lst1)
	elif lstNumber == '2':
		urlChanger(urlBody, lst2)
	elif lstNumber == '3':
		urlChanger(urlBody, lst3)

	print(time.time() - startTime)


if __name__ == '__main__':
	main()