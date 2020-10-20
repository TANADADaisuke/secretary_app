import csv
import time

from datetime import datetime


def print_pause(text):
    print(text)
    time.sleep(0.2)

def announce_task_registration(task, due):
    print('>>> 新しいタスクが登録されました')
    print('{}(期日: {})'.format(task, due))


# greetings
print_pause('How do you do, today?')
print_pause('Think how you perform, not what to do.')
print_pause('Have a nice day!')

current_id = 0
# access csv file with read method
with open('tasks.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    current_id = 0
    for row in reader:
        print(row)
        current_id = int(row['id'])

# register new task
with open('tasks.csv', 'a', newline='') as csvfile:
    fieldnames = ['id', 'tasks', 'registerd', 'due']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    # writer.writeheader()

    # task parameters
    # input form
    new_task = input('新しいタスク: ')
    due_time = input('期限: ')
    # automatically filled form
    new_id = current_id + 1
    registered_time = datetime.utcnow().isoformat(timespec='milliseconds')
    writer.writerow({
        'id': new_id,
        'tasks': new_task,
        'registerd': registered_time,
        'due': due_time
    })

    # announce successfully registerd
    announce_task_registration(new_task, due_time)
