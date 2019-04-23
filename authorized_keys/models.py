from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import base64
import binascii
import hashlib

class PubSSHKey(models.Model):
	keytype = models.CharField(max_length=32)
	"""key type as of sshd(8)"""

	pubkey = models.TextField()
	"""Public key (decoded from base64)"""

	comment = models.CharField(max_length=64)
	"""User comment field"""

	title = models.CharField(max_length=64)
	"""User defined title"""

	creation_date = models.DateTimeField(auto_now_add=True)
	last_used = models.DateTimeField()
	
	user = models.ForeignKey(User,
			related_name='pubkey',
			on_delete=models.CASCADE
		)

	@property
	def fingerprint(self):
		"""Computes SHA1 fingerprint"""
		fp = hashlib.md5(self.pubkey).hexdigest()
		return ':'.join(a + b for a, b in zip(fp[::2], fp[1::2]))

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
			raise ValidationError("Pubkeys need to be space seperated list: keytype key [comment]")

		try:
			pubkey = base64.b64decode(b64pubkey.encode('ascii'))
		except (binascii.Error, UnicodeEncodeError):
			raise ValidationError("Key is not base64 encoded")

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
