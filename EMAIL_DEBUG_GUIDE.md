# Guide de Debug et Configuration Email - SchoolApp

## Améliorations apportées

### 1. Configuration Email améliorée dans settings.py

- Ajout de `EMAIL_USE_TLS` et `DEFAULT_FROM_EMAIL`
- Correction du conflit entre `EMAIL_USE_TLS` et `EMAIL_USE_SSL`
- Ajout d'un message informatif pour le mode développement

### 2. Debug avancé dans les formulaires

#### Teacher Forms (teacher/forms.py)
- Ajout de logs détaillés pour l'envoi d'emails
- Affichage des paramètres de configuration email
- Gestion d'erreurs avec traceback complet
- Vérification du résultat de l'envoi

#### Student Forms (student/forms.py)
- Même système de debug que pour les enseignants
- Correction de l'URL de connexion dans l'email

### 3. Script de test email (test_email.py)

Un script autonome pour tester la configuration email :
- Affiche tous les paramètres de configuration
- Permet de tester l'envoi d'un email
- Gestion d'erreurs détaillée

### 4. Fichier d'exemple de configuration (.env.example)

Exemples de configuration pour différents fournisseurs :
- Mode développement (console)
- Gmail
- Autres fournisseurs SMTP

### 5. Correction des erreurs CSRF

- Correction de la vue `assign_subjects` dans teacher/views.py
- Amélioration de la gestion des erreurs
- Correction du template assign_subjects.html

## Comment utiliser le debug

### 1. Vérifier la configuration
```bash
python test_email.py
```

### 2. Créer un enseignant ou étudiant
Les logs détaillés apparaîtront dans la console du serveur Django :

```
=== DEBUG EMAIL ENSEIGNANT ===
Destinataire : teacher@example.com
Expéditeur : noreply@schoolapp.com
Backend email : django.core.mail.backends.smtp.EmailBackend
Host email : smtp-fr.securemail.pro
Port email : 465
============================
Résultat de l'envoi d'email enseignant : 1
Email enseignant envoyé avec succès !
```

### 3. En cas d'erreur
Le système affichera :
- Le type d'erreur
- Le message d'erreur détaillé
- Le traceback complet

## Configuration recommandée

### Pour le développement
```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Pour la production avec Gmail
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=votre_email@gmail.com
```

### Pour la production avec un autre fournisseur
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.votre-fournisseur.com
EMAIL_HOST_USER=votre_email@domaine.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False
DEFAULT_FROM_EMAIL=noreply@votre-domaine.com
```

## Points importants

1. **EMAIL_USE_TLS et EMAIL_USE_SSL sont mutuellement exclusifs** - Un seul doit être à True
2. **Le backend console** affiche les emails dans la console au lieu de les envoyer
3. **Les mots de passe d'application Gmail** sont requis si vous utilisez l'authentification à deux facteurs
4. **Le debug est automatiquement activé** lors de la création d'enseignants et d'étudiants

## Dépannage

### Erreur "CSRF token from POST has incorrect length"
- Vérifiez que `{% csrf_token %}` est présent dans le formulaire
- Assurez-vous que les cookies sont activés dans le navigateur

### Erreur "EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive"
- Définissez seulement l'un des deux à True dans votre fichier .env

### Email non reçu
- Vérifiez les logs de debug dans la console
- Testez avec le script test_email.py
- Vérifiez vos paramètres SMTP
