# SoftDesk

Cette API permet de lister les projets en cours de développement. Des contributeurs y sont associés ainsi que les problèmes
rencontrés. Des commentaires permettent d'assurer le suivi de résolution des problèmes.

## Installation et lancement

```bash
$ https://github.com/TheHarryPop/SoftDesk.git
$ cd SoftDesk
$ python3 -m venv env (Sous Windows => python -m venv env)
$ source env/bin/activate (Sous Windows => env\Scripts\activate)
$ pip install -r requirements.txt
$ cd LITReview
$ python manage.py runserver
```

## Endpoints

Ci dessous une liste des endpoints disponibles. La documentation Postman les présente en détail.

http://127.0.0.1:8000/api/login/
http://127.0.0.1:8000/api/register/
http://127.0.0.1:8000/api/projects/
http://127.0.0.1:8000/api/projects/{{project_id}}/
http://127.0.0.1:8000/api/projects/{{project_id}}/users/
http://127.0.0.1:8000/api/projects/{{project_id}}/users/{{user_id}}/
http://127.0.0.1:8000/api/projects/{{project_id}}/issues/
http://127.0.0.1:8000/api/projects/{{project_id}}/issues/{{issue_id}}/
http://127.0.0.1:8000/api/projects/{{project_id}}/issues/{{issue_id}}/comments/
http://127.0.0.1:8000/api/projects/{{project_id}}/issues/{{issue_id}}/comments/{{comment_id}}/


## Documentation

La documentation Postman est disponible à cette adresse :

https://documenter.getpostman.com/view/19052717/UVXgLx91


## Profils test

SuperUser : admin

Mot de passe : 1234

Nom d'utilisateur : quentin

Mot de passe : 1234azert

Nom d'utilisateur : cassandre

Mot de passe : 1234azert

