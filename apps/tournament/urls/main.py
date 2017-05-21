from django.views.generic import TemplateView
from django.conf.urls import url
from apps.tournament import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^faq[/]$', TemplateView.as_view(template_name='main/intro.html'), name='faq'),
    url(r'^help[/]$', TemplateView.as_view(template_name='main/intro.html'), name='help'),
    url(r'^about[/]$', TemplateView.as_view(template_name='main/about.html'), name='about'),
    url(r'^soon[/]$', TemplateView.as_view(template_name='main/soon.html'), name='soon'),
    url(r'^news[/]$', TemplateView.as_view(template_name='main/news.html'), name='news'),
    url(r'^thanks[/]$', TemplateView.as_view(template_name='main/thanks.html'), name='thanks'),
    url(r'^feedback[/]$', views.feedback, name='feedback'),
    url(r'^support[/]$', TemplateView.as_view(template_name='main/support.html'), name='support'),
]
