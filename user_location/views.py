from django.http import HttpResponse
from django.shortcuts import render
from .forms import EventForm
from user_location.forms import UserForm

from user_location.models import Event
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry


def index(request):
    events_list = Event.objects.all()[:3]
    if len(events_list) <= 0:
        events_list = ['test event 1', 'test event 2', 'test event 3']
    return render(request, "index.html", {'events': events_list})


def events(request):
    events_list = Event.objects.all()

    if not events_list:
        events_list = ['test event 1', 'test event 2', 'test event 3']

    return render(request, "events.html", {'events': events_list})


def profile(request):
    current_user = request.user
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            location_str = form.cleaned_data['location']
            lat, lon = map(float, location_str.split(', '))
            location = Point(lon, lat)

            location = GEOSGeometry(location.wkt)

            event = Event(
                user=current_user,
                event_name=form.cleaned_data['event_name'],
                event_date=form.cleaned_data['event_date'],
                location=location
            )
            event.save()

    else:
        form = EventForm()

    events_list = Event.objects.filter(user=current_user)

    if not events_list:
        events_list = ['test event 1', 'test event 2', 'test event 3']

    return render(request, "profile.html", {'events': events_list, 'form': form})


def edit_event(request):
    if request.method == "POST":

        event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        location_str = request.POST.get('location')

        if event_id is not None and event_name is not None and event_date is not None and location_str is not None:
            try:
                lat, lon = map(float, location_str.split(', '))
                location = Point(lon, lat)
                location = GEOSGeometry(location.wkt)

                event = Event.objects.get(id=event_id)
                event.event_name = event_name
                event.event_date = event_date
                event.location = location
                event.save()
            except ValueError:

                pass

    form = EventForm()

    events_list = Event.objects.filter(user=request.user)

    if not events_list:
        events_list = ['test event 1', 'test event 2', 'test event 3']

    return render(request, "profile.html", {'events': events_list, 'form': form})


def login(request):
    context = {"form": UserForm()}
    return render(request, "registration/login.html", context)
