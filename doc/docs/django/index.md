# Django

```py title="orchestrator.py"
from time import sleep
from os import environ, system, listdir
from os.path import isdir
from sys import argv


environ['DEBUG'] = 'True'
environ['ALLOWED_HOSTS'] = '* 127.0.0.1'
environ['DJANGO_SETTINGS_MODULE'] = '*****.settings.base'

environ['EMAIL_HOST_USER'] = '*****'
environ['EMAIL_HOST_PASSWORD'] = '*****'


system('black -S .')
# system('find -name "*.pyc" -type f -delete')
system('rm -rf `find -type d -name __pycache__`')


def collectstatic():
    system('python3 manage.py collectstatic --noinput')

def makemigrations():
    exclude_list = ['.git', '.github', '.vscode', 'templates', 'static', 'CORE', 'LIPSUM', 'requirements', 'staticfiles', 'env']
    apps = [d for d in listdir('.') if isdir(d) and d not in exclude_list]
    system('python3 manage.py makemigrations ' + ' '.join(apps))

def migrate():
    system('python3 manage.py migrate')    

def test():
    makemigrations()
    migrate()
    environ['DEBUG'] = 'False'
    system('python3 manage.py collectstatic --noinput')

def cleardb():
    system('rm -rf `find -type d -name migrations -not -path "./env/*"`')
    system('find -name "*.sqlite3" -type f -delete')
    exit(0)

def populatedb():
    makemigrations()
    migrate()
    system(...)

def docker():
    system(...)

if argv[1] == 'runserver' and environ.get('DEBUG') == 'False': collectstatic()
elif argv[1] == 'makemigrations': makemigrations(); exit()
elif argv[1] == 'test': test()
elif argv[1] == 'cleardb': cleardb()
elif argv[1] == 'populatedb': populatedb(); exit()
elif argv[1] == 'docker': docker(); system('python3 manage.py ' + ' '.join([i for i in argv[1:]])); exit()


sleep(10)
system('python3 manage.py ' + ' '.join([i for i in argv[1:]]))
```
