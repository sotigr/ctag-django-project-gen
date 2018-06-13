import sys 
import os
import shutil
from shutil import copyfile

def add_line(file, search, newline):
	with open(file, "r") as in_file:
		buf = in_file.readlines()

	with open(file, "w") as out_file:
		for line in buf:
			if line == search+"\n":
				line = line + newline +	"\n"
			out_file.write(line)	

def add(file, search, newline):
	with open(file, "r") as in_file:
		buf = in_file.readlines()

	with open(file, "w") as out_file:
		for line in buf: 
			if line == search + "\n":
				line = line[:-1] + newline + "\n"
			out_file.write(line)	
			
def create_file(file, text):
		with open(file, "w") as out_file:
			out_file.write(text)
			
def preppend_file(file, text):
	with open(file, 'r') as original: data = original.read()
	with open(file, "w") as out_file:
   		out_file.write(text + "\n" + data)

root_path = sys.argv[1] + "/"
app_path = sys.argv[1] + "/" + sys.argv[2] + "/"
static_path = app_path + "static/"

print("Copying scripts")

#Copying combine.py
copyfile("combine.py", root_path + "combine.py") 


print("Creating static directory")
#Making static
os.makedirs(static_path)
os.makedirs(static_path + "scripts/project/")

create_file(static_path + "scripts/project/main.js", '''
const getMessage = () => "Hello World Babel js";
document.write(getMessage());
''')

#Configuring debuger
vscode_path = root_path + ".vscode/"
os.makedirs(vscode_path)

python_venv = os.path.dirname(os.path.realpath(__file__)) + "/" + root_path + "bin/python3"

launch_json = '''
 {
     "version": "0.2.0",
     "configurations": [{
         "name": "Django",
         "type": "python",
         "request": "launch",
         "preLaunchTask": "babel_render",
         "program": "${workspaceFolder}/manage.py",

         "pythonPath": "'''+python_venv+'''",

         "args": [
             "runserver",
             "--noreload",
             "--nothreading"
         ],

         "debugOptions": [
             "RedirectOutput",
             "Django"
         ]
     }],
     "compounds": [],
 }
'''

task_json = ''' 
{ 
    "version": "0.1.0",
    "command": "python",  
    "args": ["combine.py", "'''+sys.argv[2]+'''/static/scripts/project", "'''+sys.argv[2]+'''/static/scripts/dist.js"],
    "problemMatcher": {
        "fileLocation": ["relative", "${workspaceRoot}"],
        "pattern": {
            "regexp": "^(.*)+s$",
            "message": 1
        },
    },
    "tasks": [ 
        {
            "taskName": "babel_render",
            "isShellCommand": true
        }
    ]
}
'''

settings_json = '''
{
    "python.pythonPath": "/usr/bin/python3.6",
}
'''

create_file(vscode_path + "launch.json", launch_json)
create_file(vscode_path + "tasks.json", task_json)
create_file(vscode_path + "settings.json", settings_json)


#Linking script to layout head
add_line(app_path + "templates/shared/layout.html", "    <title></title>", '    <script type="text/javascript" src="/static/scripts/dist.js"></script>')