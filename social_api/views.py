from rest_framework import generics,permissions,viewsets,serializers,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from django.db.models import Q 
from .models import FriendRequest,CustomUser
from .serializers import UserSerializer,FriendRequestSerializer, UserCreateSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone  
from datetime import timedelta 
from rest_framework.views import APIView


User = get_user_model()

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email__iexact=email).first()
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    
    
    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response({"detail": "Keyword parameter is required."}, status=400)

        users = CustomUser.objects.filter(
            Q(email__icontains=keyword) | 
            Q(first_name__icontains=keyword) | 
            Q(last_name__icontains=keyword)
        )
        
        if not users.exists():
            return Response({"detail": "No users found matching the keyword."}, status=404)
        
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests = FriendRequest.objects.filter(from_user=self.request.user, timestamp__gte=one_minute_ago).count()
        if recent_requests >= 3:
            raise serializers.ValidationError("You have exceeded the limit of 3 friend requests per minute.")
        serializer.save(from_user=self.request.user)
        
    @action(detail=False,methods=['get'],url_path='sent')
    def sent_requests(self,request):
        requests = FriendRequest.objects.filter(from_user=request.user)
        serializer = self.get_serializer(requests,many=True)
        return Response(serializer.data)
    
    @action(detail=False,methods=['get'],url_path='received')
    def received_requests(self,request):
        requests=FriendRequest.objects.filter(to_user=request.user)
        serializer = self.get_serializer(requests,many=True)
        return Response(serializer.data)
    
    @action(detail=True,methods=['post'])
    def accept(self,request,pk=None):
        friend_request = self.get_object()
        if friend_request.to_user == request.user:
            friend_request.accepted = True
            friend_request.save()
        return Response({'status':'friend request accepted'})
    
    @action(detail=True,methods=['post'])
    def reject(self,request,pk=None):
        friend_request = self.get_object()
        if friend_request.to_user == request.user:
            friend_request.delete()
        return Response({'status':'friend request rejected'})
        
    @action(detail=False, methods=['get'], url_path='friends')
    def list_friends(self, request):
        friends = CustomUser.objects.filter(
            Q(sent_requests__to_user=request.user, sent_requests__accepted=True) |
            Q(received_requests__from_user=request.user, received_requests__accepted=True)
        ).distinct()
        page = self.paginate_queryset(friends)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(friends, many=True)
        return Response(serializer.data)
