from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class UserManager(BaseUserManager):
    def create_user(self, id, team, email, password, part, name):

        if not id:
            raise ValueError('Users must have a id')

        if not team:
            raise ValueError('Users require a team')

        if not email:
            raise ValueError('Users require an email')

        user = self.model(
            id=id,
            team=team,
            email=email,
            part=part,
            name=name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    vote_num = models.IntegerField(default=0)


class User(AbstractBaseUser):
    id = models.CharField(max_length=10, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, unique=True)
    password = models.CharField(max_length=30)
    part = models.CharField(max_length=10)
    name = models.CharField(max_length=10)
    part_voted = models.BooleanField(default=False)
    demo_voted = models.BooleanField(default=False)
    vote_num = models.IntegerField(default=0)

    objects = UserManager()
    USERNAME_FIELD = 'id'

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.id
