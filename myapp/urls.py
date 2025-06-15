from django.urls import path
from . import views
import os
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('kiki/', views.MainPage),
    path('signin/', views.SignInPage, name='SignInPage'), 
    path('', views.cool, name='reg'),
    path('profilepicimg/', views.profilepicimg), #no html
    path('usernamenew/', views.usernamenew), #no html
    path('bionew/', views.bionew), #no html
    path('name/', views.namenew), #no html
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'myapp/static'))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)