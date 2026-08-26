from pymongo import MongoClient
from datetime import datetime, timezone

MONGODB_URL = 'mongodb+srv://bhanu:1234@cluster0.fgh4i8m.mongodb.net'
client = MongoClient(MONGODB_URL)

# The connection string's host is cluster0.fgh4i8m.mongodb.net
# The default database is usually the one after the host; let's try 'admin' or list dbs
dbs = client.list_database_names()
print('Available databases:', dbs)

# Try using 'Cluster0' as the database name (common for Atlas)
db = client['Cluster0']
users = db['users']

# Delete any existing user with this email
users.delete_one({'email': 'sridevi72901@gmail.com'})
print('Deleted any existing user')

# Insert fresh with proper datetime
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=['sha256_crypt', 'pbkdf2_sha256'], deprecated='auto')
hashed = pwd_context.hash('lubuma@1234')
now = datetime.now(timezone.utc)

user_doc = {
    'email': 'sridevi72901@gmail.com',
    'name': 'Admin',
    'password_hash': hashed,
    'plan': 'enterprise',
    'is_admin': True,
    'interviews_used': 0,
    'resumes_used': 0,
    'aptitude_used': 0,
    'cover_letters_used': 0,
    'monthly_reset_date': now,
    'created_at': now,
    'last_active': now,
}
result = users.insert_one(user_doc)
print(f'Inserted user with id: {result.inserted_id}')
print(f'Email: sridevi72901@gmail.com')
print(f'monthly_reset_date is datetime: {isinstance(user_doc[\"monthly_reset_date\"], datetime)}')