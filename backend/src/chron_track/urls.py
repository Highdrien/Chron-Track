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
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.routers.obtain import obtain_pair_router
from ninja_jwt.routers.verify import verify_router

from accounts.api import router as auth_router
from races.api import router as races_router

api = NinjaAPI(
    title="Chron Track API",
    version="0.1.0",
    description="API to manage Chron Track",
    docs_url="/docs",
    auth=[JWTAuth(), django_auth],
)


@api.get("/api/health", auth=None, tags=["Health"])
def health_check(request):
    return {"status": "ok"}


api.add_router("/api/auth/token", obtain_pair_router, tags=["Auth"])
api.add_router("/api/auth/token", verify_router, tags=["Auth"])
api.add_router("/api/auth", auth_router)
api.add_router("/api/races", races_router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", api.urls),
]
