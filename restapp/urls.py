from django.urls import include, path
from . import views
from rest_framework import routers
from restapp import views
from rest_framework.urlpatterns import format_suffix_patterns


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', views.index, name='index'),
    #path('', include(router.urls)),

    path('tables/', views.TableList.as_view()),
    path('tables/<int:pk>/', views.TableDetail.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
