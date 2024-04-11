
  

# GeoSpatial App

  

A GeoSpatial App to help you create, manage and find events.

  
  

## Functionality

  

Main functionality:

- Browse catalog of user created events.

- Create events.

- Edit listed events.

- Delete events

  
  
  

Adittional functionality:

- Browse activities from API provided from gov website.

- Modify event location. by clicking areas on map.

 - Browse events and activities by navigation through maps.




## Setup

  

Download the Django project.

 
After downloading the project open the project within PyCharm.

Ensure you have the appropriate libraries installed including Postgis.

  
  

### 1. Starting the server:

  

Once you are in the `geodjango_tutorial` directory, press the green start button in pyCharm and wait for the project to boot.


  
  

### 2. Accessing the webapp:

  

Open the following url in a browser of your choice.

  

```url

http://localhost/

```



### 3. Accessing the database:

  

Open the following url in a browser of your choice, then enter the database credentials. specified in your `settings.py` file.

  

```url

http://localhost:25432/

```

## Tech Stack

  

| Layer | Technologies |
|-----------------------|--------------------------|
| Frontend | HTML 5, django, CSS, JavaScript, bootstrap4, django-leaflet, ipykernel, psycopg2, gdal, pyproj |
| Middle Tier | django, python(3.11), Docker|
| Persistence Tier | postgres, postgis |
