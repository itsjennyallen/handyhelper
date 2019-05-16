from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^$', views.register_form),
    url(r'^users$',views.register_user),
    url(r'^login$',views.login_user),
    url(r'^dashboard$',views.dashboard),
    url(r'^jobs/new$',views.new_job),
    url(r'^jobs/create$',views.create_job),
    url(r'^jobs/(?P<id>\w+)$',views.job_details),
    url(r'^delete/(?P<id>\w+)$',views.delete),
    url(r'^jobs/edit/(?P<id>\w+)$',views.edit_job),
    url(r'^jobs/update/(?P<id>\d+)$',views.update),
    url(r'^$',views.logout),
]