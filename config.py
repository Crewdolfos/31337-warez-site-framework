import hashlib

DB_FILENAME = ':memory:'

USERS = [
         ('robert', hashlib.sha256(b'ardly_secure').hexdigest(), 'trying@n00biesz', 0),
         ('h4rr11', hashlib.sha256(b'brdly_secure').hexdigest(), 'harr1@flat3arth', 0),
	 ('pyr0', hashlib.sha256(b'hardly_secure').hexdigest(), 'bo$$@cr3wdolfos', 1),
         ('archie', hashlib.sha256(b'crdly_secure').hexdigest(), 'ilof@cr3wdolfos', 0),
]

MSGS = [
	('admin', 'robert', 'Welcome!', 'Hello fellow cracker.'),
        ('admin', 'h4rr11', 'Welcome!', 'Hello fellow cracker.'),
        ('archie', 'bigb0$$', 'New stuffz', 'Sent you the info to your crewaddress.'),
]

LOGIN_QUERY = "SELECT * FROM users WHERE login = '{}' and password = '{}';"
MSG_QUERY = "SELECT * FROM messages WHERE to_ = '{}';"

SEND_QUERY = "INSERT INTO messages VALUES (?,?,?,?);"
