
# from rest_framework import serializers
# from .models import FoodItem, Order, OrderItem, Category

# # ✅ Food Item Serializer for Display
# class FoodItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FoodItem
#         fields = ['id', 'name', 'price', 'image']


# # ✅ Order Item Serializer for Display (Nested FoodItem)
# class OrderItemDisplaySerializer(serializers.ModelSerializer):
#     food_item = FoodItemSerializer(read_only=True)

#     class Meta:
#         model = OrderItem
#         fields = ['id', 'food_item', 'quantity']


# # ✅ Order Serializer for Display (GET previous orders endpoint)
# class OrderDisplaySerializer(serializers.ModelSerializer):
#     items = OrderItemDisplaySerializer(many=True, read_only=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'created_at', 'subtotal', 'delivery_fee', 'total', 'items']


# # ✅ Category Serializer
# from rest_framework import serializers
# from .models import Category

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'image']


# # ✅ Order Item Serializer for Creating Orders
# class OrderItemCreateSerializer(serializers.ModelSerializer):
#     food_item = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all())

#     class Meta:
#         model = OrderItem
#         fields = ['food_item', 'quantity']


# # ✅ Order Serializer for Creating Orders
# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemCreateSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = [
#             'id', 'first_name', 'last_name', 'email', 'street', 'city',
#             'state', 'zip_code', 'country', 'phone', 'subtotal', 'delivery_fee',
#             'total', 'items'
#         ]
#         read_only_fields = ['id']

#     def validate_items(self, value):
#         if not value:
#             raise serializers.ValidationError("Order must have at least one item.")
#         for item in value:
#             if not item.get('food_item') or not item.get('quantity'):
#                 raise serializers.ValidationError("Each item must have 'food_item' and 'quantity'.")
#             if item['quantity'] <= 0:
#                 raise serializers.ValidationError("Quantity must be greater than zero.")
#         return value

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         request = self.context.get('request')

#         if not request or not request.user or not request.user.is_authenticated:
#             raise serializers.ValidationError("User must be authenticated to place an order.")

#         order = Order.objects.create(user=request.user, **validated_data)

#         for item in items_data:
#             OrderItem.objects.create(
#                 order=order,
#                 food_item=item['food_item'],
#                 quantity=item['quantity']
#             )

#         return order



from rest_framework import serializers
from .models import FoodItem, Order, OrderItem, Category


# ✅ Category Serializer (for nested use)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


# ✅ Food Item Serializer (with category shown as name)
# class FoodItemSerializer(serializers.ModelSerializer):
#     category = serializers.StringRelatedField()  # or use CategorySerializer() for full detail

#     class Meta:
#         model = FoodItem
#         fields = ['id', 'name', 'price', 'image', 'description', 'category']

class FoodItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'price', 'image', 'description', 'category']


# ✅ Order Item Serializer for Display
class OrderItemDisplaySerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'quantity']


# ✅ Order Serializer for Display (GET previous orders)
class OrderDisplaySerializer(serializers.ModelSerializer):
    items = OrderItemDisplaySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'subtotal', 'delivery_fee', 'total', 'items']


# ✅ Order Item Serializer for Creating Orders (POST orders)
class OrderItemCreateSerializer(serializers.ModelSerializer):
    food_item = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all())  # expects FoodItem id

    class Meta:
        model = OrderItem
        fields = ['food_item', 'quantity']


# ✅ Order Serializer for Creating Orders (POST orders)
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id', 'first_name', 'last_name', 'email', 'street', 'city',
            'state', 'zip_code', 'country', 'phone', 'subtotal', 'delivery_fee',
            'total', 'items'
        ]
        read_only_fields = ['id']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("Order must have at least one item.")
        for item in value:
            if not item.get('food_item') or not item.get('quantity'):
                raise serializers.ValidationError("Each item must have 'food_item' and 'quantity'.")
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        request = self.context.get('request')

        if not request or not request.user or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated to place an order.")

        order = Order.objects.create(user=request.user, **validated_data)

        for item in items_data:
            OrderItem.objects.create(
                order=order,
                food_item=item['food_item'],
                quantity=item['quantity']
            )

        return order
