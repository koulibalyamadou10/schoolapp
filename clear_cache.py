#!/usr/bin/env python
"""
Script pour nettoyer le cache et les sessions Django
Utile quand il y a des problèmes avec les tokens CSRF
"""

import os
import sys
import django
from pathlib import Path

# Ajouter le répertoire du projet au path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolapp.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.sessions.models import Session
from django.core.cache import cache

def clear_sessions():
    """Supprimer toutes les sessions"""
    try:
        count = Session.objects.count()
        Session.objects.all().delete()
        print(f"✅ {count} sessions supprimées")
    except Exception as e:
        print(f"❌ Erreur lors de la suppression des sessions : {e}")

def clear_cache():
    """Vider le cache"""
    try:
        cache.clear()
        print("✅ Cache vidé")
    except Exception as e:
        print(f"❌ Erreur lors du vidage du cache : {e}")

def collect_static():
    """Collecter les fichiers statiques"""
    try:
        execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
        print("✅ Fichiers statiques collectés")
    except Exception as e:
        print(f"❌ Erreur lors de la collecte des fichiers statiques : {e}")

if __name__ == '__main__':
    print("🧹 Nettoyage du cache et des sessions Django...")
    print("=" * 50)
    
    clear_sessions()
    clear_cache()
    
    print("=" * 50)
    print("✅ Nettoyage terminé !")
    print("\n💡 Conseils :")
    print("1. Redémarrez le serveur Django")
    print("2. Videz le cache de votre navigateur (Ctrl+F5)")
    print("3. Essayez de vous reconnecter")
    print("\n🚀 Pour redémarrer le serveur :")
    print("   python manage.py runserver")
