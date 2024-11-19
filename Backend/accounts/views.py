from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer

User = get_user_model()

@api_view(['POST'])
def signup(request):
    """
    회원가입: 사용자 정보를 받아 새 계정을 생성.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    """
    로그인: 이메일과 비밀번호를 사용해 인증.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, username=email, password=password)
    if user:
        return Response({"message": "로그인 성공"}, status=status.HTTP_200_OK)
    return Response({"message": "로그인 실패"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request, username):
    """
    프로필 조회 및 수정
    - GET: 특정 사용자의 정보를 반환.
    - PUT: 특정 사용자의 정보를 업데이트.
    """
    user = get_object_or_404(User, username=username)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if request.user.username != username:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, username):
    """
    회원 탈퇴: 사용자 계정을 삭제.
    """
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
    user.delete()
    return Response({"message": "계정이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
