from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from abc import ABCMeta, abstractmethod
import datetime
import inspect
import logging

import ldap3


logger = logging.getLogger(__name__)


class UserDirectory(object, metaclass=ABCMeta):
	"""Abstract base class for a user lookup backend"""

	@abstractmethod
	def all_users(self):
		"""Yields tuples (uid, is_expired)"""
		pass

	@abstractmethod
	def is_expired(self, uid):
		"""Is the User with this uid expired or non-existent?"""
		pass

	def __iter__(self):
		return self.all_users()


class LDAP(UserDirectory):
	"""Check if users are expired via LDAP. Highly customized, definitely requires adjustment"""

	# On my particular LDAP system multiple values are used for non-expiering accounts
	# You may want to extend this list
	_eternal_dates = [
		None, 
		datetime.datetime(1601, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
		datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=datetime.timezone.utc),
	]

	def __init__(self):
		super().__init__()

		self.server = ldap3.Server(settings.LDAP_SERVER, use_ssl=settings.LDAP_USE_SSL)
		self.conn = ldap3.Connection(self.server, user=settings.LDAP_USER, password=settings.LDAP_PASSWORD,
		                             authentication=settings.LDAP_AUTH_METHOD, client_strategy='SYNC',
		                             auto_referrals=True, check_names=True)
		
		if settings.LDAP_USE_TLS:
			self.conn.start_tls()
		self.conn.bind()

	def _is_date_expired(self, expirationDate):
		return expirationDate not in self._eternal_dates and expirationDate < datetime.datetime.now(datetime.timezone.utc)

	def all_users(self):
		paged_entries = self.conn.extend.standard.paged_search(
		                     settings.LDAP_SEARCH_BASE, '(uid=*)',
		                     attributes=['uid', 'accountExpires'])
		for entry_dict in paged_entries:
			attributes = entry_dict['attributes']
			# uid is a list. Here, we cover None and empty lists
			if not attributes.get('uid'):
				continue
			yield attributes['uid'][0], self._is_date_expired(attributes.get('accountExpires'))

	def is_expired(self, uid):
		search_pattern = '(uid={})'.format(uid) ## FIXME: Escape
		if not self.conn.search(settings.LDAP_SEARCH_BASE, search_pattern, attributes=['accountExpires']):
			return True
		entry = self.conn.entries[0]
		return 'accountExpires' in entry and self._is_date_expired(entry.accountExpires.value)


class Command(BaseCommand):
	help = 'Marks expired users accounts as inactive'
	
	requires_migrations_checks = True

	def global_to_local(self):
		"""Low load on directory, high on DB"""
		for uid, is_expired in self.directory:
			if is_expired:
				try:
					user = User.objects.filter(username=uid, is_active=True).get()
					logger.info('User {} is expired.'.format(user.username))
					user.is_active = False
					user.save()
				# pylint: disable=no-member
				except User.DoesNotExist:
					pass

	def global_from_local(self):
		"""High load on directory, low on DB"""
		for user in User.objects.filter(is_active=True):
			if self.directory.is_expired(user.username):
				logger.info('User {} is expired.'.format(user.username))
				user.is_active = False
				user.save()

	def handle(self, *args, **options):
		self.directory = LDAP()
		self.global_to_local()
