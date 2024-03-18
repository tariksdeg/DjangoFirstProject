Windows
2 python -m venv myenv
3 .\myenv\Scripts\Activate
4 .\myenv\Scripts\activate
5 Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
6 .\myenv\Scripts\activate
7 python manage.py runserver
8 pip install django
9 pip install Django
10 pip install djangorestframework
11 python manage.py runserver
12 pip install rest_framework_simplejwt
13 python manage.py runserver
14 pip install djangorestframework_simplejwt
15 python manage.py runserver
16 pip freeze > requirements.txt
17 pip install -r requirements.txt
18 pip freeze
19 python manage.py runserver
20 python manage.py makemigrations
21 python manage.py migrate

Linux

sudo apt update
    2  sudo apt install python3 python3-pip
    3  ls -la
    4  git pull
    5  pyhton3 -m venv myenv
    6* 
    7  sudo apt install python3.10-venv
    8  pyhton3 -m venv myenv
    9  python3 -m venv myenv
   10  source myenv/bin/activate
   11  pip3 install -r requirements.txt 
   12  python3 manage.py makemigrations
   13  python3 manage.py migrate
   14  python3 manage.py runserver