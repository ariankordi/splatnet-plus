# SplatNet (Plus?)
Yes, because Nintendo.

# Requirements
Not much.

* Django
* Pillow

# How to use
Configure your database (or don't if your using SQLite, I think), and then run `python3 manage.py runserver 0.0.0.0:8000` if you want to run it in Django's development environment. That should be it, this is just a standard Django app though.

# How to use ON WII U?!?!
It's pretty simple once you've got MitM-ing up on Wii U with Fiddler. Right now, this FiddlerScript works for me: (in OnBeforeRequest)
```js
       if(oSession.host == "wup-agmj.app.nintendo.net") {
            oSession.oRequest.headers.UriScheme = "http";
            oSession.host="192.168.1.127:8000";
        }
```

And that would be if my server was running at `192.168.1.127:8000`.

After that, it should just pass right through there.

# How to ADMINISTRATE?!?!
After configuring your database and all that, go to `/admin/`.

It'll prompt you for a username and password. Great, let's make a user.
`python3 manage.py createsuperuser` will walk you through this. We are using Django's default user models, so it'll appear like that and ask you for an email address.

Once you've done that, now you can administrate. :sunglasses:
