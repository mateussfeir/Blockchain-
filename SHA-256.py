import hashlib
import json
from time import sleep

waiting = True
while waiting:
    sleep(0.05)
    user_input = input('User input: ')
    if user_input == 'quit' or user_input == 'q':
        print('User left.')
        break
    else:
        sleep(0.05)
        sha_256 = hashlib.sha256(json.dumps(user_input).encode()).hexdigest()
        print('Outputting sha_256: {}'.format(sha_256))
