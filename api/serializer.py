from rest_framework import serializers
from .models import Category , Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        Product_count = serializers.SerializerMethodField(method_name='count_total')
        def count_total(self , obj):
            return obj.products.count()
        model = Category
        fields = '__all__' 

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name'  , read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

    def validate_price(self, value):
        if value < 0:
            return serializers.ValidationError("Price must be larger than 0.")
        return value

    def validate(self, attrs):
        stock = attrs.get('stock', getattr(self.instance, 'stock', None))
        is_available = attrs.get('is_available', getattr(self.instance, 'is_available', True))
        
        if stock == 0 and is_available:
            raise serializers.ValidationError(
            {"is_available": "A product with 0 stock cannot be available."}
        )
        return attrs
        
    

    