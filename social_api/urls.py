from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet,FriendRequestViewSet,SignUpView,CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'friend-requests',FriendRequestViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/',TokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),
]