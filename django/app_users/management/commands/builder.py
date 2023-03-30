from app_users.models import User, Sock, UserProfilePicture, SockProfilePicture

from app_geo.utilities import GeoLocation
from datetime import date, timedelta
import os
import random
import names
import requests
import os
import cloudinary
import cloudinary.uploader


def get_city():
    s = [
        "Stuttgart",
        "München",
        "Berlin",
        "Potsdam",
        "Potsdam",
        "Hamburg",
        "Wiesbaden",
        "Schwerin",
        "Hannover",
        "Düsseldorf",
        "Mainz",
        "Saarbrücken",
        "Dresden",
        "Magdeburg",
        "Kiel",
        "Erfurt",
    ]
    return s[random.randint(0, 15)]


def gen_user(gender=None):
    city = get_city()
    first_name = names.get_first_name(gender=gender)
    last_name = names.get_last_name()
    username = first_name + last_name + str(random.randint(1, 100))
    if gender == "male":
        gender = "2"
    else:
        gender = "1"

    lat, longi = GeoLocation.get_geolocation_from_city(city)
    user = User(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=str(first_name + "." + first_name + "@" + "gmail.com"),
        info_about="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec egestas massa quis imperdiet luctus. Aenean ut arcu id lectus dapibus faucibus sed at quam. Integer magna nulla, sollicitudin vel diam ut, vulputate pellentesque sapien. Nunc lobortis nisi felis, quis aliquam libero efficitur sed. Sed tincidunt nisl mauris, ut blandit nulla commodo sed. Curabitur vel arcu nisl. In commodo massa mauris, consectetur tempor velit ultrices sit amet. Pellentesque eget est ligula. Vestibulum quis molestie velit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Ut vel tristique sapien, sit amet ultrices eros.",
        info_birthday=date.today() - timedelta(356 * (18 + random.randint(0, 20))),
        info_gender=gender,
        location_city=city,
        location_latitude=lat,
        location_longitude=longi,
        notification=True,
        social_instagram="",
        social_facebook="",
        social_twitter="",
        social_spotify="",
    )
    return user


def gen_sock(user):
    if random.randint(1, 2) % 2 == 0:
        gender = "male"
    else:
        gender = "female"

    sock_name = names.get_first_name(gender)

    sock = Sock(
        user=user,
        info_name=sock_name,
        info_about="Praesent eleifend vulputate metus. Vivamus porttitor iaculis velit, id luctus est tincidunt ut. Vestibulum vitae felis enim. In est leo, eleifend non accumsan ac, imperdiet eu augue.",
        info_color=str(random.randint(1, 10)),
        info_fabric=str(random.randint(1, 7)),
        info_fabric_thickness=str(random.randint(1, 7)),
        info_brand=str(random.randint(1, 13)),
        info_type=str(random.randint(1, 9)),
        info_size=str(random.randint(1, 7)),
        info_age=random.randint(0, 5),
        info_separation_date=date.today() - timedelta(356 * (random.randint(0, 5))),
        info_condition=str(random.randint(1, 12)),
        info_holes=random.randint(0, 4),
        info_kilometers=random.randint(0, 250),
        info_inoutdoor=str(random.randint(1, 9)),
        info_washed=random.randint(0, 4),
        info_special="ut semper. Nunc condimentum leo enim, id consectetur",
    )
    return sock


def run(max_user):
    path = os.getcwd() + "/app_users/management/commands/fake_profile_pics/"

    for i in range(max_user):
        if i % 2 == 0:
            gender = "male"
        else:
            gender = "female"

        url = "https://xsgames.co/randomusers/avatar.php?g=" + gender
        user_pic = requests.get(url, allow_redirects=True)
        user_profile_file = f"{path}pic_{gender}_{i}.jpg"
        a = open(user_profile_file, "wb")
        a.write(user_pic.content)
        a.close()
        upload_result = cloudinary.uploader.upload(str(user_profile_file))
        public_id = upload_result["public_id"]

        user = gen_user(gender)
        pic = UserProfilePicture(user=user, profile_picture=public_id)
        os.remove(user_profile_file)
        user.save()
        pic.save()
        print("adding user:", user, pic)

        old_sock = sock_profile_file = f"{path}sock{random.randint(0, 30)}.jpeg"
        for j in range(random.randint(2, 4)):
            sock_profile_file = f"{path}sock{random.randint(0, 30)}.jpeg"

            upload_result = cloudinary.uploader.upload(str(sock_profile_file))
            public_id = upload_result["public_id"]

            sock = gen_sock(user)
            pic = SockProfilePicture(sock=sock, profile_picture=public_id)
            # os.remove(sock_profile_file)
            sock.save()
            pic.save()
            print("adding sock:", sock, pic)
