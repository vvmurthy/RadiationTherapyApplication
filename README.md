# Radiation Therapy Application

Source code for the creation of the Radiation Therapy (RT) website, which is the user interface
to the RT dose, CT image and RT Decision support functionality.

*NOTE:* This README overrides the directions in the dropbox folder regarding setup- it is most
up-to-date regarding setup of the website.

### Developed Functionality
* Display a home page with proper CSS formatting
* Create new users with a username and password
* Log in and log out existing users
* Filler content for an "About" Page and an "FAQ" page

#### How to Develop and Run on Your Local Computer

Typically, for developing website functionality, you will be writing and deploying the website on
your local machine to see changes. 

Instructions are currently written only for an ubuntu setup. However, they should work on the 
VM in the `RadiationTherapyDecisionSupport` repo. 

0) in the terminal, install Python packages Django, Celery and database system MySQL:
```
$ sudo apt-get install mysql-server
$ sudo apt-get install redis-server
sudo apt-get install libgtk-3-dev
sudo apt-get install libssl-dev
$ sudo apt-get install libmysqlclient-dev
$ sudo pip3 install -r requirements.txt

```
1) Create a file `ip.txt` with 1 line, containing your ip address of the computer
you wish to test on. This should usually be `localhost` unless you are using a remote server. So the contents
of the file would look like:
```
localhost
```
usually

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

3.5)
type `$ sudo nano /etc/mysql/my.cnf/` in the terminal, and edit the `my.cnf` file to say

```
[client]
user=root
password={PASSWORD}
database=dsrt
```

at the end of the file. Note everything but the last line you should have added already to the file.

4) Create tables in the database using django
```
$ python3 manage.py makemigrations upload
$ python3 manage.py makemigrations UserProfile
$ python3 manage.py migrate
```
If you are prompted for `[y/N]` for renaming different tables (e.g. `did you rename RtIsDose to RTIsodose`?) press enter. If you are prompted by `you are trying to add a non-nullable field` enter `1`, and then `1` at the prompt.  

4.5) Download the RadiationTherapyDecisionSupport repo, and symbolically link the folder to the correct location in RadiationTherapyApplication, under `RadiationTherapyApplication/AlgoEngine/app/AlgoEngine`

In ubuntu, this can be done using 
```
$ ln -s /path/to/RadiationTherapyDecisionSupport/ /path/to/RadiationTherapyApplication/AlgoEngine/app/AlgoEngine/
```

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
