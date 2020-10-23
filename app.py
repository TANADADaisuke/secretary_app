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
        self.load_data()

    def load_data(self):
        """
        Load csv data.

        Retunrs:
            dict: key -> id, value -> task parameters
        """
        self.data = collections.defaultdict(dict)
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
        with open(self.csvfile, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

            for row_id, task in self.data.items():
                print(type(task))
                task['id'] = int(row_id)
                if int(row_id) == int(task_id):
                    task['status'] = 'done'
                    print(task)
                writer.writerow(task)
        
        # load data after the task status is updated
        self.load_data()
 
    def delete_task(self, task_id):
        """Delete task of given id"""
        with open(self.csvfile, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()

            for row_id, task in self.data.items():
                task['id'] = int(row_id)
                print('deleteing')
                if int(row_id) == int(task_id):
                    continue
                writer.writerow(task)
    
        # load data after the task is deleted
        self.load_data() 
            

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

def main_roop(Task):
    """\
    Define the process of this application. Algorithm is shown below.

    *** Program Algorithm ***
    Show all tasks: TODO paginate it.
     |
    Show the way how to change prompt mode. If the user hit enter without any
    input, prompt mode will be changed.
     |
    1. Prompt for asking new task. If new task is input, go back to the top.
     |
    2. Prompt for asking which task id to update. After status update, 
     | go back to the top.
     |
    3. Prompt for asking which id to delete. After delete, go back to the top.
     |
    4. Prompt for asking process finish.
    *** End of the Algorithm ***

    Detail of the each prompt
    1. Prompt for asking new task
      - If user input a task, ask the due time. Then, ask user whether register it,
        and register that task.
      - ** Task_register function will imediately reload data dictionary.
    2. Prompt for asking which task id to update status
      - If user input a value, check if the value is integer.
      - If the value is integer, pass the id to status_update function.
        Then go back to main roop.
        ** Status_updata function should return status code which represent
           whether the id does exist in csv file and the updata process is 
           indeed succeeded.
      - If the value is not integer, ask again which task id to update.
    3. Prompt for asking which task id to delete
      - If user input a value, check if the value is interger.
      - If the value is integer, pass it to task_delete function.
        Then, go back to main roop.
        ** Task_delete fucntion should return status code which 
           represent whether the id does exist in csv file and the 
           delete process is indeed succeeded.
      - If the value is not integer, ask again which id to delete.
    4. Prompt for asking finish the process
      - If user press 'y', end the process.
      - Otherwise, go back to main roop.
    """
    # Show all tasks
    Task.show_all_tasks()

    # Explain how to change the prompt mode
    print('(Press Enter to change mode)')

    # Prompt for asking new task
    prompt_status = new_task_prompt(Task)
    if prompt_status:
        return main_roop(Task)
    else:
        # status update mode
        # Prompt for asking task id to update status
        prompt_status = status_update_prompt(Task)
        if prompt_status:
            return main_roop(Task)
        else:
            # delete mode
            # Prompt for asking task id to delete
            prompt_status = delete_prompt(Task)
            if prompt_status:
                return main_roop(Task)
            else:
                # process finish mode
                # Prompt for asking whether finish the program or not
                prompt_status = finish_prompt(Task)
                if prompt_status:
                    return None
                else:
                    return main_roop(Task)

def new_task_prompt(Task):
    """
    Prompt for asking new task.
    
    Returns: if the user input a task and register it, return True.
             if the user hit enter without any task input, return False.
    """
    new_task = input('新しいタスク: ')
    if new_task:
        due_time = date_formatted_valid_input()

        # make sure to register that task
        prompt = input(
            '>>> 新しいタスクを登録しますか?\n'
            '{}(期限: {})\n[y/n]: '.format(new_task, due_time)
            )
        if prompt.lower() in ['y', 'ye', 'yes']:
            # Register the task
            Task.create_new_task(new_task, due_time)
            # return True
            return True
        else:
            # ask new task again
            return new_task_prompt(Task)
    else:
        # return False
        return False

def status_update_prompt(Task):
    """
    Prompt for asking task_id to update status
    
    Returns:if the user input task_id, return True.
            If the user hit enter without any input, return False.
    """
    task_id = input('ステータスを更新するidを入力してください: ')
    if task_id:
        # check if the value is integer
        try:
            task_id = int(task_id)
            # update status: green/yellow/red -> done or done -> green
            Task.update_task_status(task_id)
            # return True
            return True
        except ValueError:
            # ask again which task id to update
            return status_update_prompt(Task)
    else:
        # return False
        return False

def delete_prompt(Task):
    """
    Prompt for asking which task id to delete.
    
    Returns: If the user input task_id, return True.
             If the user hit enter without any input, return False.
    """
    task_id = input('削除するタスクのidを入力してください: ')
    if task_id:
        # check if the value is integer
        try:
            task_id = int(task_id)
            # delete the task
            Task.delete_task(task_id)
            # return True
            return True
        except ValueError:
            # ask again which task id to delete
            return delete_prompt(Task)
    else:
        # return False
        return False

def finish_prompt(Task):
    """
    Prompt for asking whether finish the program or not.
    
    Returns: If the user input 'y', return True.
             If the user input other characters, return False.
    """
    prompt = input('プログラムを終了しますか?:[y/n] ')
    if prompt.lower() in ['y', 'ye', 'yes']:
        return True
    else:
        # return False
        return False

def main():
    """Call application."""
    # Say hello to the user
    greetings()
    
    # load tasks from csv datafile
    tasks = Task('tasks.csv')

    # main root
    main_roop(tasks)


if __name__ == '__main__':
    main()
