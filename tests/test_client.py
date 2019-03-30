import unittest
from app import create_app, db
from app.models import User, Role
from flask import url_for
import re

class FlaskClientTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		Role.insert_roles()
		self.client = self.app.test_client(use_cookies=True)

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_context.pop()

	def test_home_page(self):
		response = self.client.get(url_for('main.index'))
		self.assertTrue('Stranger' in response.get_data(as_text=True))

	def test_register_and_login(self):
		response = self.client.post(url_for('auth.register'), data ={
			'email': '131205@qq.com',
			'username': 'coolxc',
			'password': 'aaa',
			'password2':'aaa'
			})
		self.assertTrue(response.status_code == 302)
		response = self.client.post(url_for('auth.login'),data={
			'email': '131205@qq.com',
			'password': 'aaa',
			},follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue(re.search('Hello,\s+coolxc!', data))

		user = User.query.filter_by(email='131205@qq.com').first()
		token = user.generate_conofirmation_token()
		response = self.client.get(url_for('auth.confirm',token=token),follow_redirects=True)

		data = response.get_data(as_text=True)
		self.assertTrue('你已经确认了你的账户' in data)

		response = self.client.get(url_for('auth.logout'),follow_redirects=True)
		data = response.get_data(as_text=True)
		self.assertTrue('退出登录' in data)