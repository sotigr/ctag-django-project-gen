import sys 
import os
import shutil

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


#####################################
# Creating default app configuration
#####################################

#Add config to site settings
print("Adding config to site settings")
settings_file_path = sys.argv[1]+ "/" + sys.argv[1] + "/settings.py"
add_line(settings_file_path, "    'django.contrib.staticfiles',", "    '"+sys.argv[2]+".apps." + sys.argv[2].capitalize() + "Config',")

#Create application inner router
print("Creating application inner router")
urls_file_path = sys.argv[1]+ "/" + sys.argv[2] + "/urls.py" 
out_text = """
from django.urls import path

from .controllers import home

urlpatterns = [
	path('', home.index, name='index'),
]
"""
create_file(urls_file_path, out_text)

#Add application route configuration in general site route configuration
print("Adding application route configuration in general site route configuration")
urls_file_app_path = sys.argv[1]+ "/" + sys.argv[1] + "/urls.py"
add(urls_file_app_path, "from django.urls import path",  ", include")
add_line(urls_file_app_path, "urlpatterns = [",  "    path('', include('"+sys.argv[2]+".urls')),")


#####################################
# Changing the default project layout
#####################################
#Delete views.py
print("Deleting views.py")
old_views_file_path = sys.argv[1]+ "/" + sys.argv[2] + "/views.py" 
os.remove(old_views_file_path)

#Creating the controllers folder
print("Creating the controllers folder")
contoller_directory = sys.argv[1]+ "/" + sys.argv[2] + "/controllers"
os.makedirs(contoller_directory)

#Adding the home controller
print("Adding the home controller")
out_text = """
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
	return render(request, 'partial/home/index.html')
"""
create_file(contoller_directory + "/home.py", out_text)

#Creating the views
print("Creating the views")
templates_directory = sys.argv[1]+ "/" + sys.argv[2] + "/templates/"
os.makedirs(templates_directory)

templates_directory = sys.argv[1]+ "/" + sys.argv[2] + "/templates/shared"
os.makedirs(templates_directory)

templates_directory = sys.argv[1]+ "/" + sys.argv[2] + "/templates/partial"
os.makedirs(templates_directory)


layout_text = """
<html>
<head>
    <title></title>
</head>
<body>
{% block content %}
{% endblock %}
</body>
</html>
"""
layout_file = sys.argv[1]+ "/" + sys.argv[2] + "/templates/shared/layout.html"
create_file(layout_file, layout_text)

index_text = """
{% extends 'shared/layout.html' %}

{% block content %}

<p>Hello world!</p>

{% endblock %}
"""
os.makedirs(sys.argv[1]+ "/" + sys.argv[2] + "/templates/partial/home")
index_file = sys.argv[1]+ "/" + sys.argv[2] + "/templates/partial/home/index.html"
create_file(index_file, index_text)

print("Creating project management scripts")

view_creation_script_path = sys.argv[1] + "/" + "view.py"
shutil.copyfile('view.py', view_creation_script_path)
preppend_file(view_creation_script_path, "app_name = '"+ sys.argv[2] +"'")
