# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index(request):
    return render(request, "chat/index.html")


@login_required
def room(request, room_name):
    phone_number = request.user.phone_number  # Assuming you are using Django's built-in authentication
    avatar = request.user.avatar.file.url
    print("skldfjslkfjsdlkjklsdjflksdjflsdfjl")
    print(avatar)
    return render(request, "chat/room.html", {"room_name": room_name, "phone_number": phone_number})



#from rest_framework.decorators import api_view, permission_classes
#from rest_framework.permissions import IsAuthenticated
#from rest_framework.response import Response
#
#
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def index(request):
#    return Response({"message": "Welcome to the chat API"})
#
#
#@api_view(['GET'])
#@permission_classes([IsAuthenticated])
#def room(request, room_name):
#    user = request.user
#    phone_number = getattr(user, 'phone_number', None)
#    avatar = getattr(user, 'avatar', None)
#
#    avatar_url = avatar.file.url if avatar and hasattr(avatar, 'file') else None
#
#    return Response({
#        "room_name": room_name,
#        "phone_number": phone_number,
#        "avatar": avatar_url
#    })
