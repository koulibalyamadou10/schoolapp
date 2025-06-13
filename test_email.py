#!/usr/bin/env python
import os
import sys
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolapp.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email_configuration():
    """Test la configuration email"""
    print("=== TEST DE CONFIGURATION EMAIL ===")
    print(f"EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', 'Non configuré')}")
    print(f"EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', 'Non configuré')}")
    print(f"EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', 'Non configuré')}")
    print(f"EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', 'Non configuré')}")
    print(f"EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', 'Non configuré')}")
    print(f"EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', 'Non configuré')}")
    print(f"EMAIL_HOST_PASSWORD: {'***' if getattr(settings, 'EMAIL_HOST_PASSWORD', None) else 'Non configuré'}")
    print(f"DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', 'Non configuré')}")
    print("=====================================")

def test_send_email():
    """Test l'envoi d'un email simple"""
    try:
        print("\n=== TEST D'ENVOI D'EMAIL ===")
        
        # Email de test
        test_email = input("Entrez votre email pour le test (ou appuyez sur Entrée pour utiliser test@example.com): ").strip()
        if not test_email:
            test_email = "test@example.com"
        
        subject = 'Test d\'envoi d\'email - SchoolApp'
        message = """
Ceci est un email de test pour vérifier la configuration email de SchoolApp.

Si vous recevez cet email, la configuration fonctionne correctement.

Cordialement,
L'équipe SchoolApp
        """
        
        print(f"Envoi d'un email de test à : {test_email}")
        
        result = send_mail(
            subject,
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@schoolapp.com'),
            [test_email],
            fail_silently=False,
        )
        
        print(f"Résultat de l'envoi : {result}")
        
        if result == 1:
            print("✅ Email envoyé avec succès !")
        else:
            print("❌ Échec de l'envoi de l'email")
            
    except Exception as e:
        print(f"❌ ERREUR lors de l'envoi de l'email : {e}")
        print(f"Type d'erreur : {type(e).__name__}")
        import traceback
        print(f"Traceback complet : {traceback.format_exc()}")

if __name__ == "__main__":
    test_email_configuration()
    
    # Demander si l'utilisateur veut tester l'envoi
    test_send = input("\nVoulez-vous tester l'envoi d'un email ? (o/n): ").strip().lower()
    if test_send in ['o', 'oui', 'y', 'yes']:
        test_send_email()
    else:
        print("Test d'envoi ignoré.")
