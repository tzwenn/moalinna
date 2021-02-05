from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from authorized_keys.models import PubSSHKey

import logging
import os
import socketserver


logger = logging.getLogger(__name__)


class ReusableThreadingUnixStreamServer(socketserver.ThreadingUnixStreamServer):

	"""Cleans up socket file before & after usage"""

	enable_unlink = True

	def unlink(self):
		if self.enable_unlink:
			try:
				os.unlink(self.server_address)
			except FileNotFoundError:
				pass

	def server_bind(self):
		self.unlink()
		super().server_bind()

	def server_close(self):
		super().server_close()
		self.unlink()


class KeyRequestHandler(socketserver.StreamRequestHandler):

	def read_sshkeys(self, username):
		# pylint: disable=no-member
		return PubSSHKey.objects.filter(user__username=username, user__is_active=True)

	def handle(self):
		username = self.rfile.readline().strip().decode()
		answer = ''.join(key.AUTHORIZED_KEYS + '\n' for key in self.read_sshkeys(username))
		self.wfile.write(answer.encode())


class Command(BaseCommand):

	help = 'Runs a server, that answers for usernames send via TCP with authorized keys'

	def add_arguments(self, parser):
		bindoptions = parser.add_mutually_exclusive_group(required=False)

		default_addr = 'localhost'
		default_port = 9876

		bindoptions.add_argument('-b', '--bind',
					default=default_addr, type=str, metavar='ADDRESS',
                    help='Specify alternate bind address'
                         '[default: {}]'.format(default_addr))
		bindoptions.add_argument('-u', '--unix', metavar='FILENAME',
		            help='Specify a unix socket to bind to instead')
		
		parser.add_argument('port', action='store',
                    default=default_port, type=int,
                    nargs='?',
                    help='Specify alternate port [default: {}]'.format(default_port))

	def server_and_address(self, options):
		if options['unix']:
			address = options['unix']
			return ReusableThreadingUnixStreamServer, address, 'unix:' + address
		else:
			address = (options['bind'], options['port'])
			return socketserver.ThreadingTCPServer, address, 'tcp://{}:{}'.format(*address)

	def handle(self, *args, **options):
		server_class, address, address_log = self.server_and_address(options)
		logger.info('Listening on {} for key requests'.format(address_log))
		with server_class(address, KeyRequestHandler) as server:
			try:
				server.serve_forever()
			except KeyboardInterrupt:
				pass
			logger.info('Exiting')
