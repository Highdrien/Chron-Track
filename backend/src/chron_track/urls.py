"""
URL configuration for chron_track project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from ninja import NinjaAPI
from ninja.security import django_auth

from races.views import router as races_router

api = NinjaAPI(
    title="Chron Track API",
    version="0.1.0",
    description="API to manage Chron Track",
    docs_url="/docs",
    auth=django_auth,
)


@api.get("/api/health", auth=None, tags=["Health"])
def health_check(request):
    return {"status": "ok"}


api.add_router("/api/races", races_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]
