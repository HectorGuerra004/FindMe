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
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

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
    
class CompleteProfileSerializer(serializers.Serializer):
    sobre_mi = serializers.CharField(required=False, allow_blank=True)
    educacion = EducationSerializer(many=True, required=False)
    experiencia = ExperienceSerializer(many=True, required=False)
    habilidades = SkillSerializer(many=True, required=False)

    def create(self, validated_data):
        user = self.context['request'].user
        profile = user.profile

        # Actualiza sobre_mi si viene
        if 'sobre_mi' in validated_data:
            profile.sobre_mi = validated_data['sobre_mi']
            profile.save()

        # Crea educación
        educaciones = validated_data.get('educacion', [])
        for edu_data in educaciones:
            Education.objects.create(user=user, **edu_data)

        # Crea experiencia
        experiencias = validated_data.get('experiencia', [])
        for exp_data in experiencias:
            Experience.objects.create(user=user, **exp_data)

        # Crea habilidades
        habilidades = validated_data.get('habilidades', [])
        for skill_data in habilidades:
            Skill.objects.create(user=user, **skill_data)

        return profile