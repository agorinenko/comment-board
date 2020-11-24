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
