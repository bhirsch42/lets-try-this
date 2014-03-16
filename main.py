#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from Handler import *
from google.appengine.api import users
from UserDatabase import *

class MainHandler(Handler):
	def get(self):
		self.render("home.html")

class LoginHandler(Handler):
	def get(self):
		# Login to Google
		user = users.get_current_user()
		if not user:
			self.redirect(users.create_login_url('/login'))
			return

		if not is_registered_user(user):
			self.render("login_user_doesnt_exist.html")

# IN PROGRESS.  STOPPED WORKING HERE
class CreateAccountHandler(Handler):
	def get(self):
		self.render("create_user.html")

	def post(self):
		first_name = self.request.get("first_name")
		last_name = self.request.get("last_name")
		if first_name == '' or last_name == '':
			self.render('create_user.html', error=True)
		else:
			UserDatabase.addUser(first_name, last_name, user.user_id())
			self.render('user_created.html')

# SHOULD MOVE SOMEWHERE LOGICAL
def is_registered_user(user):
	registered_users = ndb.gql("SELECT * FROM MyUser")
	user_ids = [registered_user.google_user_id for registered_user in registered_users]
	user_exists = user.user_id() in user_ids

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/login', LoginHandler),
	('/login/createaccount', CreateAccountHandler)
], debug=True)
