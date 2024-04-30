from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from NetworkApp.models import article, document

from neomodel import db

# def index(request):
#     # return HttpResponse("Hello, world. You're at the polls index.")
#     all_country_nodes = document.nodes.all()
#     context = {"all": all_country_nodes}
#     return render(request, "NetworkApp/index.html", context)


def all_listings(request):
    year = request.GET.get("year")
    id = request.GET.get("doc_id")
    type = request.GET.get("type")
    """
    Function that processes doc code filter results
    output: dictionary "context" containing doc_id, type, and "about" document section
    """
    if year:
        year = int(year)
        query = (
            f"MATCH (d:document) WHERE d.year = {year} RETURN d.doc_id, d.type,d.about"
        )
        all_listings, meta = db.cypher_query(query, resolve_objects=True)
    elif id:
        id = int(id)
        all_listings = document.nodes.filter(doc_id=id)
        # print(all_listings.doc_id)
    elif type:
        type = str(type)
        print(type)
        query = f"MATCH (d:document) WHERE d.type = '{type}' RETURN d.doc_id, d.type,d.about"
        all_listings, meta = db.cypher_query(query, resolve_objects=True)

    else:
        all_listings = None

    context = {"all_listings": all_listings}

    return render(request, "NetworkApp/search-form.html", {"context": context})


def from_DB(request):
    id = request.GET.get("doc_id")
    figures_list = document.nodes.get(doc_id=id)
    print(id)
    results = {"figures_list": figures_list}
    return render(request, "NetworkApp/search-form.html", results)


def doc(request, doc_id):
    file = document.nodes.get(doc_id=doc_id)

    context = {"doc": file}
    print(context)

    return render(request, "NetworkApp/dashboard_main.html", {"context": context})


def about(request):
    return render(request, "NetworkApp/report.html", {})
