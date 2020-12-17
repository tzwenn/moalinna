#!/usr/bin/env python3

######################
#
# This is your AuthorizedKeysCommand in sshd
#

import sys
import os

def is_user_expired(username):
	""" Test if the user accout is expired or enabled """
	return False

def read_sshkeys(username):
	sys.path.append(os.path.join(os.path.dirname(__file__), 'moalinna'))
	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moalinna.settings')
	
	import django
	django.setup()

	from django.contrib.auth.models import User
	from authorized_keys.models import PubSSHKey

	return PubSSHKey.objects.filter(user__username=username)

def main(username):
	if not is_user_expired(username):
		for key in read_sshkeys(username):
			print(key.AUTHORIZED_KEYS)

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		sys.stderr.write("Usage: %s USERNAME\n" % sys.argv[0])
		sys.exit(1)
	main(sys.argv[1])

