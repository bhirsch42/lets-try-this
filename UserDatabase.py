from Handler import *

class MyUser(ndb.Model):
	google_user_id = ndb.StringProperty(required=True)
	first_name = ndb.StringProperty(required=True)
	last_name = ndb.StringProperty(required=True)

def addUser(fname, lname, attendings, attendingp):
	user = User(first_name=fname, last_name=lname, attending_service=attendings, attending_party=attendingp)
	user.put()