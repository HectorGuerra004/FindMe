from rest_framework import serializers
from .models import User, Profile, Portfolio, Education, Experience, Skill, Like, Petition
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_active', 'is_admin', 'fecha_registro']
        extra_kwargs = {'password': {'write_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ['user']  # Excluye 'user' porque se asigna en el registro

class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Anida el serializer de perfil

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este correo electrónico ya está registrado.")]
    )    
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        exclude = ['profile']  # ✅ no 'user'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ['empresa', 'puesto', 'ubicacion_exp', 'inicio_exp', 'fin_exp']
        extra_kwargs = {
            'ubicacion_exp': {'required': False, 'allow_null': True, 'allow_blank': True},
            'inicio_exp': {'required': False, 'allow_null': True},
            'fin_exp': {'required': False, 'allow_null': True},
        }


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        exclude = ['profile']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class PetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Petition
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Credenciales inválidas")
        return user
    
class CompleteProfileSerializer(serializers.ModelSerializer):
    educacion = EducationSerializer(many=True, required=False, source='educations')
    experiencia = ExperienceSerializer(many=True, required=False, source='experiences')
    habilidades = SkillSerializer(many=True, required=False, source='skills')

    class Meta:
        model = Profile
        fields = [
            'nombre',
            'apellido',
            'img_profile',
            'biografia',
            'ubicacion',
            'telefono',
            'fecha_nacimiento',
            'sobre_mi',
            'educacion',
            'experiencia',
            'habilidades'
        ]

    def update(self, instance, validated_data):
        # Actualizar campo simple
        instance.sobre_mi = validated_data.get('sobre_mi', instance.sobre_mi)
        instance.save()

        # Actualizar educacion
        educacion_data = validated_data.pop('educations', None)
        if educacion_data is not None:
            # Para simplicidad, eliminar todo y volver a crear
            instance.educations.all().delete()
            for edu in educacion_data:
                Education.objects.create(profile=instance, **edu)

        # Actualizar experiencia
        experiencia_data = validated_data.pop('experiences', None)
        if experiencia_data is not None:
            instance.experiences.all().delete()
            for exp in experiencia_data:
                Experience.objects.create(profile=instance, **exp)

        # Actualizar habilidades
        habilidades_data = validated_data.pop('skills', None)
        if habilidades_data is not None:
            instance.skills.all().delete()
            for skill in habilidades_data:
                Skill.objects.create(profile=instance, **skill)

        return instance