import asyncio
import aiohttp

import time
import argparse
from collections import ChainMap

defaults = {'list': 'urllist.txt', 'output': 'urlcomments.txt'}

parser = argparse.ArgumentParser(description='Comment discovery scanner in code.')
parser.add_argument('-l', '--list', help='Source of urls list file for scan (default: urllist.txt)')
parser.add_argument('-o', '--output', help='The file you want to save found comments (default: urlcomments.txt)')

args = parser.parse_args()
new_dict = {key: value for key, value in vars(args).items() if value}
settings = ChainMap(new_dict, defaults)


async def fetch(session, url):
    async with session.get(url) as response:
        # print('Status:', response.status)
        # print('Content-type:', response.headers['content-type'])
        html = await response.text()
        someComments = commentFilter(html.strip())  # strip() to delete \n
        return someComments


async def request(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        return html


def fileWriter(urlList, toFile):
    tof = open(toFile, 'w')

    with open(urlList) as fp:
        for line in fp:
            print('Url:', line.strip())

            loop = asyncio.get_event_loop()
            html = loop.run_until_complete(request(line.strip()))

            tof.write(line + '\n' + html + '\n')

    tof.close()


def commentFilter(someLst):
    comment = ''

    for i in range(len(someLst)):
        cnt = 0
        if someLst[i] == '<' and someLst[i + 1] == '!' and someLst[i + 2] == '-' and someLst[
            i + 3] == '-':  # Check when comment starts with <!--
            cnt = i + 3
            while someLst[cnt] != '-' or someLst[cnt + 1] != '>':
                comment += someLst[cnt]
                cnt += 1
            comment += '\n\n'
    return comment


def main():
    startTime = time.time()

    fileWriter(settings['list'], settings['output'])

    print(f'Required time: {time.time() - startTime}')


if __name__ == '__main__':
    main()
