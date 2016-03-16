import todoist #The official todoist-python API. Get it with 'pip install todoist-python'
import getpass
import os
import ConfigParser
import argparse

# Default file path for configuration file
configfile = os.path.expanduser('~/.todoist-cli')

default_project = 'Inbox'

def print_tasks(tasklist, header=True, sort=True):
    '''
        Given a list of existing tasks (in the format returned from the API) print them out.
    '''

    if len(tasklist) == 0:
        print "No tasks in list"
        return None

    # Sort according to priority
    if sort:
        tasklist.sort(key=(lambda x: x['priority']), reverse=True)

    if header:
        print "Priority\tTitle"
        print "---------------------"
    for task in tasklist:
        pri = task['priority']
        # Switch statement to find priority string
        if 1 == pri:
            pri_string = "Low\t"
        elif 2 == pri:
            pri_string = "Medium\t"
        elif 3 == pri:
            pri_string = "High\t"
        elif 4 == pri:
            pri_string = "Very High"

        due = task['due_date']
        
        print pri_string, '\t', task['content']

def get_project(api, title=None):
    '''
        Returns the project object given a title
    '''
    api.projects.sync()
    if not title:
        # With no input, return default project
        title = default_project

    # Be aware of projects that don't exist and return None
    projects = [i for i in api.state['Projects'] if i['name'] == title]
    if len(projects) > 0:
        return projects[0]
    return None

def add_task(api, title, project=default_project, priority=1, due_date=None):
    '''
        Adds a task with the given attributes to Todoist
    '''
    # Reset inputs to default if we have Null args
    if not project:
        project = default_project
    if not priority:
        priority = 1

    # Get appropriate project object
    p = get_project(api, project)
    if not p:
        # Set to default project if we have an error
        p = get_project(api)
        print "Project {} doesn't exist.".format(project)
        print "Adding task to project {}.".format(p['name'])

    task = api.items.add(title, p['id'], priority=priority, date_string=due_date)
    api.commit()

def login():
    '''
        Gets username and password from the user, logs in, and saves the API Token
            into a configuration file.
    '''

    # Get login info from user and verify correctness
    while True:
        username = raw_input("Username: ")
        pw = getpass.getpass()
        api = todoist.api.TodoistAPI()
        user = api.login(username, pw)
        
        # Check for success
        if 'error' in user:
            print "Incorrect login. Please try again."
            print ""
        else:
            break

    # Ask whether to save settings or not
    while True:
        response = raw_input("Save login (Y/N)?")
        response = response.lower()
        if response == 'y' or response == 'yes':
            save = True
            break
        elif response == 'n' or response == 'no':
            save = False
            break

    if save:
        # Save API Token to the settings file
        config = ConfigParser.ConfigParser()

        config.add_section('Settings')
        config.set('Settings', 'api_token', user['token'])

        with open(configfile, 'wb') as cfgfile:
            config.write(cfgfile)

    api.sync()
    return api

def main():

    # Set arguments list
    parser = argparse.ArgumentParser(description="Command line interface to Todoist.")

    parser.add_argument('action', choices=['add', 'list', 'query', 'next'],
            help="Specify action to take.")
    parser.add_argument('-p', '--project', help="Specify project.")
    parser.add_argument('-pri', '--priority', type=int, choices=range(1,5),
            help="Specify priority, 1-4.")
    parser.add_argument('-d', '--due', help="Due date.")

    args, extras = parser.parse_known_args()

    # Check to see if login is already saved
    config = ConfigParser.ConfigParser()
    config.read(configfile)
    try:
        token = config.get('Settings', 'api_token')
        api = todoist.api.TodoistAPI(token)
        api.sync()
    except:
        print "Your saved API token is expired. Please reenter your login."
        print ''
        api = login()

    response = api.user.sync()

    # Parse arguments and act

    # Switch on the action argument
    if args.action.lower() == 'add':
        # Add new task
        # extras contains the title of the task, so combine into one name
        add_task(api, ' '.join(extras), project=args.project,
                priority=args.priority, due_date=args.due)

    if args.action.lower() == 'list':
        # Prints a list of tasks that match all the inputs
        # Just add everything onto 'extras', query, and print everything in all lists

        #if args.project:
            # I'm not sure how to limit the query to a project...
        if args.priority:
            extras.append(str(args.priority))
        if args.due:
            extras.append(args.due)
        if len(extras) == 0:
            # If no inputs, by default print todays tasks
            extras = ['today']

        response = api.query(extras)
        tasks = []
        for x in response:
            tasks.append(x['data'])

        # Find common tasks
        common_tasks = []
        for x in tasks[0]:
            common = True
            for y in tasks:
                g = [k['id'] for k in y]
                if x['id'] not in g:
                    common = False
                    break

            if common:
                common_tasks.append(x)

        print_tasks(common_tasks)

    if args.action.lower() == 'query':
        # Raw query on each of the remaining args and print
        # Intended for testing or power users
        response = api.query(extras)
        print "Queries: ", ' '.join(extras)
        for x in response:
            print ''
            print "Query: ", x['query']
            print_tasks(x['data'])

    if args.action.lower() == 'next':
        # Print all tasks due today
        print "Tasks Due Today"
        print ''
        print_tasks(api.query('today')[0]['data'])

if __name__ == "__main__":
        main()

