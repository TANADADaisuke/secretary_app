import collections
import csv
import time

from datetime import datetime, timedelta

# initial parameters
username = 'Daisuke'


def print_pause(text):
    print(text)
    time.sleep(0.2)

def greetings(username=username):
    """Greeting message."""
    print_pause('Hi, {}! How do you do, today?'.format(username))
    print_pause('Think how you perform, not what to do.')
    print_pause('Have a nice day!')

def format_datetime(date_time):
    """Return str type datetime."""
    return date_time.isoformat(timespec='milliseconds')


class Task(object):
    """tasks"""
    def __init__(self, csvfile):
        self.csvfile = csvfile
        self.fieldnames = ['id', 'tasks', 'registered', 'due', 'status']
        self.data = collections.defaultdict(dict)
        self.load_data()

    def load_data(self):
        """
        Load csv data.

        Retunrs:
            dict: key -> id, value -> task parameters
        """
        with open(self.csvfile, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.sequence_id = 0
            for row in reader:
                self.sequence_id = int(row['id'])
                for column in self.fieldnames[1:]:
                    self.data[self.sequence_id][column] = row[column]
        return self.data

    def create_new_task(self, task, due):
        """Register new task"""
        with open(self.csvfile, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            # parameters
            # new_task = new_task
            # due_time = due_time_valid_input()
            # automatically filled form
            task_id = self.sequence_id + 1
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
            if new_time > datetime.fromisoformat(due):
                status = 'red'

            # write row
            writer.writerow({
                'id': task_id,
                'tasks': task,
                'registered': format_datetime(registered_time),
                'due': due,
                'status': status
            })
        
        # update sequence_id
        self.sequence_id = task_id

        # announce successfully registered
        self.announce_task_registration(task, due)

        # load data after new task is registered
        self.load_data()

    def show_each_task(self, task_id):
        """Show each task according to task id."""
        task_name = self.data[task_id]['tasks']
        task_due = self.data[task_id]['due']
        task_status = self.data[task_id]['status']
        print('{}. <{}> {}(期限: {})'.format(task_id, task_status, task_name, task_due))

    def show_all_tasks(self):
        """\
        Show all tasks registered in csv file.
        """
        for task_id in range(len(self.data)):
            self.show_each_task(task_id + 1)

    def update_task_parameters(self):
        pass

    def update_task_status(self, task_id):
        """Update task status of given id."""
        # TODO: you cannnot use csv as database.
        #       you need to load all data in python local and rewrite csv
        #       to save the change.
        pass

    def deleat_task(self):
        pass

    def announce_task_registration(self, task, due):
        """Announce that the task is successfully registered."""
        print('>>> 新しいタスクが登録されました')
        print('{}(期限: {})\n'.format(task, due))


def date_formatted_valid_input():
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
        return date_formatted_valid_input()

def select_prompt_mode(Task):
    """\
    If the user input new task, return task register function.
    Else(hit the enter without any input), change mode.\
    """
    print('(Press Enter to change mode)')
    new_task = input('新しいタスク: ')
    if new_task:
        due_time = date_formatted_valid_input()
        Task.create_new_task(new_task, due_time)
        Task.show_all_tasks()
        return select_prompt_mode(Task)
    else:
        task_id = input('ステータスを更新するidを入力してください: ')
        if task_id:
            update_task_status(task_id)
            sequence_id = show_all_tasks()
            return select_prompt_mode(sequence_id)
        else:
            prompt = input('プログラムを終了しますか?:[y/n] ')
            if prompt.lower() in ['y', 'ye', 'yes']:
                return None
            return select_prompt_mode(Task)

def main():
    """Main roop for app."""
    # Say hello to the user
    greetings()
    
    # load tasks from csv datafile
    tasks = Task('tasks.csv')

    # Show all tasks
    tasks.show_all_tasks()

    # select prompt mode
    select_prompt_mode(tasks)


if __name__ == '__main__':
    main()
