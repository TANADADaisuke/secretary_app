import csv
import time

from datetime import datetime, timedelta

username = 'Daisuke'

def print_pause(text):
    print(text)
    time.sleep(0.2)

def greetings(username=username):
    """Greeting message."""
    print_pause('Hi, {}! How do you do, today?'.format(username))
    print_pause('Think how you perform, not what to do.')
    print_pause('Have a nice day!')

def announce_task_registration(task, due):
    """Announce that the task is successfully registered."""
    print('>>> 新しいタスクが登録されました')
    print('{}(期限: {})'.format(task, due))

def format_datetime(date_time):
    """Return str type datetime."""
    return date_time.isoformat(timespec='milliseconds')

def due_time_valid_input():
    """\
    Check if the user input is valid compared with datetime class type.
    We expect the following user input.
    2020-01-01\
    """
    due_time = input('期限: ')
    try:
        datetime.fromisoformat(due_time)
        return due_time
    except ValueError:
        print('Invalid date type. We expect the following date type input.'
            '\n>>> 2020-01-01')
        return due_time_valid_input()

def show_each_task(task):
    """Show each task registered in csv file."""
    task_id = task['id']
    task_name = task['tasks']
    task_due = task['due']
    task_status = task['status']
    print('{}. <{}> {}(期限: {})'.format(task_id, task_status, task_name, task_due))

def show_all_tasks():
    """\
    Show all tasks registered in csv file.
    Returns: current_id\
    """
    current_id = 0
    # access csv file with read method
    with open('tasks.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        current_id = 0
        for row in reader:
            # print(row)
            show_each_task(row)
            current_id = int(row['id'])
    return current_id

def register_new_task(current_id):
    """Register new task."""
    with open('tasks.csv', 'a', newline='') as csvfile:
        fieldnames = ['id', 'tasks', 'registerd', 'due', 'status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()

        # task parameters
        # input form
        new_task = input('新しいタスク: ')
        due_time = due_time_valid_input()
        # automatically filled form
        new_id = current_id + 1
        registered_time = datetime.utcnow()
        # set task status
        new_time = datetime.utcnow()
        delta_time = new_time - registered_time
        delta_green = timedelta(days=2)
        delta_yellow = timedelta(days=5)
        if delta_time <= delta_green:
            status = 'green'
        elif delta_time <= delta_yellow:
            status = 'yellow'
        else:
            status = 'red'
        if new_time > datetime.fromisoformat(due_time):
            status = 'red'

        # write row
        writer.writerow({
            'id': new_id,
            'tasks': new_task,
            'registerd': format_datetime(registered_time),
            'due': due_time,
            'status': status
        })

        # announce successfully registerd
        announce_task_registration(new_task, due_time)

def main():
    greetings()
    current_id = show_all_tasks()
    register_new_task(current_id)


if __name__ == '__main__':
    main()
