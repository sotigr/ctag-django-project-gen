#!/bin/bash  
echo " ██████╗████████╗ █████╗  ██████╗               ██████╗      ██╗ █████╗ ███╗   ██╗ ██████╗  ██████╗ "
echo "██╔════╝╚══██╔══╝██╔══██╗██╔════╝               ██╔══██╗     ██║██╔══██╗████╗  ██║██╔════╝ ██╔═══██╗"
echo "██║        ██║   ███████║██║  ███╗    █████╗    ██║  ██║     ██║███████║██╔██╗ ██║██║  ███╗██║   ██║"
echo "██║        ██║   ██╔══██║██║   ██║    ╚════╝    ██║  ██║██   ██║██╔══██║██║╚██╗██║██║   ██║██║   ██║"
echo "╚██████╗   ██║   ██║  ██║╚██████╔╝              ██████╔╝╚█████╔╝██║  ██║██║ ╚████║╚██████╔╝╚██████╔╝"
echo " ╚═════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝               ╚═════╝  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝  ╚═════╝ "
echo "                                                                                                    "
echo "██╗    ██╗██╗████████╗██╗  ██╗    ██████╗  █████╗ ██████╗ ███████╗██╗                               "
echo "██║    ██║██║╚══██╔══╝██║  ██║    ██╔══██╗██╔══██╗██╔══██╗██╔════╝██║                               "
echo "██║ █╗ ██║██║   ██║   ███████║    ██████╔╝███████║██████╔╝█████╗  ██║                               "
echo "██║███╗██║██║   ██║   ██╔══██║    ██╔══██╗██╔══██║██╔══██╗██╔══╝  ██║                               "
echo "╚███╔███╔╝██║   ██║   ██║  ██║    ██████╔╝██║  ██║██████╔╝███████╗███████╗                          "
echo " ╚══╝╚══╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝                          "
#http://patorjk.com/software/taag/#p=display&f=ANSI%20Shadow&t=CTAG%20-%20DJANGO%0AWITH%20BABEL

echo ""
echo "+--------------------------------+"
echo "|                                |"
echo "| SUPPORTS:                      |"
echo "|  /ES6 TRANSPILATION WITH BABEL |"
echo "|  /MULTILINGUAL                 |"
echo "|  /PRERENDERING PAGES FOR SEO   |"
echo "|  /VSCODE DEBUGGER INTERGRATION |"
echo "|                                |"
echo "+--------------------------------+"
echo ""

 
read -p "Project name:" project_name

read -p "Enter application name:" app_name
   
echo "Python version:"
python3 -c "import sys; print(sys.version)"

echo "" 

echo "Django version:"
python3 -c "import django; print(django.get_version())"

echo ""  
pip3 install django
django-admin startproject $project_name

cd $project_name

python3 manage.py startapp $app_name

cd ..
 
echo "Modifying and linking the site with the application..."
echo ""

python3 make.py $project_name $app_name

echo "Django project created."
echo ""

echo "Creating python venv and installing dependencies"
echo ""

#Creating venv

cd $project_name
BASEDIR=$(dirname "$0")
echo $BASEDIR
python3 -m venv "$BASEDIR"
source bin/activate 
pip3 install wheel
pip3 install Django==2.0.7
pip3 install django-modeltranslation==0.13b1
pip3 install django-tinymce4-lite
read -p "Run migrations? (y/n)" migrate
if [ $migrate == "y" ]; then
	python3 manage.py makemigrations
	python3 manage.py migrate
	read -p "Create superuser? (y/n)" csu
	if [ $csu == "y" ]; then
		python3 manage.py createsuperuser
	fi
fi
cd ..

#Front end and debugger configuration
python3 make_frontend.py $project_name $app_name

cd $project_name
deactivate
pip3 install --user PyExecJS

npm install babel-core
npm install babel-preset-es2015
npm install babel-preset-stage-2
cd ..

cd $project_name/$app_name/static/scripts/lib
git clone https://github.com/sotigr/CTAG-JS.git

echo "VSCODE debbuger configured."
echo ""

echo ""
echo "Done."