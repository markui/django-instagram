from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static

from . import views, apis

urlpatterns = [
    url(r'^', include(views)),
    url(r'^api/', include(apis, namespace='api'))
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
