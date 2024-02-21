from django.shortcuts import render
# from django.contrib.auth.models import User
from accounts.models import User
from .models import Chat,Message
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from .models import Chat, Message
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()
def generate_room_name(name1, name2):
    return str(name1 + name2)




def filter_messages(request):
    chat_user1 = Chat.objects.filter(user1=request.user).first()
    chat_user2 = Chat.objects.filter(user2=request.user).first()

    if chat_user1 is None and chat_user2 is None:
        # Handle the case where no chat room is found for the user
        return render(request, 'chat/message_list.html')

    get_room = None
    if chat_user1 is not None and chat_user2 is not None:
        # If the user has two chat rooms, choose one
        get_room = chat_user1 if chat_user1 == chat_user2 else chat_user1
    elif chat_user1 is not None:
        get_room = chat_user1
    else:
        get_room = chat_user2

    get_message = Message.objects.filter(chat=get_room).order_by('-id')
    return render(request, 'chat/message_list.html', {'messages': get_message})



def home(request, username):
    try:
        get_user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User not found", status=404)

    existing_chat = Chat.objects.filter(user1=request.user, user2=get_user) | Chat.objects.filter(user1=get_user, user2=request.user)
    
    if existing_chat.exists():
        chat_room = existing_chat.first()
        room_name = chat_room.room_name
    else:
        room_name = generate_room_name(request.user.username, username)
        chat_room = Chat.objects.create(user1=request.user, user2=get_user, room_name=room_name)

    # Fetch existing messages for the chat room
    messages = Message.objects.filter(chat=chat_room).order_by('timestamp')

    return render(request, 'chat/chatroom.html', {'room_name': room_name, 'messages': messages})



def all_active_users(request):
    all_active_lecturers=User.objects.filter(is_lecturer=True)
    context={
        'lecturers':all_active_lecturers,
    }
    return render(request,'chat/active_list.html',context)


