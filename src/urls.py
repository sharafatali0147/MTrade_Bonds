from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from src.users.urls import users_router
from src.bonds.views import BondsViewSet

schema_view = get_schema_view(
    openapi.Info(title="Bonds API", default_version='v1'),
    public=True,
)

router = DefaultRouter()

router.registry.extend(users_router.registry)

urlpatterns = [
    # admin panel
    path('admin/', admin.site.urls),
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # summernote editor
    path('summernote/', include('django_summernote.urls')),
    # api
    path('api/v1/', include(router.urls)),
    url(r'^api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # auth
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Bonds
    path('bonds/all', BondsViewSet.bonds_list, name='bonds_list'),
    path('bonds/get_published', BondsViewSet.get_published),
    path('bonds/create', BondsViewSet.bonds_create, name='bonds_create'),
    path('bonds/purchase/<str:id>', BondsViewSet.bonds_purchase),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
