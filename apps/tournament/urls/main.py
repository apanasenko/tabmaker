from django.views.generic import TemplateView
from django.conf.urls import patterns, url
from apps.tournament import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^faq[/]$', TemplateView.as_view(template_name='main/intro.html'), name='faq'),
    url(r'^help[/]$', TemplateView.as_view(template_name='main/intro.html'), name='help'),
    url(r'^about[/]$', TemplateView.as_view(template_name='main/about.html'), name='about'),
    url(r'^soon[/]$', TemplateView.as_view(template_name='main/soon.html'), name='soon'),
    url(r'^news[/]$', TemplateView.as_view(template_name='main/news.html'), name='news'),
    url(r'^thanks[/]$', TemplateView.as_view(template_name='main/thanks.html'), name='thanks'),
    url(
        r'^new_tournament_confirm[/]$',
        TemplateView.as_view(template_name='tournament/new_tournament_confirm.html'),
        name='new_tournament_confirm'),

        # TODO настроить ссылку на страницу с формой после отправки формы создания турнира

    url(
        r'^tabmaker_feedback[/]$',
        TemplateView.as_view(template_name='main/tabmaker_feedback.html'),
        name='tabmaker_feedback'),
)