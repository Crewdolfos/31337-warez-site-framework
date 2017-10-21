#!/usr/bin/env python3.5

from config import DB_FILENAME, USERS, MSGS, LOGIN_QUERY, MSG_QUERY, SEND_QUERY
from views import index_view, board_view, landing_view

import asyncio
import base64
import sqlite3
import hashlib
import os
import time

from aiohttp import web
from aiohttp_session import setup, get_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

	 
async def index(request):
	fail = request.GET.get('fail', '') # Safe
	return web.Response(body=index_view.format(fail), content_type='text/html')


async def quote(request):
	filters = ['proc', 'sys', 'home', '.py', '.pyc', '/opt']
	quotes = {'quote1.txt': 'Quote1',
		  'quote2.txt': 'Quote2',
		  'quote3.txt': 'Quote3'}
	filename = request.GET.get('file', 'quote1.txt')

	for f in filters:
		if f in filename:
			return web.json_response({'result': 'Filename filtered'})

	if filename in quotes:
		return web.json_response({'result': quotes[filename]})

	try:
		cwd = os.path.dirname(os.path.realpath(__file__)) + '/'
		with open(cwd + filename, 'r') as fp:
			return web.json_response({'result': fp.read()})
	except:
		return web.json_response({'result': 'Something went wrong!'})


async def landing(request):
	return web.Response(body=landing_view, content_type='text/html')

	

async def login(request):
	data = await request.post()
	user = data.get('login', None)
	password = data.get('password', None)

	await asyncio.sleep(2)  # m4d bruteforce protection 

	if len(user) > 8:
		return web.HTTPFound('/verysecret?fail=NAME%20TOO%20LONG')

	if user and password:
		db_connection = request.app['db_connection']
		c = db_connection.cursor()
		digest = hashlib.sha256(password.encode('utf-8')).hexdigest()
		print(LOGIN_QUERY.format(user, digest))
		c.execute(LOGIN_QUERY.format(user, digest))
		users = c.fetchall()
		print(users)
		
		if users == []:
			return web.HTTPFound('/verysecret?fail=NOT%20FOUND')

		user, stored_digest, _, is_admin = users[0]

		session = await get_session(request)
		session['login'] = user
		session['is_admin'] = is_admin
		return web.HTTPFound('/board')

	return web.HTTPFound('/verysecret?fail=EMPTY')


async def logout(request):
	session = await get_session(request)
	session.invalidate()
	return web.HTTPFound('/verysecret')


async def board(request):
	fail = request.GET.get('fail', '') # Safe
	session = await get_session(request)
	login = session['login'] if 'login' in session else None
	if not login:
		return web.HTTPFound('/verysecret')
	db_connection = request.app['db_connection']
	c = db_connection.cursor()
	c.execute(MSG_QUERY.format(login))
	msgs = c.fetchall()
	table = '<p>Logged in as {}</p>'.format(login)
	for m in msgs:
		table += '<h4>{} from {}</h4>'.format(m[2], m[0])
		table += '<p>{}</p>'.format(m[3])
	return web.Response(body=board_view.format(table, fail), content_type='text/html')

async def sendm(request):
	session = await get_session(request)
	login = session['login'] if 'login' in session else None
	if not login:
		return web.HTTPFound('/verysecret')

	data = await request.post()
	user = data.get('user', None)
	msg = data.get('message', None)

	await asyncio.sleep(2)  # m4d bruteforce protection 

	if user and msg:
		db_connection = request.app['db_connection']
		c = db_connection.cursor()
		print(SEND_QUERY, (login, user, 'New Mail', msg))
		try:
			c.execute(SEND_QUERY, (login, user, 'New Mail', msg))
		except:
			return web.HTTPFound('/board?fail=NOT%20FOUND')
		return web.HTTPFound('/board?fail=SENT')
	return web.HTTPFound('/board?fail=ERROR')



def setup_app(db_connection):
	app = web.Application()
	app['db_connection'] = db_connection

	fernet_key = fernet.Fernet.generate_key()
	secret_key = base64.urlsafe_b64decode(fernet_key)
	setup(app, EncryptedCookieStorage(secret_key))

	app.router.add_get('/', landing)
	app.router.add_get('/verysecret', index)
	app.router.add_get('/quote', quote)
	app.router.add_get('/board', board)
	app.router.add_post('/login', login)
	app.router.add_post('/send', sendm)
	app.router.add_get('/logout', logout)
	app.router.add_static('/static', 'static/')
	web.run_app(app, host='0.0.0.0', port=80)


def setup_db():
	db_connection = sqlite3.connect(DB_FILENAME)
	c = db_connection.cursor()
	with open('schema.sql') as fp:
		c.executescript(fp.read())
	c.executemany('INSERT INTO users VALUES (?,?,?,?)', USERS)
	c.executemany('INSERT INTO messages VALUES (?,?,?,?)', MSGS)
	db_connection.commit()
	return db_connection


if __name__ == '__main__':
	db_connection = setup_db()
	setup_app(db_connection)
