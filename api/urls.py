from django.urls import path
from .views import BlogList, ProductList, BlogCreate, create_product, get_product, get_product_by_id, update_product, delete_product, partial_update_product,\
    BlogList, BlogDetail, BlogUpdate, BlogDelete, BlogListCreateView, BlogRetrieveUpdateDestroyView, \
    RegisterView, LoginView, LogoutView, NewRegisterView
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router  = routers.DefaultRouter()
router.register('products', views.ProductViewSet )

urlpatterns = [   
    #authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #class based views
    path('products/', ProductList.as_view(), name='product_list'),
    path('blogs/', BlogList.as_view(), name='blog_list'),
    path('blogs_create/', BlogCreate.as_view(), name='blog_create'),
    path('blogs_detail/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path('blogs_update/<int:pk>/', BlogUpdate.as_view(), name='blog_update'),
    path('blogs_delete/<int:pk>/', BlogDelete.as_view(), name='blog_delete'),
    path('blogs_newcreate/', BlogListCreateView.as_view(), name='blog_list_create'),
    path('blogs_newcreate/<int:pk>/', BlogRetrieveUpdateDestroyView.as_view(), name='blog_retrieve_update_delete'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain'),
    path('refresh_token/', TokenRefreshView.as_view(), name='token-refresh'),
    path('newregister/', NewRegisterView.as_view(), name='newregister'),


    #function based views
    path('create_product/', create_product, name='create_product'),
    path('get_product/', get_product, name='get_product'),
    path('get_product/<int:id>/', get_product_by_id, name='get_product_by_id'),
    path('update_product/<int:id>/', update_product, name='update_product'),
    path('delete_product/<int:id>/', delete_product, name='delete_product'),
    path('update/<int:id>/', partial_update_product, name='partial_update_product'),
] + router.urls
