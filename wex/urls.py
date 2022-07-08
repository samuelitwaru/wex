"""wex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static
from core.urls import *
from . import router
from core.views import AuthLoginView, AuthLogoutView

more_patterns = []

# add urls for app if the app in installed
if 'procurement' in settings.INSTALLED_APPS: from procurement.urls import *
if 'results' in settings.INSTALLED_APPS: 
    from results.urls import *
    more_patterns += nested_url_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/', include(router.urls)),
    path('api/auth/login/', AuthLoginView.as_view()),
    path('api/auth/logout/', AuthLogoutView.as_view()),
] + more_patterns

# add accounts urls if 'accounts' app in installed
if 'accounts' in settings.INSTALLED_APPS: 
    urlpatterns.append(re_path("^accounting/", include("accounts.urls")))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns.append(
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    )

if settings.DEBUG:
    from django.views.generic import TemplateView
    from rest_framework.schemas import get_schema_view

    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    urlpatterns.extend([
        path('openapi', get_schema_view(
                title="Your Project",
                description="API for all things …",
                version="1.0.0"
            ), name='openapi-schema'),
        path('swagger-ui/', TemplateView.as_view(
            template_name='swagger-ui.html',
            extra_context={'schema_url':'openapi-schema'}
        ), name='swagger-ui'),
    ])