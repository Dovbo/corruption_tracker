"""corruption_tracker URL Configuration"""

from django.conf.urls import static
from django.urls import path, include
from django.conf import settings
from django.conf.urls import i18n
from django.contrib.gis import admin
from django.views.static import serve
from django.views.i18n import JavaScriptCatalog

from corruption_tracker import views
from api import urls as api_urls

js_info_dict = {}

urlpatterns = [
    # Rest API
    path('api/', include(api_urls.urlpatterns)),

    path('admin/', admin.site.urls),
    path('i18n/', include(i18n.urlpatterns)),
    path('jsi18n/', JavaScriptCatalog.as_view(), js_info_dict, name='javascript-catalog'),

    path('', views.MapPageView.as_view(), name="single"),

    path('', include('social.apps.django_app.urls', namespace='social')),
    path('login/', views.LoginView.as_view(),
        name='login'),

    path('logout/', views.logout_user,
        name='logout'),

    path('static/<path>', serve, {'document_root': settings.STATIC_ROOT}),

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        # path(r'profiling/', views.profiling),
        path(r'press/', include('blog.urls')),
        path(r'user/', include('interaction.urls')),
    ]
