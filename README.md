# Radiation Therapy Application

Source code for the creation of the Radiation Therapy (RT) website, which is the user interface
to the RT dose, CT image and RT Decision support functionality.

### Developed Functionality
* Display a home page with proper CSS formatting
* Create new users with a username and password
* Log in and log out existing users
* Filler content for an "About" Page and an "FAQ" page

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

#### How to develop

Instructions are currently written only for an ubuntu setup

0) in the terminal, install django and celery:
```
$ pip3 install django==1.11.6
$ pip3 install celery==4.1.0
```
1) Create a file `ip.txt` with 1 line, containing your ip address of the computer
you wish to test on. 
2) Set up mysql, with a root account with a password, default port. Set up `/etc/mysql/my.cnf/` with
```
[client]
user=root
password={PASSWORD}
``` 
3) Create the database in the terminal
```
$ mysql
$ create database dsrt;
```
4) Create tables in the database using django
```
$ python3 manage.py migrate
```
5) Run
```
$ python3 manage.py runserver 0.0.0.0:8000
```
Then connect to the webpage using whichever ip your computer is linked against.

at the end of the file

### Sample Log In for Reference (Deployed) instance

If you would like to log in, the sample user's info is as follows:
Username: user
Password: ipilabusc
