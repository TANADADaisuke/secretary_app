import csv
import time

from datetime import datetime


def print_pause(text):
    print(text)
    time.sleep(0.2)

# greetings
print_pause('How do you do, today?')
print_pause('Think how you perform, not what to do.')
print_pause('Have a nice day!')

current_id = 0
# access csv file with read method
with open('tasks.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
        current_id = row['id']

# register new task
with open('tasks.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'tasks', 'registerd', 'due']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    new_id = current_id + 1
    new_task = '新しいタスクテスト'
    registered_time = datetime.utcnow().isoformat(timespec='milliseconds')
    due_time = '2020-11-10'
    writer.writerow({
        'id': new_id,
        'tasks': new_task,
        'registerd': registered_time,
        'due': due_time
    })

