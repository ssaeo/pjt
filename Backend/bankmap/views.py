from rest_framework import viewsets
from .models import BankBranch
from .serializers import BankBranchSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
import logging
import math  # math 모듈 가져오기
from .utils import FinMapAPI  # FinMapAPI 가져오기

logger = logging.getLogger(__name__)

class BankBranchViewSet(viewsets.ModelViewSet):
    queryset = BankBranch.objects.all()
    serializer_class = BankBranchSerializer

    @action(detail=False, methods=['get'])
    def nearby(self, request):
        try:
            lat = float(request.query_params.get('lat'))
            lng = float(request.query_params.get('lng'))
            radius = float(request.query_params.get('radius', 1000))

            # 요청 데이터 로깅
            logger.info(f"Nearby search request: lat={lat}, lng={lng}, radius={radius}")

            # FinMapAPI를 통해 실제 은행 지점 데이터 조회
            branches = FinMapAPI.search_branches(
                lat - radius / 111000,
                lng - radius / (111000 * math.cos(math.radians(lat))),
                lat + radius / 111000,
                lng + radius / (111000 * math.cos(math.radians(lat)))
            )

            # 검색 결과가 없을 경우
            if not branches:
                return Response({"error": "검색 결과가 없습니다."}, status=404)

            # 응답 데이터 가공
            formatted_branches = [
                {
                    "name": branch.get("brch_name"),
                    "address": branch.get("addr"),
                    "latitude": branch.get("latitude"),
                    "longitude": branch.get("longitude"),
                    "phone": branch.get("brch_telno", "정보 없음"),
                }
                for branch in branches
            ]
            return Response(formatted_branches)

        except Exception as e:
            logger.error(f"Error in nearby branches search: {str(e)}")
            return Response(
                {"error": "서버 오류가 발생했습니다."}, 
                status=500
            )
