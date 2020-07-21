import asyncio
import aiohttp

import json
import time
import argparse
from collections import ChainMap

defaults = {'list': 'urllist.txt', 'output': 'urlcomments.json'}

parser = argparse.ArgumentParser(description='Comment discovery scanner in code.')
parser.add_argument('-l', '--list', help='Source of urls list file for scan (default: urllist.txt)')
parser.add_argument('-o', '--output', help='The file you want to save found comments (default: urlcomments.json)')

args = parser.parse_args()
new_dict = {key: value for key, value in vars(args).items() if value}
settings = ChainMap(new_dict, defaults)

# Dictionary with urls and comments we will write to file
result_dct = {}


def write_to_file(toFile, data):
    with open(toFile, 'w') as fp:
        json.dump(data, fp)


async def fetch(session, url):
    async with session.get(url) as response:
        print('Url:', url)
        # print('Status:', response.status)
        # print('Content-type:', response.headers['content-type'])
        html = await response.text()
        html_comments = commentFilter(html)  # Add strip() to delete \n
        return html_comments


async def request(url):
    async with aiohttp.ClientSession() as session:
        html_comments = await fetch(session, url)
        result_dct[url] = html_comments
        # return html_comments


def fileWriter(urlList, toFile):
    with open(urlList) as fp:
        loop = asyncio.get_event_loop()
        tasks = [asyncio.ensure_future(request(line.strip())) for line in fp]       # Task - url(line) in file
        loop.run_until_complete(asyncio.gather(*tasks))

    write_to_file(toFile, result_dct)


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
