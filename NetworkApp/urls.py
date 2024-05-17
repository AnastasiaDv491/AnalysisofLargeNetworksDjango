from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.all_listings, name="all_listings"),
    path("doc_id/<int:doc_id>/", views.doc, name="doc"),
    path("art_id/<int:art_id>/", views.art, name="art"),
    path("art_v_id/<int:art_v_id>/", views.art_v, name="art_v_id"),
    path("report/", views.about, name="about"),
    path("statistics/", views.stats, name="stats"),
]
