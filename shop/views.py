from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import Produit, PanierItem
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

# Vue d'inscription
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Inscription réussie !')
            return redirect('login')  # Redirection vers la page de connexion après inscription
    else:
        form = UserCreationForm()
    return render(request, 'shop/inscription.html', {'form': form})

# Vue d'accueil
def home(request):
    equipements_fitness = Produit.objects.filter(categorie='fitness')
    chaussures = Produit.objects.filter(categorie='chaussures')
    vetements_sportif = Produit.objects.filter(categorie='vetements')  # ✅ Ajout de la catégorie vêtements

    context = {
        'equipements_fitness': equipements_fitness,
        'chaussures': chaussures,
        'vetements_sportif': vetements_sportif,  # ✅ Ajout au contexte
    }
    return render(request, 'shop/home.html', context)


# Vue pour ajouter un produit au panier
@login_required(login_url=reverse_lazy('login'))
def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    # On utilise 'utilisateur' car c'est le nom du champ dans le modèle PanierItem
    panier_item, created = PanierItem.objects.get_or_create(
        utilisateur=request.user,  # et non 'user=request.user'
        produit=produit
    )
    
    if not created:
        panier_item.quantite += 1  # Assure-toi que tu utilises 'quantite' ici aussi
        panier_item.save()
    
    # Incrémenter le compteur d'articles dans la session
    if 'panier' not in request.session:
        request.session['panier'] = 0
    
    request.session['panier'] += 1
    request.session.modified = True  # Indiquer que la session a été modifiée
    
    return redirect('home')  # ou vers la page panier si tu veux

    produit = get_object_or_404(Produit, id=produit_id)
    
    # On utilise 'utilisateur' car c'est le nom du champ dans le modèle PanierItem
    panier_item, created = PanierItem.objects.get_or_create(
        utilisateur=request.user,  # et non 'user=request.user'
        produit=produit
    )
    
    if not created:
        panier_item.quantite += 1  # Assure-toi que tu utilises 'quantite' ici aussi
        panier_item.save()
    
    return redirect('home')  # ou vers la page panier si tu veux

# Vue pour afficher le panier
@login_required

def panier(request):
    panier_items = PanierItem.objects.filter(utilisateur=request.user)  # Récupération des éléments du panier
    total_panier = sum(item.produit.prix * item.quantite for item in panier_items)  # Utilisation de 'quantite' au lieu de 'quantity'

    context = {
        'produits': panier_items,
        'total_panier': total_panier
    }
    return render(request, 'shop/panier.html', context)



# Vue pour afficher les produits de la boutique
def boutique(request):
    produits = Produit.objects.filter(categorie="chaussures")
    equipements_fitness = Produit.objects.filter(categorie="fitness")
    vetements_sportif = Produit.objects.filter(categorie='vetements')
    return render(request, 'shop/boutique.html', {
        'produits': produits,
        'equipements_fitness': equipements_fitness,
         'vetements_sportif': vetements_sportif,
    })
from django.shortcuts import redirect, get_object_or_404

def modifier_quantite(request, item_id):
    item = get_object_or_404(PanierItem, id=item_id)
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantite'))
        if new_quantity >= 1:
            item.quantite = new_quantity  # Utilisation de 'quantite' ici
            item.save()
    return redirect('panier')


def supprimer_du_panier(request, item_id):
    item = get_object_or_404(PanierItem, id=item_id)
    item.delete()
    
    # Décrémenter le compteur dans la session
    if 'panier' in request.session and request.session['panier'] > 0:
        request.session['panier'] -= 1
        request.session.modified = True
    
    return redirect('panier')


from django.db.models import Q

def recherche(request):
    query = request.GET.get('q')
    produits = []
    if query:
        produits = Produit.objects.filter(Q(nom__icontains=query))
    
    context = {
        'query': query,
        'produits': produits,
    }
    return render(request, 'shop/recherche.html', context)


def produits_par_genre_categorie(request, genre, categorie):
    produits = Produit.objects.filter(genre=genre, categorie=categorie)
    return render(request, 'shop/produits_filtrés.html', {
        'produits': produits,
        'genre': genre,
        'categorie': categorie
    })
    

def produits_par_categorie(request, categorie_slug):
    produits = Produit.objects.filter(categorie=categorie_slug)
    return render(request, 'shop/produits_par_categorie.html', {'produits': produits, 'categorie': categorie_slug})




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages

from django.contrib import messages
from .forms import ModifierCompteForm
@login_required

def mon_compte(request):
    if request.method == 'POST':
        form = ModifierCompteForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été mis à jour.')
            return redirect('mon_compte')
    else:
        form = ModifierCompteForm(instance=request.user)

    return render(request, 'shop/mon_compte.html', {'form': form})



from django.shortcuts import render, get_object_or_404
from .models import Produit  # Assurez-vous que c'est le bon nom de modèle

def detail_produit(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    context = {
        'produit': produit,
        'tailles': produit.get_tailles_display(),  # Utilise la nouvelle méthode
        'title': f"Détails - {produit.nom}",
    }
    return render(request, 'shop/detail_produit.html', context)


import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY_TEST

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        try:
            # Créer une session Stripe
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'eur',
                            'product_data': {
                                'name': 'Commande Test',
                            },
                            'unit_amount': int(float(request.POST.get('total'))) * 100,
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/paiement-reussi/'),
                cancel_url=request.build_absolute_uri('/panier/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
def paiement_reussi(request):
    return render(request, 'shop/paiement_reussi.html')