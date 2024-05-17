# Create your models here.
from django.db import models
from neomodel import (
    config,
    StructuredNode,
    StringProperty,
    IntegerProperty,
    DateTimeFormatProperty,
    RelationshipFrom,
    RelationshipTo,
)
from django_neomodel import DjangoNode
from django import forms


class document(DjangoNode):
    doc_id = IntegerProperty(unique_index=True, required=True)
    about = StringProperty(unique_index=False, required=False)

    # date = DateTimeFormatProperty(format="%Y-%m-%d %H:%M:%S", required=False)
    type = StringProperty(unique_index=False, required=False)

    year = IntegerProperty(unique_index=False, required=False)
    month = IntegerProperty(unique_index=False, required=False)
    day = IntegerProperty(unique_index=False, required=False)

    doc_rel = RelationshipTo("document", "rel")


class article(StructuredNode):
    art_id = StringProperty(unique_index=True, required=True)


class article_version(StructuredNode):
    art_v_id = StringProperty(unique_index=True, required=True)
    title = StringProperty(unique_index=False, required=False)
