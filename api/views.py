import secrets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from drf_spectacular.utils import extend_schema

from .models import Member, AuthToken, Message
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    MemberSerializer,
    MessageSerializer,
    ProfileUpdateSerializer
)
from .authentication import TokenAuthentication
from .permissions import IsAuthenticated


class RegisterView(APIView):
    """User registration endpoint"""
    authentication_classes = []
    permission_classes = []
    
    @extend_schema(
        request=RegisterSerializer,
        responses={201: MemberSerializer}
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                member = serializer.save()
                token = AuthToken.objects.create(
                    key=secrets.token_hex(20),
                    member=member
                )
                return Response({
                    'token': token.key,
                    'user': MemberSerializer(member).data
                }, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'error': 'Username already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """User login endpoint"""
    authentication_classes = []
    permission_classes = []
    
    @extend_schema(
        request=LoginSerializer,
        responses={200: MemberSerializer}
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            try:
                member = Member.objects.get(username=username)
                if member.check_password(password):
                    # Delete old tokens and create new one
                    AuthToken.objects.filter(member=member).delete()
                    token = AuthToken.objects.create(
                        key=secrets.token_hex(20),
                        member=member
                    )
                    return Response({
                        'token': token.key,
                        'user': MemberSerializer(member).data
                    })
                else:
                    return Response(
                        {'error': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Member.DoesNotExist:
                return Response(
                    {'error': 'Invalid credentials'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """User logout endpoint"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: dict}
    )
    def post(self, request):
        # Delete user's token
        AuthToken.objects.filter(member=request.user).delete()
        return Response({'message': 'Successfully logged out'})


class ProfileView(APIView):
    """User profile endpoint"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: MemberSerializer}
    )
    def get(self, request):
        serializer = MemberSerializer(request.user)
        return Response(serializer.data)
    
    @extend_schema(
        request=ProfileUpdateSerializer,
        responses={200: MemberSerializer}
    )
    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(MemberSerializer(request.user).data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MessagesView(APIView):
    """Messages endpoint for listing and creating messages"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: MessageSerializer(many=True)}
    )
    def get(self, request):
        limit = int(request.GET.get('limit', 50))
        offset = int(request.GET.get('offset', 0))
        
        if limit > 100:
            limit = 100
        
        messages = Message.objects.all()[offset:offset + limit]
        count = Message.objects.count()
        
        serializer = MessageSerializer(messages, many=True)
        return Response({
            'count': count,
            'results': serializer.data
        })
    
    @extend_schema(
        request=MessageSerializer,
        responses={201: MessageSerializer}
    )
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(author=request.user)
            return Response(
                MessageSerializer(message).data,
                status=status.HTTP_201_CREATED
            )
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
