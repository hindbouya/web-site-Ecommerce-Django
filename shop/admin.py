from django.contrib import admin
from .models import Produit
from .models import PanierItem

admin.site.register(Produit)
admin.site.register(PanierItem)
