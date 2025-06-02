from urllib import response
from django.shortcuts import render
from .serializers import ProductSerializer, BlogSerializer, RegisterSerializer
from .models import Product, Blog
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes  #for function based Permissions
from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework import permissions #for class based Permissions
from rest_framework.authtoken.models import Token #for token based authentication
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User

# Create your views here.
class ProductList(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
# class BlogCreate(APIView):
#     def post(self, request):
#         serializer = BlogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])  #for function based Permissions
def create_product(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_product(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_product_by_id(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_product(request, id):
    if request.method == 'PUT':
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_product(request, id):
    if request.method == 'DELETE':
        product = Product.objects.get(id=id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def partial_update_product(request, id):
    if request.method == 'PATCH':
        product = Product.objects.get(id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#generics api
class BlogList(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer
    permission_classes = [permissions.AllowAny] # this is for class based permissions

class BlogCreate(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer
    permission_classes = [permissions.AllowAny]

class BlogDetail(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer
    permission_classes = [permissions.IsAuthenticated]


class BlogUpdate(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer

class BlogDelete(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer

class BlogListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer

class BlogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer
    permission_classes = [permissions.AllowAny]

class BlogView(generics.GenericAPIView):
    queryset = Blog.objects.all()
    serializer_class =  BlogSerializer

    def get(self, obj):
        pass

    def post(self, obj):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass

#mixins
# class ProductListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset =Product.objects.all()
#     serializer_class =  ProductSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(self, request, *args, **kwargs)
    
# class ProductCreateView(mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset =Product.objects.all()
#     serializer_class =  ProductSerializer

#     def post(self, request, *args, **kwargs):
#         return self.create(self, request, *args, **kwargs)
    
# class ProductRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset =Product.objects.all()
#     serializer_class =  ProductSerializer

#     def get(self, request, *args, **kwargs, pk=None):
#         return self.retrieve(self, request, *args, **kwargs, pk=None)
    
# class ProductUpdateView(mixins.UpdateModelMixin, generics.GenericAPIView):
#     queryset =Product.objects.all()
#     serializer_class =  ProductSerializer

#     def put(self, request, *args, **kwargs, pk=None):
#         return self.update(self, request, *args, **kwargs, pk=None)

# class ProductDestroyView(mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset =Product.objects.all()
#     serializer_class =  ProductSerializer

#     def delete(self, request, *args, **kwargs, pk=None):
#         return self.destroy(self, request, *args, **kwargs, pk=None)
    
#viewset
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#register view
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token':token.key,
                    'username' : user.username,
                    'email' : user.email
                }, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#login view
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token':token.key
                }, status=status.HTTP_200_OK
            )
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    

#logout
class LogoutView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # request.user.auth_token.delete() or use :
        logout(request)
        return Response({"message":"Logged Out Successfully !!!"})
    
class NewRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer