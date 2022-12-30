
from django.shortcuts import render,redirect
from coLearn.models import CoLearnUser
from chat.models import Chat,ChatMessage
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    users= CoLearnUser.objects.all().exclude(user_id=request.user.id)


    return render(request, "chat/index.html",{"users":users})

@login_required
def room(request,room_name):
    
    
    users=CoLearnUser.objects.all().exclude(pk=request.user.id)
    room=Chat.objects.get(id=room_name)
    # all_rooms=Chat.objects.all()
    # for oda in all_rooms:
    #     if oda==room_name:
    #         room=oda
    #room=Chat.objects.get(chat_id=room_name)
    messages=ChatMessage.objects.filter(chat_id=room)

    # if request.user != room.first_user:
    #     if request.user!=room.second_user:
    #         return redirect("index")

    return render(request,"chat/room2.html",{'room_name': room_name,
                                               "room":room,
                                               "users":users,
                                               'messages':messages})
@login_required
def start_chat(request, user_name):

    first_user=CoLearnUser.objects.get(pk=request.user.id)
    second_user = CoLearnUser.objects.filter(user__username=user_name).first()
    # users= CoLearnUser.objects.all().exclude(id=request.user.id)
    # for i in users:
    #     if str(i.user)==user_name:
    #         user_id=i.id
    # second_user=CoLearnUser.objects.get(pk=user_id)

    # _,roomx = Chat.objects.get_or_create(first_user=first_user, second_user=second_user)

    try:
        roomx=Chat.objects.get(first_user=first_user, second_user=second_user)
        
    except:
        try:
            roomx=Chat.objects.get(first_user=second_user, second_user=first_user)
            
        except:
            roomx=Chat.objects.create(first_user=first_user, second_user=second_user)
                      
    #return HttpResponseRedirect(reverse('room', kwargs={'room_name': room}))
    # #return redirect("index")
    return redirect("room",room_name=roomx.id)
    #return redirect("rooms",room.id)
    # #return render(request, "chat/index2.html",{"users":users})
    # #return render(request, "chat/room.html",{"room_name": room_name})