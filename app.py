import csv
import time

def print_pause(text):
    print(text)
    time.sleep(2)

print_pause('How do you do, today?')
print_pause('Think how you perform, not what to do.')
print_pause('Have a nice day!')

with open('tasks.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
