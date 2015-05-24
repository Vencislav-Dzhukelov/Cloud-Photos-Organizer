from django.conf.urls import url, patterns


urlpatterns = patterns('website.views',
                       url(r'^$', 'index', name="index"),
                       url(r"^register/$", 'register', name="register"),
                       url(r"^organizer/", 'organizer', name="organizer"),
                       url(r"^logout/$", 'organizer_logout', name="logout"),
                       url(r"^contact/$", 'contact', name="contact"),
                       )
