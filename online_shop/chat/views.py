from django.shortcuts import render
from django.views.generic import TemplateView

from chat.permissionmixins import IsChatOwnerOrOperator


def index(request):
    return render(request, 'chat/index.html', {})


# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name': room_name
#     })

class Room(IsChatOwnerOrOperator, TemplateView):
    template_name = 'chat/room.html'

    def get_context_data(self, **kwargs):
        context = super(Room, self).get_context_data(**kwargs)
        context['room_name'] = self.kwargs['room_name']
        return context

    # def get(self, request, room_name):
    #     return render(request, 'chat/room.html', {
    #         'room_name': room_name
    #     })

