'''
resources:
https://www.youtube.com/watch?v=4kD-GRF5VPs

https://stackoverflow.com/questions/14685999/trigger-an-event-when-clipboard-content-changes
'''

import time
import sys
import os

import pyperclip

import CopiedText

text = ""


def main():
    while True:
        check = pyperclip.paste()
        if check != text:
            text = check
            print(text)
        time.sleep(0.1)

if __name__ == "__main__":
    main()