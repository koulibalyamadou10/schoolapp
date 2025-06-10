# 🏫 SchoolApp – Système de Gestion Scolaire

Ce projet est un système de gestion scolaire développé avec Django et MySQL, permettant de gérer les utilisateurs (administrateurs, enseignants, étudiants), les matières, et les notes.

---

## 🚀 Fonctionnalités

- Authentification sécurisée (avec rôles : admin, enseignant, étudiant)
- Gestion des étudiants
- Gestion des enseignants
- Gestion des matières
- Attribution et consultation des notes
- Interfaces distinctes selon les rôles

---

## 🧱 Technologies

- **Framework** : Django 4+
- **Langage** : Python 3.10+
- **Base de données** : MySQL
- **ORM** : Django ORM
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

---

## 🌐 URLs du projet
Après avoir lancé le serveur, vous pouvez accéder aux différentes interfaces :

Connexion : http://127.0.0.1:8000/account/login/

Inscription : http://127.0.0.1:8000/account/register/

Tableau de bord Admin : http://127.0.0.1:8000/account/admin-dashboard/

Tableau de bord Enseignant : http://127.0.0.1:8000/account/teacher-dashboard/

Tableau de bord Étudiant : http://127.0.0.1:8000/account/student-dashboard/

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

# 4. Créer un fichier .env a la racine du projet et coller le contenu     'default': {

# 6. Lancer le serveur
python manage.py runserver
