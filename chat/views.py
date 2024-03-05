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


from django.db.models import Max

def filter_messages(request):
    user_chatrooms = Chat.objects.filter(user1=request.user) | Chat.objects.filter(user2=request.user)
    if not user_chatrooms.exists():
        return render(request, 'chat/message_detail.html')

    user_chatrooms = user_chatrooms.annotate(max_timestamp=Max('messages__timestamp'))

    user_chatrooms = user_chatrooms.order_by('-max_timestamp')

    latest_messages = {}
    for chatroom in user_chatrooms:
        latest_message = chatroom.messages.order_by('-timestamp').first()
        if latest_message:
            latest_messages[chatroom] = latest_message

    return render(request, 'chat/message_detail.html', {'latest_messages': latest_messages})



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

    messages = Message.objects.filter(chat=chat_room).order_by('timestamp')

    return render(request, 'chat/chatroom.html', {'room_name': room_name, 'messages': messages})



def all_active_users(request):
    all_active_lecturers=User.objects.filter(is_lecturer=True)
    all_active_students=User.objects.filter(is_student=True)
    context={
        'lecturers':all_active_lecturers,
        'students':all_active_students
    }
    return render(request,'chat/active_list.html',context)


