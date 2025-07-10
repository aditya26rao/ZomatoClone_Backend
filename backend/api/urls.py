from django.urls import path
from .views import FoodItemListView, PlaceOrderView, register_user, get_categories,previous_orders
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

def welcome(request):
    return JsonResponse({"message": "Welcome to ZomatoClone API 👋"})
urlpatterns = [
    path('', welcome),  # Handles base path of this app
    path('api/foods/', FoodItemListView.as_view(), name='food-list'),  # ✅ Changed from 'food/' to 'foods/'
    path('api/orders/', PlaceOrderView.as_view(), name='place-order'),
    path('api/categories/', get_categories, name='get_categories'),
 path('api/previous-orders/',previous_orders, name='previous-orders'),

    # JWT Token
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Register
    path('api/register/', register_user, name='register'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
