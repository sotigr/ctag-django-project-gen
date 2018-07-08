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
add_line(settings_file_path, "                'django.contrib.messages.context_processors.messages',", "                'main.context_processors.scripts_styles.scripts_styles',")
add_line(settings_file_path, "STATIC_URL = '/static/'", """STATIC_PATH = ''

MEDIA_URL = '/media/'
STATIC_PATH = ''
""")
add_line(settings_file_path, "USE_TZ = True", """
#Model translation setup
USE_I18N = True #Keep this on

gettext = lambda s: s
LANGUAGES = (
    ('el', gettext('Greek')),
    ('en', gettext('English')),
)
MODELTRANSLATION_LANGUAGES = ('el', 'en')
MODELTRANSLATION_FALLBACK_LANGUAGES = ('el', 'en')
MODELTRANSLATION_PREPOPULATE_LANGUAGE = 'el'
""")
add_line(settings_file_path, "INSTALLED_APPS = [", "    'modeltranslation', #install pip django-modeltranslation==0.13b1")
os.remove(sys.argv[1]+ "/" + sys.argv[2] + "/models.py")
os.remove(sys.argv[1]+ "/" + sys.argv[2] + "/admin.py")

create_file(sys.argv[1]+ "/" + sys.argv[2] + "/admin.py" , """
from django.contrib import admin
from main.models import News
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin

class NewsAdmin(TabbedTranslationAdmin):
    group_fieldsets = True 
    #both_empty_values_fields = ('title', 'text')


admin.site.register(News, NewsAdmin)
""")

create_file(sys.argv[1]+ "/" + sys.argv[2] + "/models.py" , """
from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "News"
""")


create_file(sys.argv[1]+ "/" + sys.argv[2] + "/translation.py" , """
from modeltranslation.translator import register, TranslationOptions
from main.models import News

@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)
    required_languages = ('en', 'el')
""")

#Creating js libs
os.makedirs(sys.argv[1]+ "/" + sys.argv[2] + "/static/scripts/lib" )  
  
#Creating js libs
os.makedirs(sys.argv[1]+ "/" + sys.argv[2] + "/context_processors" )  
processor = """
import os
from django.core.cache import cache

def get_file_content(files):
    contents = []
    for name in files:
        try:
            cache_key_name = "app_cache_file_" + name
            if cache.get(cache_key_name) == None:
                with open( os.getcwd() + "/main" + name, 'r') as f:
                    f_cont = f.read()
                    cache.set(cache_key_name, f_cont, 300)
                    contents.append({'name':name, 'value': f_cont})
            else:
                contents.append({'name':name, 'value': cache.get(cache_key_name)})
        except IOError as exc:
            pass
    return contents

def scripts_styles(request):
    
    svg_files = [ 

    ]
    javascript_files = [
        "/static/scripts/lib/CTAG-JS/ctag.dist.min.js",
        "/static/scripts/dist.js",
    ]
    css_files = [

    ]
    context = {
        "svg" : get_file_content(svg_files),
        "javascript" : get_file_content(javascript_files),
        "css" : get_file_content(css_files),
    }

    return context
"""
create_file(sys.argv[1]+ "/" + sys.argv[2] + "/context_processors/scripts_styles.py" , processor)

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
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <title></title> 

        {% for svg_item in svg %}
        <template style="display:none;" id="{{svg.name}}">{{svg_item.value|safe}}</template>
        {% endfor %}
        
        {% for js_item in javascript %}
        <script type="text/javascript">{{js_item.value|safe}}</script>
        {% endfor %} 

        {% for css_item in css %}
        <style>{{css_item.value|safe}}</style>
        {% endfor %} 
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
