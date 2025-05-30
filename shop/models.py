from django.db import models
from django.contrib.auth.models import User

class Produit(models.Model):
    GENRES = [
        ('homme', 'Homme'),
        ('femme', 'Femme'),
        ('enfant', 'Enfant'),
    ]
    
    CATEGORIES = [
        ('chaussures', 'Chaussures'),
        ('vetements', 'Vêtements Sportif'),
        ('fitness', 'Fitness & Musculation'),
        ('velo', 'Vélo'),
    ]
    
    TAILLES_CHAUSSURES = [
        ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'),
        ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'),
    ]
    
    TAILLES_VETEMENTS = [
        ('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'),
        ('XXL', 'XXL'), ('XXXL', 'XXXL'),
    ]
    
    TAILLES_ENFANT = [
        ('2A', '2 ans'), ('4A', '4 ans'), ('6A', '6 ans'), ('8A', '8 ans'),
        ('10A', '10 ans'), ('12A', '12 ans'), ('14A', '14 ans'),
    ]

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=255)
    
    genre = models.CharField(max_length=10, choices=GENRES, default='homme')
    categorie = models.CharField(max_length=50, choices=CATEGORIES, default='autres')
    
# Gestion des tailles
    tailles_disponibles = models.JSONField(default=list, blank=True)
    
    # Pour le stock (optionnel)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.nom
    
    
    def save(self, *args, **kwargs):
        # Définir automatiquement les tailles disponibles selon la catégorie
        if not self.tailles_disponibles:
            if self.categorie == 'chaussures':
                if self.genre == 'enfant':
                    self.tailles_disponibles = [size[0] for size in self.TAILLES_ENFANT]
                else:
                    self.tailles_disponibles = [size[0] for size in self.TAILLES_CHAUSSURES]
            elif self.categorie == 'vetements':
                self.tailles_disponibles = [size[0] for size in self.TAILLES_VETEMENTS]
        
      
        
        super().save(*args, **kwargs)
    
    def get_tailles_display(self):
        """Retourne les tailles disponibles formatées pour l'affichage"""
        if self.categorie == 'chaussures':
            taille_dict = dict(self.TAILLES_CHAUSSURES + self.TAILLES_ENFANT)
        else:
            taille_dict = dict(self.TAILLES_VETEMENTS)
        
        return [taille_dict.get(t, t) for t in self.tailles_disponibles]



class PanierItem(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    taille = models.CharField(max_length=10, blank=True, null=True)  # Ajout de la taille
    def __str__(self):
        return f"{self.produit.nom} x {self.quantite}"
