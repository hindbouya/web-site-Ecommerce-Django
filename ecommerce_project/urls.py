"""
URL configuration for ecommerce_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from shop import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from shop.views import create_checkout_session


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')
urlpatterns = [
   
    
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('compte/', include('django.contrib.auth.urls')),  # URLs d'authentification natives
    path('inscription/', views.inscription, name='register'),

    
     # URLs d'authentification
     # Authentification
    path('compte/connexion/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('compte/inscription/', views.inscription, name='inscription'),
    path('compte/deconnexion/', logout_view, name='logout'),
    path('ajouter-au-panier/<int:produit_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
    path('panier/', views.panier, name='panier'),

path('compte/connexion/', auth_views.LoginView.as_view(), name='login'),
path('panier/modifier/<int:item_id>/', views.modifier_quantite, name='modifier_quantite'),
path('panier/supprimer/<int:item_id>/', views.supprimer_du_panier, name='supprimer_du_panier'),
path('recherche/', views.recherche, name='recherche'),
path('produits/<str:genre>/<str:categorie>/', views.produits_par_genre_categorie, name='produits_filtrés'),
path('categorie/<str:categorie_slug>/', views.produits_par_categorie, name='produits_filtrés'),

    path('mon-compte/', views.mon_compte, name='mon_compte'),

path('produit/<int:produit_id>/', views.detail_produit, name='detail_produit'),

  path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),
    path('paiement-reussi/', views.paiement_reussi, name='paiement-reussi'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)