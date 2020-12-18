from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import PubSSHKey

def index(request):
	pubsshkey_list = PubSSHKey.objects.all()
	context = {
		'pubsshkey_list': pubsshkey_list,
	}
	return render(request, 'authorized_keys/index.html', context)


def add(request):
	try:
		pubsshkey = PubSSHKey.create(
				user_input=request.POST['content'],
				# missing user
				title=request.POST.get('title'), # optional
			)
		pubsshkey.save()
	except KeyError:
		return HttpResponseBadRequest("Invalid POST data")
	except ValidationError as e:
		messages.error(request, "Invalid key: {}".format("<br />".join(line for line in e)))
	except Exception as e:
		messages.error(request, repr(e))
	else:
		messages.success(request, "Added key {}".format(pubsshkey.fingerprint))
	return HttpResponseRedirect(reverse('authorized_keys:index'))


def delete(request, key_id):
	pubsshkey = get_object_or_404(PubSSHKey, pk=key_id)

	# if k.user !=
	#	error_message = "That's not your key"
	# else:
	pubsshkey.delete()
	messages.success(request, 'Deleted key {}'.format(pubsshkey.fingerprint))

	return HttpResponseRedirect(reverse('authorized_keys:index'))