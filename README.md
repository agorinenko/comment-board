# comment-board
## Install dev requirements
```shell script
pip install -r requirements.dev.txt
```
## Start dev server
```shell script
python -m api
```
## Create migrations
```shell script
python -m db revision --autogenerate
```
## Deploy migrations
```shell script
python -m db upgrade head
```
## Start dev server
```shell script
python -m api runserver api --root api --verbose
```
## Run tests from console
```shell script
pytest -ra
```
## PyCharm :: Run/Debug configuration
1. Add python configuration
1. Module name: api
1. Parameters: runserver api --root api --verbose
