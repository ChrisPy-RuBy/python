import pyperclip
import sys

labbook_address = 'http://127.0.0.1:8000/{}'
for line in sys.stdin:
    splitline = line.split('.md')
    full_address = labbook_address.format(splitline[0])
    print(full_address)
    pyperclip.copy(full_address)


