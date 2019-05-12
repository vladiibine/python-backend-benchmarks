from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import Permission

# Create your views here.


def one_query_view(request):
    perms_count = Permission.objects.count()
    return HttpResponse(f"{perms_count}".encode("utf-8"))

def ten_queries_view(request):
    count = 0

    for _ in range(10):
        count += Permission.objects.count()

    return HttpResponse(f"{count}".encode("utf-8"))

