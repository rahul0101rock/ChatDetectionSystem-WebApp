# ChatDetectionSystem WebApp 
### A Web App for [Active Chat Monitoring and Suspicious Chat Detection System Project](https://github.com/rahul0101rock/Active-Chat-Monitoring-and-Suspicious-Chat-Detection-System)
### https://22cse12.pythonanywhere.com/
## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/rahul0101rock/ChatDetectionSystem-WebApp.git
$ cd ChatDetectionSystem-WebApp
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ mkvirtualenv myenv
$ pip install django
$ workon myenv
```

Then install the dependencies:

```sh
(myenv)$ cd ChatDetectionSystem-WebApp
(myenv)$ pip install -r requirements.txt
```

Once `pip` has finished installing the dependencies:
```sh
(myenv)$ python manage.py migrate
(myenv)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/` or `http://localhost:8000/`.
