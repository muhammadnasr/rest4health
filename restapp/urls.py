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

    path('tables/', views.TableList.as_view()),
    path('tables/<int:pk>/', views.TableDetail.as_view()),

    path('reservations/', views.ReservationList.as_view()),
    path('reservations/<int:pk>/', views.ReservationDetail.as_view()),
    path('reservations/available/<int:seats_count>/', views.ReservationAvailable.as_view()),
    path('reservations/today/', views.ReservationToday.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)
