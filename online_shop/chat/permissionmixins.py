from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class IsChatOwnerOrOperator(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if 'Operators' in request.user.groups.all().values_list('name', flat=True) or kwargs['room_name'] == \
                request.user.phone:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied('Permission denied')
