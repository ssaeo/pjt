import requests
from datetime import datetime, timedelta
from .models import FinMapToken
import logging

logger = logging.getLogger(__name__)

class FinMapAPI:
    BASE_URL = 'https://testfinmapapi.kftc.or.kr'
    CLIENT_ID = 'c7ba1ffd-a5f6-4abc-a00f-ddd8c7643b54'
    CLIENT_SECRET = '6d50fe26-0fc2-4425-9eb4-49dd5bd767b0'

    @classmethod
    def get_token(cls):
        token = FinMapToken.objects.order_by('-created_at').first()
        
        if not token or token.created_at + timedelta(seconds=token.expires_in) < datetime.now():
            response = requests.post(
                f'{cls.BASE_URL}/oauth/2.0/token',
                data={
                    'client_id': cls.CLIENT_ID,
                    'client_secret': cls.CLIENT_SECRET,
                    'scope': 'finmap',
                    'grant_type': 'client_credentials'
                }
            )
            data = response.json()
            token = FinMapToken.objects.create(
                access_token=data['access_token'],
                token_type=data['token_type'],
                expires_in=int(data['expires_in']),
                scope=data['scope']
            )
        
        return token.access_token

    @classmethod
    def search_branches(cls, lat1, lng1, lat2, lng2):
        """
        주어진 영역 내의 은행 지점을 검색
        """
        token = cls.get_token()
        try:
            response = requests.post(
                f'{cls.BASE_URL}/v1.0/inquiry/brch_lists',
                headers={'Authorization': f'Bearer {token}'},
                json={
                    'start_latitude': str(lat1),
                    'start_longitude': str(lng1),
                    'end_latitude': str(lat2),
                    'end_longitude': str(lng2),
                    'brch_srch_yn': 'Y',
                    'brch_cond': {
                        'open_yn': 'N',
                        'ptsh_icld_yn': 'Y',
                        'org_code_srch_yn': 'Y',
                        'org_code_srch': ['004', '011', '020', '081']
                    }
                }
            )
            return response.json().get('data', [])
        except Exception as e:
            logger.error(f"Error in FinMapAPI search_branches: {str(e)}")
            return []