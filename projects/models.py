from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
    def authenticate(self, email=None, password=None):
        user = self.get(email=email)
        if user and user.check_password(password):
            return user
        return None

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    img_profile = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    biografia = models.CharField(max_length=255, blank=True, null=True)
    ubicacion = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}" if self.nombre else self.user.email

class Portfolio(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True)
    archivo = models.FileField(upload_to='portfolio_files/', blank=True, null=True)
    descripcion_archivo = models.CharField(max_length=255, blank=True, null=True)

class Education(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    institucion = models.CharField(max_length=150, blank=True, null=True)
    titulo = models.CharField(max_length=150, blank=True, null=True)
    campo_estudio = models.CharField(max_length=150, blank=True, null=True)

class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    empresa = models.CharField(max_length=150, blank=True, null=True)
    puesto = models.CharField(max_length=150, blank=True, null=True)
    ubicacion_exp = models.CharField(max_length=150, blank=True, null=True)
    inicio_exp = models.DateField(blank=True, null=True)
    fin_exp = models.DateField(blank=True, null=True)

class Skill(models.Model):
    LEVEL_CHOICES = [
        ('Básico', 'Básico'),
        ('Intermedio', 'Intermedio'),
        ('Avanzado', 'Avanzado'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='skills')
    nombre_skill = models.CharField(max_length=100, blank=True, null=True)
    nivel = models.CharField(max_length=10, choices=LEVEL_CHOICES, blank=True, null=True)

class Like(models.Model):
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_sent')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='likes_received')
    fecha_like = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_profile', 'to_profile')

class Petition(models.Model):
    from_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='petitions_sent')
    to_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='petitions_received')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)