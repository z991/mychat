import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from django.utils.safestring import mark_safe


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def test_send(request):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "chat_test_chat",
        {
            "type": "chat_message",
            'message': "用接口测试一下发送消息啦啦啦",
            'destination': "test_chat",
            'time': datetime.now().strftime(format("%Y-%m-%d %H:%M:%S"))
        }
    )
    pass
    return JsonResponse({"info": "成功"})

def test(request):
    return render(request, 'chat/test.html', {})
