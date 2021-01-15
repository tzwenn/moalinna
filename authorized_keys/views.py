from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.translation import gettext as _

from .models import PubSSHKey

def format_as_code(text):
	return '<span class="is-family-code">{}</span>'.format(text)

@login_required
def index(request):
	mypk = request.user.pk
	pubsshkey_list = PubSSHKey.objects.filter(user__pk=mypk)
	context = {
		'pubsshkey_list': pubsshkey_list,
	}
	return render(request, 'authorized_keys/index.html', context)


@login_required
def add(request):
	try:
		pubsshkey = PubSSHKey.create(
				user_input=request.POST['content'],
				user=request.user,
				title=request.POST.get('title'), # optional
			)
		pubsshkey.save()
	except KeyError:
		return HttpResponseBadRequest("Invalid POST data")
	except ValidationError as e:
		messages.error(request, _("Invalid key: {}").format("<br />".join(line for line in e)))
	except IntegrityError as e:
		messages.error(request, _("Integrity Error: Has this key already been added?"))
	except Exception as e:
		messages.error(request, repr(e))
	else:
		messages.success(request, _("Added key {}.").format(format_as_code(pubsshkey.fingerprint)), extra_tags='safe')
	return HttpResponseRedirect(reverse('authorized_keys:index'))


@login_required
def delete(request, key_id):
	pubsshkey = get_object_or_404(PubSSHKey, pk=key_id)

	if pubsshkey.user.pk != request.user.pk:
		messages.error(request, _("That's not your key!"))
	else:
		try:
			pubsshkey.delete()
		except Exception as e:
			messages.error(request, _("Cannot delete: {}.").format(repr(e)))
		else:
			messages.success(request, _("Deleted key {}.").format(format_as_code(pubsshkey.fingerprint)), extra_tags='safe')

	return HttpResponseRedirect(reverse('authorized_keys:index'))