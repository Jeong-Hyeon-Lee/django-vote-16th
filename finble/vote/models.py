from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, id, team, email, part, name, password, **extra_fields):
        if not id:
            raise ValueError('Users must have an id')
        if not team:
            raise ValueError('Users require a team')
        if not email:
            raise ValueError('Users require an email')
        if not part:
            raise ValueError('Users require a part')
        if not name:
            raise ValueError('Users require a name')
        email = self.normalize_email(email)
        user = self.model(self, id=id, team=team, email=email, part=part, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, id, team, email, part, name, password=None, **extra_fields):
        return self._create_user(self, id, team, email, part, name, password, **extra_fields)

    # def create_superuser(self, id, team, email, part, name, password, **extra_fields):
    #     user = self.create_user(
    #         id=id,
    #         team=team,
    #         email=email,
    #         part=part,
    #         name=name,
    #         password=password,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user


class Team(models.Model):
    TEAM_CHOICES = {
        ('teample', 'Teample'),
        ('finble', 'Finble'),
        ('prefolio', 'Pre:folio'),
        ('diametes', 'diaMEtes'),
        ('recipeasy', 'recipeasy'),
    }
    name = models.CharField(max_length=20, choices=TEAM_CHOICES)
    description = models.CharField(max_length=200, default=None)
    vote_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    PART_CHOICES = {
        ('front', 'Front-end'),
        ('back', 'Back-end'),
        ('design', 'Design'),
        ('plan', 'Plan')
    }
    name = models.CharField(max_length=20)
    part = models.CharField(max_length=10, choices=PART_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    vote_num = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    PART_CHOICES = {
        ('front', 'Front-end'),
        ('back', 'Back-end'),
        ('design', 'Design'),
        ('plan', 'Plan')
    }
    id = models.CharField(max_length=10, primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, unique=True)
    part = models.CharField(max_length=10, choices=PART_CHOICES)
    name = models.CharField(max_length=10)
    part_voted = models.BooleanField(default=False)
    demo_voted = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['team', 'email', 'part', 'name', ]

    def __str__(self):
        return self.name
