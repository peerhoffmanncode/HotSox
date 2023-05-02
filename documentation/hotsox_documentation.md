# HOTSOX "app_users"
The "app_user" of the HotSox Project is composed by different features that handles the User Profiles and their related Socks profile/s.


## FEATURE Login and User CRUD using “Django AllAuth”

### Purpose
The purpose/ aim of the feature is to give the user the option to register/ sign in/ sign out or edit preferences with the app.

### Description
A user can signup to the app by entering his personal information and attributes from username, password to age and city where the user lives in.
During this signup process we lookup the geolocation (longitude and latitude) from the given city name. Everything will be stored to our database as the main user model.
Using AllAuth we do not have to create the whole authentication process but relay on what is done by this package.
A user can upload one or many profile picture/s which will be stored to the cloudinary CDN. We use their python SDK packet to make it most convenient for our development experience [https://cloudinary.com/documentation/python_quickstart]. This SDK includes a Django ready model field as a specific “picture upload field”.
Users can edit their profiles as well as add or remove pictures from their profile pictures.

A user can see a profile overview that shows all his/her personal data as well as a visual representation of his geo location on a map created by folium. As a part of this overview a user is also able to delete his/ her account. An account deletion will also delete any dependent data (socks, pictures, messages, chats) from the database.

A user can create an account at hotsox using the social media login via Oatuth2.0 via google. He/ She needs to have a valid account at google. Validation and password hashing is done by google in this case.

### Technical implementation
The whole app is designed around the logged in user. Every aspect of the app, every functionality, every backend or frontend part is validating that a given user has the permission to do a certain action. A logged in user can only see him-/herself, it's own socks, and all actions that has him/her as the center of interest. A user can only interact with another user once they have a valid match. This means you can only see, chat, interact with a users you matched.
This is done using custom validation mixing classes that inherit their main functionality from Djangos “LoginRequiredMixin” class. Every view or endpoint is protected, except the signup and login.

### UI/UX:
Our frontend uses custom forms for signup / login / and log out. The forms are designed using crispy forms as well as custom form widgets. The widgets are a custom switch to enable/ disable notifications, and sliding range selectors for any numeric input field.

### Licenses & Dependencies
Django AllAuth https://django-allauth.readthedocs.io/en/latest/
Django crispy forms https://django-crispy-forms.readthedocs.io/en/latest/
Cloudinary SDK https://cloudinary.com/documentation/python_quickstart/


## FEATURE Websocket based chat-module using “Django Channels“

### Purpose
The purpose/ aim of the feature is to realize a realtime chat between two users of the hotsox app.

### Description
If one user sends a json encoded message using a websocket request to the backend, first it will be stored to the database. Secondly it will be resend from the backend to all subscribed listeners. In our case, this will include the sender itself as well as the “other” user that this message was actually meant for. A message has a string as payload content, a sending date and a seen date.
Once a message got “seen” in a frontend, it will be marked as seen and therefore stored with the “seen_date” in the database.
We have a Javascript Ajax function (websocket) waiting for a response (send message) from the backend. Once such a message got received the function will inject this message into a html <div> to show this message to the user. It will also send this message to the backend again, to mark it as “seen”.

### Technical implementation
In the backend we use the websocket based library Django Channels [https://channels.readthedocs.io/en/stable/] in version 3.0.5. We decided to use version 3.0.5 because version 4.0 has some serious issues with the later versions of Uvicorn and Django. For our current MVP the version 3.0.5 fulfills all our needs.
Crucial to have websockets work is to run the whole Django project asynchronously. So we decided to switch from the standard WSGI server to the ASGI server. As deployment server we decided on Uvicorn as our production server [https://www.uvicorn.org].
Our frontend uses native Javascript and its build in websocket support. Alls the function calls are asynchronous as well.

### UI/UX
Our user experience should be as simple as possible for the moment. As MVP we decided to have a simple input box for max 160 chars and text box that represents the chat history for a max of the latest 300 messages.

### Licenses
This feature did not use any specific license agreements aside to the main ones.




# HOTSOX "app_home"
The "app_home" of the HotSox Project contains the pre_prediction algorithm that handles the match preselection between User/Socks profiles.

## FEATURE Pre-Prediction Algorithm

### Purpose
The purpose of the 'Pre-Prediction Algorithm' is to predict the next sock that a user might like based on the similarity score calculated from their previous sock preferences.

### Description
The algorithm calculates a similarity score between two socks and then filters out the socks which have already been liked or disliked by the user, as well as the user's own socks. The remaining unseen socks are then sorted in decreasing order of similarity to the user's current sock, and the most similar sock is returned as the next suggested sock match.







# HOTSOX "app_geo-location"

### Description
The geolocation feature in this application uses a third-party database called GeoLite2 to determine the country and city associated with an IP address.

### Purpose
The Geo-location feature is intended to determine the physical location of the device using the Hot-Sox application. This information can be useful for a variety of future potential purposes, such as providing location-based services, delivering targeted advertising, and improving security by identifying potential fraudulent activity.
NOTE: it is important to note that Geo-location is not always accurate, and there may be privacy concerns associated with collecting and using this information. Users should be informed about how their location data will be used and have the option to opt-out if they choose. Additionally, websites and applications should comply with relevant data privacy regulations when collecting and using location data.

### Technical Implementation
The technical implementation of the location feature involves the use of geolocation API to retrieve the user's location. This API provides a simple way for websites to access the user's location information without requiring any additional plugins or software.
Once the user's location is retrieved, the website uses a combination of client-side scripting and server-side programming to process and display the location information to the user.
To enhance the accuracy of the location information, the app incorporated the use of a third-party database: the MaxMind's GeoLite2 database. This database provides IP geolocation data which can be used to estimate the user's location based on their IP address, by parsing the database file, to query the data

### UI/UX
Overall, the UI/UX of this feature is likely to be fairly simple and straightforward, with a focus on providing an useful geolocation data to the user in a clear and concise manner by the use of Folium to display the OpenStreetMap with Mercator Projection onto the webpage corresponding to the approximate location of the user related to its IP address. A marker icon with a pair of sox will mark the User’s city center location.
As soon as a user match with another via the app, a connecting line in blue automatically appears on map, connecting the 2 location and simultaneously the map zoom out to fit the relevant scale of the match on the chart.

### Dependencies
In order to work, the Geo App is using 5 dependencies: Folium, geodesic, Nominatim, GeoIP2 and GeoLite2 Database.
- Folium is a Python library used to create interactive maps with data visualization capabilities.
- Geodesic is part of the GeoPy library and provides functions for calculating geodesic distances on the ellipsoid model of the earth.
- Nominatim is a search engine for OpenStreetMap (OSM) data that can be used to geocode addresses and find points of interest.
- GeoIP2 is a Python library that provides access to MaxMind's binary GeoIP2 databases for geolocation data.
- GeoLite2 Database is a free geolocation database offered by MaxMind that provides IP geolocation data.

### Licenses
The GeoLite2 end-user license agreement applies to the GeoLite2 database used for the geolocation feature. It incorporates components of the Creative Commons Attribution-ShareAlike 4.0 International License. The attribution requirement may be met by including the following in all advertising and documentation mentioning features of or use of GeoLite2 data:
> “This product includes GeoLite2 data created by MaxMind, available from
> <a href="https://www.maxmind.com">https://www.maxmind.com</a>.”
