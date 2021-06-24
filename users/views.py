import json

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import CreateView

from foodgram import settings
from users.models import Contact, User

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'reg.html'


@require_POST
@login_required
def subscriptions_add(request):
    user_id = json.loads(request.body).get('id')
    user_to = get_object_or_404(User, id=user_id)
    user_from = request.user
    if Contact.objects.filter(user_to=user_to, user_from=user_from).exists():
        return JsonResponse({'success': False})
    Contact(user_to=user_to, user_from=user_from).save()
    return JsonResponse({'success': True})


@require_http_methods(['DELETE', ])
@login_required
def subscriptions_remove(request, user_id):
    user_to = get_object_or_404(User, id=user_id)
    user_from = request.user
    if not Contact.objects.filter(user_to=user_to,
                                  user_from=user_from).exists():
        return JsonResponse({'success': False})
    Contact.objects.get(user_to=user_to, user_from=user_from).delete()
    return JsonResponse({'success': True})


@login_required
def subscriptions(request):
    user_from = request.user
    authors = user_from.following.all().prefetch_related(
        'recipes').annotate(recipe_count=Count('recipes')).order_by('username')
    paginator = Paginator(authors, settings.RECORDS_ON_THE_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'page': page,
        'paginator': paginator,
    }
    return render(request, 'subscriptions.html', context)
