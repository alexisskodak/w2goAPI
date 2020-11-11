# Where To Go - API
Rest API that makes requests to Google Maps Places
and returns an array of objects (Places) near a
specified location.
Returned Places attributes are:

```name```, ```formated_address```, ```icon```, ```photo```
```rating``` and ```types```

It also handles GET, PUT, POST and DELETE requests for custom
"Step" and "Itinerary" Objects.

## Get Places Details nearby by Geolocation

### Sample request:
```javascript
    $.ajax({

        url: `${base_url}/api/gmaps-places/?location=${location}&keyword=${type}&radius=${radius}`,
        type: "GET",
        dataType: "json",
        xhrFields: {withCredentials: true },
        headers: {Authorization: 'Token ' + MY_TOKEN},

        success: function(response) {
            console.log(response);
        },

        error: function(error) {
            console.log(error);
        }
    });
```

Would pass a query string like so:

```https://sampledomain.com/api/gmaps-places/?location=xxxx&keyword=xxxx&radius=xxxx```

Required parameters are:
- ```location```: (string). A latitude - longitude pair separated by a comma
- ```radius```: (integer) Meters. Max: 9999

In order to get a usable response, passing a keyword parameter is recommended
- ```keyword```: (string) A term to be matched against all content that Google 
has indexed for this place, including but not limited to name, type, and address, 
as well as customer reviews and other third-party content.

### Sample response object:

```json
{
"name": "La Boîte à Café",
"formatted_address": "3 Rue de l'Abbé Rozier, 69001 Lyon, France",
"icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/cafe-71.png",
"photos": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=20wjRl58zEeXbw&key=API_KEY",
"rating": 4.5,
"types": [ "bakery", "cafe", "restaurant" ]
}
```


                        
