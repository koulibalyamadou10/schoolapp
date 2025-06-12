# 🏫 SchoolApp – Système de Gestion Scolaire

Ce projet est un système de gestion scolaire développé avec Django et MySQL, permettant de gérer les utilisateurs (administrateurs, enseignants, étudiants), les matières, et les notes.

---

## 🚀 Fonctionnalités

### Gestion des Utilisateurs
- Authentification sécurisée (avec rôles : admin, enseignant, étudiant)
- Gestion des profils utilisateurs
- Système de récupération de mot de passe
- Tableau de bord personnalisé selon le rôle

### Gestion des Étudiants
- Inscription et gestion des étudiants
- Suivi des informations personnelles
- Gestion des dossiers académiques
- Suivi de l'assiduité
- Consultation des notes et bulletins

### Gestion des Enseignants
- Gestion des profils enseignants
- Attribution des matières
- Gestion des emplois du temps
- Saisie et modification des notes
- Suivi de l'assiduité des élèves

### Gestion Académique
- Gestion des matières et cours
- Planification des emplois du temps
- Gestion des salles de classe
- Organisation des examens
- Système de notation flexible

### Gestion Administrative
- Tableau de bord administratif
- Rapports et statistiques
- Gestion des annonces
- Communication interne
- Gestion des documents

---

## 🧱 Technologies

- **Framework** : Django 4+
- **Langage** : Python 3.10+
- **Base de données** : MySQL
- **ORM** : Django ORM
- **Front-end** : HTML5, CSS3, JavaScript
- **UI Framework** : Bootstrap 5
- **Sécurité** : hachage des mots de passe intégré

---

## 🗂️ Structure des apps Django

| App         | Description                              |
|-------------|------------------------------------------|
| `account`   | Gestion des utilisateurs et rôles        |
| `student`   | Gestion des étudiants                    |
| `teacher`   | Gestion des enseignants                  |
| `subject`   | Gestion des matières                     |
| `grade`     | Gestion des notes                        |
| `attendance`| Gestion de l'assiduité                  |
| `schedule`  | Gestion des emplois du temps            |
| `exam`      | Gestion des examens                     |
| `report`    | Génération des rapports et bulletins    |
| `message`   | Système de messagerie interne           |

---

## 🌐 URLs du projet
Après avoir lancé le serveur, vous pouvez accéder aux différentes interfaces :

### URLs de Compte (account/)
- Connexion : http://127.0.0.1:8000/account/login/
- Inscription : http://127.0.0.1:8000/account/register/
- Déconnexion : http://127.0.0.1:8000/account/logout/
- Profil : http://127.0.0.1:8000/account/profile/
- Changement de mot de passe : http://127.0.0.1:8000/account/profile/change-password/
- Réinitialisation de mot de passe : http://127.0.0.1:8000/account/password-reset/

- Tableaux de bord :
  - Admin : http://127.0.0.1:8000/account/admin-dashboard/
  - Enseignant : http://127.0.0.1:8000/account/teacher-dashboard/
  - Étudiant : http://127.0.0.1:8000/account/student-dashboard/

### URLs Enseignant (teacher/)
- Profil : http://127.0.0.1:8000/teacher/profile/
- Matières : http://127.0.0.1:8000/teacher/subjects/
- Emploi du temps : http://127.0.0.1:8000/teacher/schedule/
- Gestion des notes : http://127.0.0.1:8000/teacher/grades/
- Suivi de l'assiduité : http://127.0.0.1:8000/teacher/attendance/

### URLs Étudiant (student/)
- Liste des étudiants : http://127.0.0.1:8000/student/list/
- Création d'étudiant : http://127.0.0.1:8000/student/create/
- Détails étudiant : http://127.0.0.1:8000/student/<id>/
- Modification étudiant : http://127.0.0.1:8000/student/<id>/update/
- Dossier académique : http://127.0.0.1:8000/student/<id>/academic-record/
- Tableau de bord étudiant : http://127.0.0.1:8000/student/dashboard/

## 🔐 Système de Permissions
Le projet utilise des décorateurs personnalisés pour gérer efficacement les accès :

@role_required(['admin'])
@role_required(['teacher'])
@role_required(['student'])

Rôles disponibles :
- admin : Accès aux vues réservées aux administrateurs
- teacher : Accès aux vues réservées aux professeurs
- student : Accès aux vues réservées aux étudiants

## ⚙️ Installation

```bash
# 1. Cloner le projet
git clone https://github.com/votreutilisateur/schoolapp.git
cd schoolapp

# 2. Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
# ou
.venv\Scripts\activate       # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer la base de données
# Créer un fichier .env à la racine du projet avec les variables d'environnement

# 5. Appliquer les migrations
python manage.py migrate

# 6. Créer un super utilisateur
python manage.py createsuperuser

# 7. Lancer le serveur
python manage.py runserver
```

## 📝 Contribution

1. Fork le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE.md](LICENSE.md) pour plus de détails.
