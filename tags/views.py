# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


from tags.models import Tag


@login_required
def tags_management(request):
    tags = Tag.objects.filter(owner=request.user)
    c = {
        "tags": tags,
    }
    return render(request, "tags/management.html", c)

