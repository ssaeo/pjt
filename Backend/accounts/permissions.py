from rest_framework.permissions import BasePermission

class IsAuthenticatedForAccounts(BasePermission):
    """
    accounts 앱에 대해서는 인증된 사용자만 접근 허용.
    다른 앱은 모든 사용자 허용.
    """
    def has_permission(self, request, view):
        if request.resolver_match.namespace == 'accounts':  # URL namespace 확인
            return request.user and request.user.is_authenticated
        return True  # 다른 앱은 모두 허용
