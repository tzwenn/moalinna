from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from authorized_keys.models import PubSSHKey

class Command(BaseCommand):
	help = 'This is your AuthorizedKeysCommand in sshd'
	
	requires_migrations_checks = True

	def read_sshkeys(self, username):
		# pylint: disable=no-member
		return PubSSHKey.objects.filter(user__username=username, user__is_active=True)

	def add_arguments(self, parser):
		parser.add_argument('username', type=str)

	def handle(self, *args, **options):
		for key in self.read_sshkeys(options["username"]):
			print(key.AUTHORIZED_KEYS)
