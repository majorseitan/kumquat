# Setup
## configure with your credentials

   mv config.py.sample config.py

   https://developer.twitter.com/en/apps
   details -> keys and tokens

## create your schema

```python
from app import db
db.create_all()
```
