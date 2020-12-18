from django.http import HttpResponse
from django.shortcuts import render

from .models import PubSSHKey

def index(request):
	pubsshkey_list = PubSSHKey.objects.all()
	context = {'pubsshkey_list': pubsshkey_list}
	return render(request, 'authorized_keys/index.html', context)


def add(request):
	return HttpResponse("Not added")

def delete(request, key_id):
	return HttpResponse("Key %d not deleted" % key_id)