from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import base64
import binascii
import hashlib

class PubSSHKey(models.Model):
	keytype = models.CharField(max_length=32)
	"""key type as of sshd(8)"""

	pubkey = models.BinaryField()
	"""Public key (decoded from base64)"""

	comment = models.CharField(max_length=64)
	"""User comment field"""

	title = models.CharField(max_length=64)
	"""User defined title"""

	creation_date = models.DateTimeField(auto_now_add=True)
	last_used = models.DateTimeField(null=True, blank=True)
	
	user = models.ForeignKey(User,
			related_name='pubkey',
			on_delete=models.CASCADE
		)

	@property
	def md5fp(self):
		"""Computes MD5 fingerprint"""
		fp = hashlib.md5(self.pubkey).hexdigest()
		return ':'.join(a + b for a, b in zip(fp[::2], fp[1::2]))

	@property
	def sha256fp(self):
		"""Computes SHA256 fingerprint"""
		# I am aware of stripping the base64 padding. Haven't found it elsewhere with SHA256 fps
		return "SHA256:" + base64.b64encode(hashlib.sha256(self.pubkey).digest()).decode('ascii').rstrip('=')

	@property
	def fingerprint(self):
		return self.sha256fp if settings.USE_SHA256_FINGERPRINTS else self.md5fp

	@property
	def AUTHORIZED_KEYS(self):
		"""Reconstructs sshd(8) AUTHORIZED_KEYS format"""
		return "{} {}".format(self.keytype, base64.b64encode(self.pubkey).decode('ascii'))

	def __str__(self):
		return "PubSSHKey<{} of {}>".format(repr(self.title), self.user.username)

	class Meta:
		unique_together = (("keytype", "pubkey"), )

	@classmethod
	def create(cls, user_input, user=None, title=None):
		# Options are not supported
		l = user_input.strip().split()
		if len(l) < 3:
			l.append(None)

		try:
			keytype, b64pubkey, comment = l
		except ValueError:
			raise ValidationError("Pubkeys need to be space seperated list (keytype key [comment])")

		try:
			pubkey = base64.b64decode(b64pubkey.encode('ascii'))
		except (binascii.Error, UnicodeEncodeError):
			raise ValidationError("Key data is not base64 encoded")

		res = cls(
					keytype=keytype,
					pubkey=pubkey,
					comment=comment,
					title=title,
					user=user
				)
		return res


###########################

	####################
	# Future Extended Options?
	#   (see AUTHORIZED_KEYS in sshd(8))
	# * permitopen
	# * no-port-forwarding
	# * from
