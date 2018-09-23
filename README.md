# kumquat
  A personal twitter client.

## Code layout

	ui - frontend code
	static - (generated)
	app.py - the whole app

## Setup
### configure with your credentials

	1. mv config.py.sample config.py
	2. get credentials
	   https://developer.twitter.com/en/apps
	   details -> keys and tokens

### create your schema


```python3 -c "from app import db; db.create_all()"```

### run

```python3 app.py```
