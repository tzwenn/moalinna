# Moalinna

-- *Gateway to the sheep pasture.*

A web interface to store SSH keys for public key authentication in a database, that can be used with OpenSSH's [`AuthorizedKeysCommand`](https://man.openbsd.org/sshd_config#AuthorizedKeysCommand).

## Testing & Development

For your local development setup, install the requirements in a virtual environment, copy the sample settings and create a database.

```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
cp settings.ini.sample settings_dev.ini
./manage.py migrate
./manage.py runserver
```

Now you can access the running instance at http://localhost:8000.

Moalinna requires an [OpenID Connect provider](https://openid.net/connect/) for user authentication in the web interface. If you don't have one at hand, create a local user and login first via the [local admin interface](http://localhost:8000/admin) and afterwards return to the [start page](http://localhost:8000).

```
./manage.py createsuperuser
```

## References

* We use OpenSSH's [`AuthorizedKeysCommand`](https://man.openbsd.org/sshd_config#AuthorizedKeysCommandg)
* We accept key in the [sshd(8) `AUTHORIZED_KEYS` file format](https://man.openbsd.org/sshd.8#AUTHORIZED_KEYS_FILE_FORMAT)
* How [GitLab does it](https://docs.gitlab.com/ee/administration/operations/fast_ssh_key_lookup.html)
* How [Google NSCache does it](https://github.com/google/nsscache/blob/master/examples/authorized-keys-command.py)

