from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import PubSSHKey

testdata = [{
		"file": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDMf9t1tv4gCXctP8GEL6MaAy/ZEHESJvSeDK4IdZl0T8irB9xM+BN5rw+FxIB0IUl7hFAN82p8Z8nBiBmnDuz1A1cPVbJKbwQY1xXXougbOSsbKTFybwq1KF4pGUtVgf9fsYjYks3gNaj5Vu3hX37du2H0jpjOu9g921SUSCX8CQZtpkucDDeHhzL9A6w2wLiYyiF+sLtl579LhwIFG6DaTc348rO1EtHddpG10L10UrS/spiKO2m71+Sk5vQVIo57USG8MSM7AJkqkId0MAUiqoD1Cn1ihiCL0lBwtm7PYQITjjnSfr+z9hKSdPHPwdz/LDqmodgy7XDwDmu3RbiL sheep@pasture",
		"keytype": "ssh-rsa",
		"md5fp": "d4:3c:c8:39:f7:c3:cc:1e:99:d6:f9:c8:c4:13:14:e1",
		"comment": "sheep@pasture",
		"sha256fp": "SHA256:lxfaWMqFWQKTdN32cT7saRHsGCYtahwHqtdWjEPVgG0",
	}]


class PubSSHKeyTests(TestCase):

	def test_valid_creation(self):
		for data in testdata:
			pubkey = PubSSHKey.create(data["file"])
			self.assertEqual(pubkey.keytype, data["keytype"])
			self.assertEqual(pubkey.md5fp, data["md5fp"])
			self.assertEqual(pubkey.sha256fp, data["sha256fp"])
			self.assertEqual(pubkey.comment, data["comment"])

	def test_creating_missing_comment(self):
		for data in testdata:
			nc_data = " ".join(data["file"].split(" ")[:2])
			pubkey = PubSSHKey.create(nc_data)
			self.assertEqual(pubkey.keytype, data["keytype"])
			self.assertEqual(pubkey.md5fp, data["md5fp"])
			self.assertEqual(pubkey.sha256fp, data["sha256fp"])
			self.assertIsNone(pubkey.comment)

	def test_invalid_b64(self):
		with self.assertRaises(ValidationError):
			PubSSHKey.create("ssh-rsa Broken sheep@pasture")
		with self.assertRaises(ValidationError):
			PubSSHKey.create("ssh-rsa Bröken sheep@pasture")

	def test_invalid_file(self):
		with self.assertRaises(ValidationError):
			PubSSHKey.create("Badly Bröken Beyond Repair")

