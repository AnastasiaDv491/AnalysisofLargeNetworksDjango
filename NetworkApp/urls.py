from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.all_listings, name="all_listings"),
    path("doc_id/<int:doc_id>/", views.doc, name="doc"),
    path("report/", views.about, name="about"),
]
