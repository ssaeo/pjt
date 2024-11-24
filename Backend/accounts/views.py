from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

User = get_user_model()

@api_view(['POST'])
def signup(request):
    """
    회원가입: 사용자 정보를 받아 새 계정을 생성
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        # 토큰 생성
        token = Token.objects.create(user=user)
        return Response({
            'message': '회원가입이 완료되었습니다.',
            'token': token.key
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user:
        token, created = Token.objects.get_or_create(user=user)
        # UserSerializer를 사용하여 사용자 정보 직렬화
        serializer = UserSerializer(user, context={'request': request})
        return Response({
            'token': token.key,
            'user': serializer.data
        })
    else:
        return Response(
            {'error': '잘못된 사용자 이름 또는 비밀번호입니다.'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    로그아웃: 사용자의 토큰을 삭제
    """
    request.user.auth_token.delete()
    return Response({'message': '로그아웃 되었습니다.'}, status=status.HTTP_200_OK)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    user = get_object_or_404(User, username=username)
    
    if request.method in ['PUT', 'DELETE'] and request.user.username != username:
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
            
    elif request.method == 'DELETE':
        user.delete()
        return Response({"message": "계정이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)