#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from Handler import *
import Database

class MainHandler(Handler):
	def get(self):
		self.render('home.html', user=self.get_user())

class LoginHandler(Handler):
	def get(self):
		# Login to Google
		user = self.get_google_user()
		if not user:
			self.redirect(users.create_login_url('/login'))
			return

		if not Database.is_registered_user(user):
			self.render('login_user_doesnt_exist.html', user=self.get_user())
			return

		self.redirect('/')


class CreateAccountHandler(Handler):
	def get(self):
		if Database.is_registered_user(self.get_google_user()):
			self.render('user_already_exists.html', user=self.get_user())
		else:
			self.render('create_user.html', user=self.get_user())

	def post(self):
		first_name = self.request.get('first_name')
		last_name = self.request.get('last_name')
		user = self.get_google_user();
		if not user:
			self.redirect('/login')
		elif first_name == '' or last_name == '':
			self.render('create_user.html', user=self.get_user(), error=True)
		else:
			Database.addUser(user.user_id(), first_name, last_name)
			self.render('user_created.html', user=self.get_user())

class LogoutHandler(Handler):
	def get(self):
		user = self.get_google_user()
		if not user:
			self.redirect('/')
		self.redirect(users.create_logout_url('/'))

class AdminHandler(Handler):
	def get(self):
		user = self.get_user()
		if user.is_a_moderator
			self.render('moderator.html', user=user)
			return
		self.render('permission_denied.html', user=user)

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/login', LoginHandler),
	('/login/createaccount', CreateAccountHandler),
	('/logout', LogoutHandler),
	('/admin', AdminHandler)
], debug=True)
