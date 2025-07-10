from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, filters
from .models import FoodItem, Order, Category
from .serializers import FoodItemSerializer, OrderSerializer, CategorySerializer

# ✅ List All Food Items (GET /api/foods/)
@permission_classes([AllowAny])
class FoodItemListView(generics.ListAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description', 'category']  # 🔍 fields you want to search in


# ✅ Place a New Order (POST /api/orders/)  :- for fetch token 30min
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except ValidationError as ve:
            return Response({'error': ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the error e as needed
            return Response({'error': 'Internal Server Error: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=201)


# ✅ Register a New User (POST /api/register/)
@api_view(['POST'])
@permission_classes([AllowAny])  # 👈 Public endpoint
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name', '')

    if not username or not email or not password:
        return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
    user.save()

    return Response({'message': '✅ User registered successfully!'}, status=status.HTTP_201_CREATED)


# ✅ Get All Categories (GET /api/categories/) → Public, No Authentication Needed
@api_view(['GET'])
@permission_classes([AllowAny])  # 👈 Fix: Public access
def get_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_foods(request):
    category_name = request.GET.get('category')
    
    if category_name and category_name != 'All':
        foods = FoodItem.objects.filter(category__name=category_name)
    else:
        foods = FoodItem.objects.all()
        
    serializer = FoodItemSerializer(foods, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Order
from .serializers import OrderDisplaySerializer  # ✅ Use the right serializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def previous_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    serializer = OrderDisplaySerializer(orders, many=True)  # ✅ Fixed here
    return Response(serializer.data)

