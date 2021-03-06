# ITwarrior

![insert IT Crowd gif here](https://media.giphy.com/media/9PTaAhwri56V2/giphy.gif)

This is a Django frontend for Taskwarrior specifically designed for IT crews.

We developped this as an attempt to enable people to add stuff in our task pipe without having to use a terminal, so they don't have to come and disturb us.

![insert IT Crowd gif here](https://media.giphy.com/media/M8miKCT0qveKY/giphy.gif)

Later we will implement a ticket list view, by-project permissions and highly cool stuff.


## System requirements

With Ubuntu:

```
sudo apt install python3-venv python3-dev libsasl2-dev libldap2-dev libssl-dev
```


## Installation

Clone the repo (duh...) :

```
git clone git@code.probayes.net:it/itwarrior.git
cd itwarrior
```

Create a Python 3 virtual environment :

```
python3 -m venv venv
```

Acticate the virtual environment :

```
. venv/bin/activate
```

Install the dependancies :

```
pip install -r requirements.txt
```

## Development run

To test the application, run (inside the virtual environment) :

```
python3 manage.py runserver
```

## Production run

```
¯\_(ツ)_/¯
```
