from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import Permission

# Create your views here.


def test_view(request):
    perms_count = Permission.objects.count()
    return HttpResponse(f"{perms_count}".encode("utf-8"))
