# comment-board
## Install dev requirements
```shell script
pip install -r requirements.dev.txt
```
## Start dev server
```shell script
adev runserver
```
## Create migrations
```shell script
python -m db revision --message="Init" --autogenerate
```
```shell script
python -m db upgrade head
```
