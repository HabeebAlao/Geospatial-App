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
from django.views.decorators.cache import cache_page
from django.core.cache import cache

# Initialize geolocator with a user_agent
geolocator = Nominatim(user_agent="location")


def index(request):
    # Retrieve the latest 3 events or use default test events if none exist
    events_list = Event.objects.all()[:3]
    if len(events_list) <= 0:
        events_list = ['test event 1', 'test event 2', 'test event 3']

    # Render the index.html template with the events list
    return render(request, "index.html", {'events': events_list})


# Define the update_going view function
def update_going(request):
    # Handle POST requests when the user is authenticated
    if request.method == 'POST' and request.user.is_authenticated:
        event_id = request.POST.get('event_id')
        event = get_object_or_404(Event, pk=event_id)

        # Update the list of users going to the event and return the count
        if 'going' in request.POST:
            if request.user in event.going_users.all():
                event.going_users.remove(request.user)
            else:
                event.going_users.add(request.user)

        count_users_going_to_event = event.going_users.count()

        # Return the count in JSON format
        return JsonResponse({'going_count': count_users_going_to_event})


# Define the events view function
def events(request, slug=None):
    if slug:
        # Try to get activities from cache
        activities = cache.get(f'activities_{slug}')

        if activities is None:
            # If not in cache, perform the API call
            api_url = f'https://failteireland.azure-api.net/opendata-api/v1/activities?subscription-key=&search=*&$filter=address/addressRegion eq \'{slug}\''

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    activities = response.json()
                    # Cache activities for 1 hour (adjust as needed)
                    cache.set(f'activities_{slug}', activities, 3600)
                else:
                    print(f"Error fetching activities. Status code: {response.status_code}")
                    activities = []
            except Exception as e:
                print(f"Error fetching activities: {e}")
                activities = []

        # Filter events based on the provided slug (address)
        events_list = Event.objects.filter(address__icontains=slug)

        # Set events_list to an empty list if it's None
        if not events_list:
            events_list = []

        # Check if the user is going to each event and add a flag
        for event in events_list:
            if request.user.is_authenticated:
                event.is_user_going = request.user in event.going_users.all()
            else:
                event.is_user_going = False

        # Render the events.html template with events, activities, and county information
        return render(request, "events.html", {'events': events_list, 'activities': activities, 'county': slug})

    # If no slug is provided, retrieve and render a list of counties
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


# Define the profile view function
def profile(request):
    # Handle POST requests to add a new event
    current_user = request.user
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            # Geocode the location and create a new event if successful
            geocoded_location = geolocator.geocode(form.cleaned_data['location'])
            if geocoded_location:
                point = Point(geocoded_location.longitude, geocoded_location.latitude)
                print(point)
                event = Event(
                    user=current_user,
                    event_name=form.cleaned_data['event_name'],
                    event_date=form.cleaned_data['event_date'],
                    address=form.cleaned_data['location'],
                    location=point
                )
                event.save()
                print("created event")
            else:
                form = EventForm()
                print("geocoding failed")

    else:
        form = EventForm()

    # Retrieve and render events associated with the current user
    events_list = Event.objects.filter(user=current_user)

    if not events_list:
        events_list = []

    return render(request, "profile.html", {'events': events_list, 'form': form})


# Define the location_geocode view function
def location_geocode(request):
    # Handle AJAX requests to geocode a location based on latitude and longitude
    lat = request.GET.get('lat', '')
    lng = request.GET.get('lng', '')
    res = {"success": 0, "address": ""}

    try:
        if lat != '' and lng != '':
            # Reverse geocode the provided latitude and longitude
            reverse_geocoded_address = geolocator.reverse((lat, lng), language='en')
            res = {"success": 1, "address": reverse_geocoded_address.address}
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        # Handle geocoding errors
        error_message = f"Geocoding error: {str(e)}"
        res = {"success": 0, "error": error_message}

    return JsonResponse({'locations': res})


# Define the edit_event view function
def edit_event(request):
    if request.method == "POST":
        # Handle editing of events based on POST data
        event_id = request.POST.get('event_id')
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        location_str = request.POST.get('location')

        print(event_id, event_name, event_date, location_str)

        # Check if necessary data is present before attempting to edit
        if event_id is not None and event_name is not None and event_date is not None and location_str != "":
            try:
                # Geocode the new location and update event details
                geocoded_val = geolocator.geocode(location_str)

                if geocoded_val:
                    point = Point(geocoded_val.longitude, geocoded_val.latitude)

                    event, created = Event.objects.get_or_create(id=event_id)
                    event.event_name = event_name
                    event.event_date = event_date
                    event.address = location_str
                    event.location = point
                    event.save()
            except ValueError as e:
                # Handle errors when updating event details
                error_message = f"edit error: {str(e)}"
                print(error_message)
                pass
        elif event_id is not None and event_name is not None and event_date is not None:
            try:
                # Update event details without changing the location
                event, created = Event.objects.get_or_create(id=event_id)
                event.event_name = event_name
                event.event_date = event_date
                event.save()
            except ValueError as e:
                error_message = f"edit error: {str(e)}"
                print(error_message)
                pass

        form = EventForm()

        # Retrieve and render events associated with the current user
        events_list = Event.objects.filter(user=request.user)

        return render(request, "profile.html", {'events': events_list, 'form': form})


# Define the login view function
def login(request):
    # Render the login.html template with an empty UserForm
    context = {"form": UserForm()}
    return render(request, "registration/login.html", context)

    # Define the offline view function


def offline(request):
    # Render the offline.html template
    return render(request, "offline.html")

    # Define the manifest view function


def manifest(request):
    # Render the manifest.json file with PWA settings
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


# Define the service_worker view function
def service_worker(request):
    # Serve the PWA service worker script
    response = HttpResponse(
        open(app_settings.PWA_SERVICE_WORKER_PATH).read(), content_type="application/javascript"
    )
    return response
