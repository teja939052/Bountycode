from pymongo import MongoClient
from datetime import datetime, timezone

MONGODB_URL = 'mongodb+srv://bhanu:1234@cluster0.fgh4i8m.mongodb.net'
client = MongoClient(MONGODB_URL)
db = client.get_database()
users = db['users']

# Fix the user document: set monthly_reset_date to None so the code will set it to 'now'
result = users.update_one(
    {'email': 'sridevi72901@gmail.com'},
    {'$set': {'monthly_reset_date': None}}
)
print(f'Matched: {result.matched_count}, Modified: {result.modified_count}')

# Verify the document
user = users.find_one({'email': 'sridevi72901@gmail.com'})
print('User document after fix:')
for k, v in user.items():
    if k != 'password_hash':
        print(f'  {k}: {repr(v)} (type: {type(v).__name__})')