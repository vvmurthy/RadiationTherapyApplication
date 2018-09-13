# Radiation Therapy Application

Source code for the creation of the Radiation Therapy (RT) website, which is the user interface
to the RT dose, CT image and RT Decision support functionality.

### Developed Functionality
* Display a home page with proper CSS formatting
* Create new users with a username and password
* Log in and log out existing users
* Filler content for an "About" Page and an "FAQ" page

#### How to develop

Instructions are currently written only for an ubuntu setup

0) in the terminal, install Python packages Django, Celery and database system MySQL:
```
$ sudo pip3 install django==1.11.6
$ sudo pip3 install celery==4.1.0
$ sudo pip3 install redis
$ sudo apt-get install redis-server
$ sudo apt-get install mysql-server
```
1) Create a file `ip.txt` with 1 line, containing your ip address of the computer
you wish to test on. 
2) Set up mysql, with a root account with a password. **Do not use a default / blank password**. Also set MySQL to use the default port. type `$ sudo nano /etc/mysql/my.cnf` on the command line and set up `/etc/mysql/my.cnf/` with
```
[client]
user=root
password={PASSWORD}
``` 
at the end of the file

3) Create the database in the terminal
```
$ mysql
$ create database dsrt;
```
4) Create tables in the database using django
```
$ python3 manage.py makemigrations upload
$ python3 manage.py makemigrations UserProfile
$ python3 manage.py migrate

5) Create the admin (first account). Typically this will be with username `admin` and password `radiation`. 
Use `example@example.com` if prompted for an email.
```
$ python3 manage.py createsuperuser
```

5) Run
```
$ sudo service redis-server start 
$ python3 manage.py runserver 0.0.0.0:8000
```
or just run `sh run.sh`
Then connect to the webpage using whichever ip your computer is linked against.

at the end of the file

#### Changing Frontend (CSS / HTML / JS)
To see changes to css / js reload webpage with `CTRL + F5` (Chrome)
CSS is from the `stylesheet` declared at the top of the html file

### Accessing admin page
Go to the following page
```
[ip]:8000/admin/
```

and log in with `admin`, `radiation` as above. This can be used to:
* Add or change user information
* Add or change hospital information

### How to Run

1) Get into the RT server 68.181.174.158. Ask someone for the username and password.
2) From the command line on the RT server:
```
$ cd RadiationTherapyApplication
$ python manage.py runserver 0.0.0.0:8000
```
This starts the [Django](https://www.djangoproject.com/) Application to run the RT website. 

You can then connect at your client-side browser by typing at the URL:
```
68.181.174.158:8000
```
which should redirect you to the home page of the website. 