#coding: utf-8
from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static
from rentv_crm.views import ClientsListView, ClientDetailView 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
url(r'^$', ClientsListView.as_view(), name='list'), # то есть по URL http://имя_сайта/blog/ 
                                               # будет выводиться список постов
url(r'^(?P<pk>\d+)/$', ClientDetailView.as_view()), # а по URL http://имя_сайта/blog/число/ 
                                              # будет выводиться пост с определенным номером

)
#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
