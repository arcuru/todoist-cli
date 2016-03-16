# todoist-cli
Command line interface for the Todoist task manager.

## Configuration
This uses the Official Python API from Todoist. You can install with:

```
pip install todoist-python
```

It will ask for your Username/Password on first run and save your API Authentication token (not your password) into a config file. The config file location can be changed manually in todoist-cli.py.


## Usage

```
python2 todoist-cli.py -h
usage: todoist-cli.py [-h] [-p PROJECT] [-pri {1,2,3,4}] [-d DUE]
                      {add,list,query,next}

Command line interface to Todoist.

positional arguments:
  {add,list,query,next}
                        Specify action to take.

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECT, --project PROJECT
                        Specify project.
  -pri {1,2,3,4}, --priority {1,2,3,4}
                        Specify priority, 1-4.
  -d DUE, --due DUE     Due date.
```

Most inputs are just as flexible as Todoist allows, since the processing is handed off to the server. 

### Add
Adds a task to your Todoist.

#### Example 1
Add a task to your default project with no due date. Each of the below are equivalent.
```
python2 todoist-cli.py add Pay Bills
python2 todoist-cli.py add 'Pay Bills'
```

#### Example 2
Add the task 'Generate pull request' to project 'Coding', priority 4 (Very High), and due tomorrow.
```
python2 todoist-cli.py add Generate pull request -p Coding -pri 4 -d tomorrow
```

### List
Lists all the tasks that match **all** the criteria you provide.

#### Example 1
This would list all of the high priority tasks due tomorrow.
```
python2 todoist-cli.py list -pri 4 -d tom
```

### Next
Lists all of your tasks due today. Ignores all other arguments.