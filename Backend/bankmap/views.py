from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import BankBranch
from .serializers import BankBranchSerializer
import logging
import math

logger = logging.getLogger(__name__)

class BankBranchViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = BankBranch.objects.all()
    serializer_class = BankBranchSerializer

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        # 1. 파라미터 검증
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', '1000')
        bank_code = request.query_params.get('bank_code')

        logger.debug(f"Received params: lat={lat}, lng={lng}, radius={radius}, bank_code={bank_code}")

        if not all([lat, lng]):
            return Response(
                {"error": "위도와 경도는 필수 파라미터입니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. 데이터 타입 변환
        lat = float(lat)
        lng = float(lng)
        radius = float(radius)

        # 3. 간단한 범위 검색
        lat_range = radius / 111000  # 약 111km = 1도
        lng_range = radius / (111000 * abs(math.cos(math.radians(lat))))

        query = Q(
            latitude__gte=lat - lat_range,
            latitude__lte=lat + lat_range,
            longitude__gte=lng - lng_range,
            longitude__lte=lng + lng_range
        )

        if bank_code:
            query &= Q(bank_code=bank_code)

        # 4. 쿼리 실행
        branches = BankBranch.objects.filter(query)[:50]  # 최대 50개로 제한
        
        logger.debug(f"Query: {query}")
        logger.debug(f"Found {branches.count()} branches")

        # 5. 시리얼라이즈 및 응답
        serializer = self.serializer_class(branches, many=True)
        
        return Response({
            "count": len(serializer.data),
            "results": serializer.data
        })