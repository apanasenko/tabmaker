from django.urls import include
from django.views.generic import TemplateView
from django.conf.urls import url
from apps.tournament import views
from apps.tournament.api import urls as api_urls

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^faq[/]$', TemplateView.as_view(template_name='main/intro.html'), name='faq'),
    url(r'^help[/]$', TemplateView.as_view(template_name='main/intro.html'), name='help'),
    url(r'^about[/]$', TemplateView.as_view(template_name='main/about.html'), name='about'),
    url(r'^soon[/]$', TemplateView.as_view(template_name='main/soon.html'), name='soon'),
    url(r'^news[/]$', TemplateView.as_view(template_name='main/news.html'), name='news'),
    url(r'^thanks[/]$', TemplateView.as_view(template_name='main/thanks.html'), name='thanks'),
    url(r'^policy[/]$', TemplateView.as_view(template_name='main/policy.html'), name='policy'),
    url(r'^feedback[/]$', views.feedback, name='feedback'),
    url(r'^support[/]$', views.support, name='support'),
    url(r'^api/', include(api_urls)),
]
