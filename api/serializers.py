from rest_framework import serializers
from api.models import Blog, Product
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator, MaxValueValidator, MaxLengthValidator, MinLengthValidator, EmailValidator
from  django.contrib.auth.models import User


# class UserSerializer(serializers.Serializer):
#     first_name = serializers.CharField(max_length=100)
#     last_name = serializers.CharField(max_length=100)
#     email = serializers.EmailField()

#     def create(self, validated_data):
#         return {"first_name": validated_data['first_name'],
#                 "last_name": validated_data['last_name'],
#                 "email": validated_data['email']}

#     def update(self, instance, validated_data):
#         instance['first_name'] = validated_data.get('first_name', instance['first_name'])
#         instance['last_name'] = validated_data.get('last_name', instance['last_name'])
#         instance['email'] = validated_data.get('email', instance['email'])
#         return instance
    
class ProductSerializer(serializers.ModelSerializer):
    # name = serializers.SerializerMethodField()
    # name = serializers.CharField(max_length=100, validators = [UniqueValidator(queryset=Product.objects.all())]) #field level validation
    # price = serializers.DecimalField(max_digits=10, decimal_places=2, validators =  [MinValueValidator(0.01), MaxValueValidator(5000000)])

    class Meta:
        model = Product
        fields = '__all__'  # or ['id', 'name', 'description', 'price', 'stock']

    # def get_name(self, obj):
    #     return obj.name.upper()
    
class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

# class ProductDetailSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = '__all__'
# #object level validation
#     def validate(self, data):
#         if data['price'] < 0:
#             raise serializers.ValidationError("PRICE MUST BE GREATER THAN 0")
#         return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            )
        
        #agar admin panel me password invallid ya plain text me dikha hash me na dikhe toh upr se password filed nikalke use the following:
        #  password=validated_data['password']
        # user.set_password(password)
        # user.save()
        return user
