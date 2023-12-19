from django.http import HttpResponse
from django.shortcuts import render
from .forms import EventForm
from user_location.forms import UserForm
from . import app_settings
from user_location.models import Event, Counties
from django.contrib.gis.geos import Point
from django.contrib.gis.geos import GEOSGeometry
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import requests
from geopy.geocoders import Nominatim
from django.http import JsonResponse
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

geolocator = Nominatim(user_agent="location")


def index(request):
    events_list = Event.objects.all()[:3]
    if len(events_list) <= 0:
        events_list = ['test event 1', 'test event 2', 'test event 3']

    return render(request, "index.html", {'events': events_list})


def update_going(request):
    if request.method == 'POST' and request.user.is_authenticated:
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        if 'going' in request.POST:
            if request.user in event.going_users.all():
                event.going_users.remove(request.user)
            else:
                event.going_users.add(request.user)

        count_users_going_to_event = event.going_users.count()

        return JsonResponse({'going_count': count_users_going_to_event})


def events(request, slug=None):
    if slug:
        events_list = Event.objects.filter(address__icontains=slug)

        api_url = f'https://failteireland.azure-api.net/opendata-api/v1/activities?subscription-key=&search=*&$filter=address/addressRegion eq \'{slug}\''

        try:
            # Make a GET request to the API
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                activities = response.json()
            else:
                # Handle the error if the request was not successful
                print(f"Error fetching activities. Status code: {response.status_code}")
                activities = []
        except Exception as e:
            # Handle exceptions, such as network errors
            print(f"Error fetching activities: {e}")
            activities = []

        if not events_list:
            events_list = []

        for event in events_list:
            # Check if the user is going to this event (based on session)
            if request.user.is_authenticated:
                event.is_user_going = request.user in event.going_users.all()
            else:
                event.is_user_going = False

        return render(request, "events.html", {'events': events_list, 'activities': activities, 'county': slug})

    counties_list = Counties.objects.all()

    county_data = []
    for county in counties_list:
        if county.geom:
            county_geojson = GEOSGeometry(county.geom).json
            county_data.append({
                'name': county.name_tag,
                'geometry': county_geojson,
            })

    return render(request, "counties.html", {'counties': counties_list, 'county_data': county_data})


def profile(request):
    current_user = request.user
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            geocoded_location = geolocator.geocode(form.cleaned_data['location'])

            if geocoded_location:
                point = Point(geocoded_location.longitude, geocoded_location.latitude)

                event = Event(
                    user=current_user,
                    event_name=form.cleaned_data['event_name'],
                    event_date=form.cleaned_data['event_date'],
                    address=form.cleaned_data['location'],
                    location=point
                )
                event.save()
            else:
                form = EventForm()
                print("geocoding failed")

    else:
        form = EventForm()

    events_list = Event.objects.filter(user=current_user)

    if not events_list:
        events_list = []

    return render(request, "profile.html", {'events': events_list, 'form': form})


def location_geocode(request):
    lat = request.GET.get('lat', '')
    lng = request.GET.get('lng', '')

    res = {"success": 0, "address": ""}

    try:
        if lat != '' and lng != '':
            reverse_geocoded_address = geolocator.reverse((lat, lng), language='en')
            res = {"success": 1, "address": reverse_geocoded_address.address}
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        error_message = f"Geocoding error: {str(e)}"
        res = {"success": 0, "error": error_message}

    return JsonResponse({'locations': res})


def edit_event(request):
    if request.method == "POST":

        event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        location_str = request.POST.get('location')

        print(event_id, location_str, event_id is not None, event_name is not None, event_date is not None,
              location_str != "")

        if event_id is not None and event_name is not None and event_date is not None and location_str != "":
            try:
                geocoded_val = geolocator.geocode(location_str)

                if geocoded_val:
                    point = Point(geocoded_val.latitude, geocoded_val.longitude)

                    event, created = Event.objects.get_or_create(id=event_id)
                    event.event_name = event_name
                    event.event_date = event_date
                    event.address = location_str
                    event.location = point
                    event.save()
            except ValueError as e:
                error_message = f"edit error: {str(e)}"
                print(error_message)
                pass
        elif event_id is not None and event_name is not None and event_date is not None:
            try:
                event, created = Event.objects.get_or_create(id=event_id)
                event.event_name = event_name
                event.event_date = event_date
                event.save()
            except ValueError as e:
                error_message = f"edit error: {str(e)}"
                print(error_message)
                pass

    form = EventForm()

    events_list = Event.objects.filter(user=request.user)

    if not events_list:
        events_list = ['test event 1', 'test event 2', 'test event 3']

    return render(request, "profile.html", {'events': events_list, 'form': form})


def login(request):
    context = {"form": UserForm()}
    return render(request, "registration/login.html", context)


def offline(request):
    return render(request, "offline.html")


def manifest(request):
    return render(
        request,
        "manifest.json",
        {
            setting_name: getattr(app_settings, setting_name)
            for setting_name in dir(app_settings)
            if setting_name.startswith("PWA_")
        },
        content_type="application/json",
    )


def service_worker(request):
    response = HttpResponse(
        open(app_settings.PWA_SERVICE_WORKER_PATH).read(), content_type="application/javascript"
    )
    return response
