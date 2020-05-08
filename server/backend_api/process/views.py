from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import string
import random
from process.models import User


def home(request):
    newusername = request.POST.get('username', False)
    newpassword = request.POST.get('password', False)
    for user in User.objects.all():
        if user.username == newusername and user.password == newpassword:
            return redirect(request, 'load_file.html')
    return render(request, 'pages/home.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'pages/register.html')
    elif request.method == 'POST':
        newusername = request.POST.get('username', False)
        newpassword = request.POST.get('password', False)
        newUser = User.objects.create(username=newusername, password=newpassword)
        return render(request, 'pages/home.html')


def index(request):
    """
    Strona umożlwiająca upload pliku
    """

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        random_identifier = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        return render(request, 'load_file.html', {
            'uploaded_file_url': uploaded_file_url,
            'calculation_id': random_identifier
        })
    return render(request, 'load_file.html')


def track_progress(request, calculation_name):
    """Strona na której można śledzić postęp obliczeń

    Arguments:
        calculation_name {string} -- nazwa kanału komunikacyjnego
    """

    return render(request, 'progress_tracker.html', {
        'calculation_name': calculation_name
    })


def websocket_sending_message_demo(request, calculation_name, message):
    """Demonstracja wykorzystania websocketów do rozgłaszania statusu obliczeń

    Arguments:
        calculation_name {string} -- nazwa kanału komunikacyjnego
        message {string} -- wiadomość do rozgłoszenia
    """

    # pobranie instancji kanału komunikacyjnego
    channel_layer = get_channel_layer()
    # wygenerowanie nazwy kanału
    tracker_group_name = 'tracker_%s' % calculation_name

    # wysłanie wiadomości do nasłuchujących użytkowników
    async_to_sync(channel_layer.group_send)(
        tracker_group_name,
        {
            'type': 'progress_update', 'message': message
        }
    )

    return HttpResponse("OK")
