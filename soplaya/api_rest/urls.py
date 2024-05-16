from django.urls import path, include
from api_rest.models import Report
from django.views.generic import ListView
from django.conf.urls.static import static
from api_rest import views
from django.conf import settings
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'report', views.ReportViewSet)

urlpatterns = [
    path('', ListView.as_view(
        queryset = Report.objects.all(),
        template_name = "index.html"), name = 'home'),
    path('load/', views.loadData, name='load_table'),
    path('json/', views.JsonData, name='json'),
    path('differences/', views.differences, name='differences'),
    path('calculate_differences/', views.calculate_differences, name='calculate_differences'),
    path('reset/', views.resetData, name='reset_table'),
    path('filter/', views.filtered_report, name='filter'),
    path('api/', include(router.urls), name='api'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)