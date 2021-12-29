from django.db import models

from django.conf import settings


class Users(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user', null=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    password = models.CharField(max_length=150, blank=True)


class Projects(models.Model):
    class Type(models.TextChoices):
        BAC = 'BACK-END', 'BACK-END'
        FRO = 'FRONT-END', 'FRONT-END'
        IOS = 'IOS', 'IOS'
        AND = 'ANDROID', 'ANDROID'

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    type = models.CharField(max_length=9, choices=Type.choices, default=Type.BAC)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='project_author', null=True)


class Contributors(models.Model):
    class Meta:
        unique_together = ['user', 'project']

    class Role(models.TextChoices):
        AUT = 'AUTHOR', 'AUTHOR'
        CONT = 'CONTRIBUTOR', 'CONTRIBUTOR'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='contributor_project', null=True)
    permission = models.CharField(max_length=64, null=True)
    role = models.CharField(max_length=64, choices=Role.choices, default=Role.CONT)


class Issues(models.Model):

    class Priority(models.TextChoices):
        FAI = '1', 'FAIBLE'
        MOY = '2', 'MOYENNE'
        ELE = '3', 'ÉLEVÉE'

    class Tag(models.TextChoices):
        BUG = '1', 'BUG'
        AME = '2', 'AMÉLIORATION'
        TAC = '3', 'TÂCHE'

    title = models.CharField(max_length=128)
    desc = models.CharField(max_length=2048)
    tag = models.CharField(max_length=12, choices=Tag.choices, default=Tag.BUG)
    priority = models.CharField(max_length=7, choices=Priority.choices, default=Priority.FAI)
    project = models.ForeignKey(to=Projects, on_delete=models.CASCADE, related_name='issue_project', null=True)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='issue_author', null=True)
    assignee_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='issue_assigned', null=True)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    comment_id = models.IntegerField
    description = models.CharField(max_length=2048)
    author_user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='comment_author')
    issue = models.ForeignKey(to=Issues, on_delete=models.CASCADE, related_name='comment_issue')
    created_time = models.DateTimeField(auto_now_add=True)
