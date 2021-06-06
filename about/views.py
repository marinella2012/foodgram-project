from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutAuthorPage(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context['text'] = 'На создание этой страницы у меня ушло пять минут!'
        return context


class AboutTechPage(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О технологиях'
        context['text'] = 'https://github.com/marinella2012/foodgram-project'
        return context
