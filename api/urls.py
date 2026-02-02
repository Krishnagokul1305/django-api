from django.urls import path,include

urlpatterns=[
    path("users/",include("users.urls")),
    path("auth/",include("auth.urls")),
    path("internships/",include("internshihips.urls")),
    path("webinars/",include("webinars.urls")),
    path("memberships/",include("memberships.urls")),
]

