from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import matplotlib.pyplot as plt, mpld3
import matplotlib
from NetworkApp.models import article, document
import io
import base64, urllib
from neomodel import db
import numpy as np
from io import BytesIO
import pandas as pd
from plotly.offline import plot
from plotly.graph_objs import Bar, Histogram
import networkx as nx
import os


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
        all_listings = document.nodes.first(doc_id=id)
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


def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


def doc(request, doc_id):
    file = document.nodes.get(doc_id=doc_id)
    context = {"doc": file}
    query = f"MATCH (d:document)-[:ARTICLE]->(a:article) WHERE d.doc_id = {doc_id} RETURN a.art_id"

    query2 = f"MATCH (d:document)-[r:rel]->(p:document) WHERE d.doc_id = {doc_id} RETURN p.doc_id, r.rel "
    query3 = f"MATCH (d:document)-[r:keyword]->(k:keyword) WHERE d.doc_id = {doc_id} RETURN k.key_name"

    art_details, meta = db.cypher_query(query, resolve_objects=True)
    art_details = flatten_concatenation(art_details)

    doc_rel, meta = db.cypher_query(query2, resolve_objects=True)
    # doc_rel = flatten_concatenation(doc_rel)

    key_rel, meta = db.cypher_query(query3, resolve_objects=True)
    key_rel = flatten_concatenation(key_rel)

    print(doc_rel)
    return render(
        request,
        "NetworkApp/dashboard_main.html",
        {
            "context": context,
            "art_details": art_details,
            "doc_rel": doc_rel,
            "key_rel": key_rel,
        },
    )


def art(request, art_id):
    art_id = str(art_id)
    query = f"MATCH (a:article) WHERE a.art_id = {art_id} RETURN a.art_id"
    art_details, meta = db.cypher_query(query, resolve_objects=True)
    art_details = flatten_concatenation(art_details)

    # get article versions
    query2 = f"MATCH (a:article)-[:VERSION]->(v:article_version) WHERE a.art_id = {art_id} RETURN v.art_v_id, v.startdate, v.title"
    v_details, meta = db.cypher_query(query2, resolve_objects=True)
    return render(
        request,
        "NetworkApp/article.html",
        {"context": art_details, "version": v_details},
    )


def art_v(request, art_v_id):

    art_v_id = str(art_v_id)
    query = f"MATCH (v:article_version) WHERE v.art_v_id = {art_v_id} RETURN v.art_v_id, date(v.startdate), v.title, v.enddate"
    art_details, meta = db.cypher_query(query, resolve_objects=True)
    print(art_details)

    art_details = flatten_concatenation(art_details)

    return render(
        request,
        "NetworkApp/article_version.html",
        {"context": art_details},
    )


def stats(request):
    query = "MATCH (n:document) WITH distinct (n.type) as type, count(*) as count RETURN type, count"
    doc_type_count, meta = db.cypher_query(query, resolve_objects=True)

    doc_type = []
    count = []
    for i in doc_type_count:
        doc_type.append(i[0])
        count.append(i[1])

    # doc_type_count = flatten_concatenation(doc_type_count)
    doc_type_count_df = pd.DataFrame({"type": doc_type, "count": count})

    doc_type_count_df.loc[doc_type_count_df["count"] >= 100, "type"] = (
        doc_type_count_df["type"]
    )
    doc_type_count_df.loc[doc_type_count_df["count"] < 100, "type"] = "Other"

    plot_div = plot(
        [
            Bar(
                x=doc_type_count_df["type"],
                y=doc_type_count_df["count"],
                name="test",
            )
        ],
        output_type="div",
    )

    # GET THE AVG NUMEBR OF ARTICLES PER DOC
    query3 = "MATCH (d:document)-[:ARTICLE]->(a:article) with d.doc_id as id, count(a) as count return id, count"
    art_count, meta = db.cypher_query(query3, resolve_objects=True)

    doc_id = []
    count = []
    for i in art_count:
        doc_id.append(i[0])
        count.append(i[1])

    art_count_df = pd.DataFrame({"doc_id": doc_id, "count": count})
    art_count_df.loc[art_count_df["count"] >= 80, "count"] = 80
    art_count_df.loc[art_count_df["count"] < 80, "count"] = art_count_df["count"]

    plot_art_count = plot(
        [
            Histogram(
                x=art_count_df["count"],
                name="test",
            )
        ],
        output_type="div",
    )

    # BIG DOCUMENTS
    query4 = "MATCH (k:keyword)<-[:keyword]-(d:document)-[:ARTICLE]->(a:article) with d.doc_id as id, count(a) as count, k.key_name as key where count > 500 return distinct(key)"
    large_docs, meta = db.cypher_query(query4, resolve_objects=True)
    large_docs = flatten_concatenation(large_docs)
    return render(
        request,
        "NetworkApp/statistics.html",
        {
            "doc_type_count": plot_div,
            "plot_art_count": plot_art_count,
            "large_docs": large_docs,
        },
    )


def about(request):
    G = nx.DiGraph()
    G.add_edges_from(
        [
            ("document", "document"),
            ("document", "date"),
            ("document", "keyword"),
            ("document", "article"),
            ("article", "article version"),
        ]
    )
    pos = nx.spring_layout(G)

    nx.draw(
        G,
        pos,
        with_labels=True,
        edge_color="black",
        width=1,
        linewidths=1,
        node_size=500,
        node_color="pink",
    )
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels={
            ("document", "document"): ":REL",
            ("document", "date"): ":DATE",
            ("document", "keyword"): ":KEYWORD",
            ("document", "article"): ":ARTICLE",
            ("article", "article version"): ":VERSION",
        },
        font_color="red",
    )

    if not os.path.isfile("./NetworkApp/static/diagram1.png"):
        plt.savefig("./NetworkApp/static/diagram1.png")
    p = "hey"
    return render(
        request,
        "NetworkApp/report.html",
        {
            "plot": p,
        },
    )
