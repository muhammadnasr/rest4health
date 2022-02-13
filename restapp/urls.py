from django.urls import include, path
from .views import reservation_views
from .views import tables_views
from rest_framework import routers
from restapp.views import reservation_views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'users', tables_views.UserViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', tables_views.index, name='index'),

    path('tables/', tables_views.TableList.as_view()),
    path('tables/<int:pk>/', tables_views.TableDetail.as_view()),

    path('reservations/', reservation_views.ReservationList.as_view()),
    path('reservations/<int:pk>/', reservation_views.ReservationDetail.as_view()),
    path('reservations/available/<int:seats_count>/', reservation_views.ReservationAvailable.as_view()),
    path('reservations/today/', reservation_views.ReservationToday.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]

urlpatterns = format_suffix_patterns(urlpatterns)
