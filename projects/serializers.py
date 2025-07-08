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
    # This will expose the 'id' of the User object associated with the profile.
    # It will appear as 'user' in your frontend's profileData.user
    user = serializers.PrimaryKeyRelatedField(read_only=True) # Exposes the user's ID

    # This field will calculate the number of likes received by this profile.
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        # Include all necessary fields that your frontend consumes
        # I've added 'user', 'img_profile', 'sobre_mi' and 'likes_count'
        # based on your frontend code and previous discussions.
        fields = [
            'user', # The ID of the User associated with this Profile
            'nombre',
            'apellido',
            'telefono',
            'fecha_nacimiento',
            'ubicacion',
            'img_profile', # Assuming you have this field for the avatar
            'sobre_mi',    # Assuming you have this field for the 'about me' section
            'likes_count', # The new field for the total likes
            # Add any other fields you need for skills, education, experience if they are here
            # or if you have separate serializers for them in a nested structure
        ]
        
        # Keep your extra_kwargs for validation messages
        extra_kwargs = {
            'nombre': {'error_messages': {'required': 'El nombre es obligatorio.', 'blank': 'El nombre no puede estar vacío.'}},
            'apellido': {'error_messages': {'required': 'El apellido es obligatorio.', 'blank': 'El apellido no puede estar vacío.'}},
            'fecha_nacimiento': {'error_messages': {'required': 'La fecha de nacimiento es obligatoria.', 'blank': 'La fecha de nacimiento no puede estar vacía.'}},
        }

    def get_likes_count(self, obj):
        # This method defines how 'likes_count' is calculated.
        # 'obj' is the current Profile instance being serialized.
        # 'likes_received' is the related_name from the 'to_profile' field in your Like model.
        # It counts how many Like objects have this Profile as their 'to_profile'.
        return obj.likes_received.count()

class UserRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Anida el serializer de perfil

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Este correo electrónico ya está registrado.")],
        # Mensaje personalizado para email requerido o inválido
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'blank': 'El correo electrónico no puede estar vacío.',
            'invalid': 'Introduce un correo electrónico válido.'
        }
    )    
    password = serializers.CharField(
        write_only=True,
        min_length=8, # Puedes definir una longitud mínima aquí
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'blank': 'La contraseña no puede estar vacía.',
            'min_length': 'La contraseña debe tener al menos 8 caracteres.' # Mensaje para longitud mínima
        }
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'profile']
        # Podemos añadir mensajes generales para campos no especificados o si faltan por completo
        extra_kwargs = {
            'email': {'required': True}, # Asegurarse de que sea requerido
            'password': {'required': True}, # Asegurarse de que sea requerido
        }


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
    # 'to_profile' will be sent by the client, so it's a writable field.
    # We use PrimaryKeyRelatedField to expect the ID of the Profile.
    to_profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())

    class Meta:
        model = Like
        fields = ['id', 'to_profile', 'fecha_like'] # 'from_profile' is handled in the view
        read_only_fields = ['from_profile', 'fecha_like'] # These fields are set by the server

    def validate(self, data):
        # Get the 'from_profile' from the request context
        # This assumes request.user.profile is available from authentication
        request_user_profile = self.context['request'].user.profile
        to_profile_instance = data.get('to_profile')

        # Prevent liking one's own profile
        if request_user_profile == to_profile_instance:
            raise serializers.ValidationError("You cannot like your own profile.")

        # Check if a like already exists (unique_together handles this at DB level,
        # but pre-checking here can give a more specific error message).
        # This check is more crucial for the 'toggle' logic in the ViewSet,
        # but good to have here for direct POSTs if you allow them.
        if Like.objects.filter(from_profile=request_user_profile, to_profile=to_profile_instance).exists():
            # This validation will only trigger if a direct POST is attempted for an existing like.
            # For the 'toggle_like' action, the action itself handles existence.
            pass # We'll let the ViewSet's toggle_like handle the existence check more directly.

        return data

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
            raise serializers.ValidationError("Clave o correo incorrectos")
        return user
    
class CompleteProfileSerializer(serializers.ModelSerializer):
    educacion = EducationSerializer(many=True, required=False, source='educations')
    experiencia = ExperienceSerializer(many=True, required=False, source='experiences')
    habilidades = SkillSerializer(many=True, required=False, source='skills')
    
    # --- ¡ESTA ES LA LÍNEA NUEVA QUE NECESITAS AÑADIR! ---
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'user', 
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
            'habilidades',
            # --- ¡ESTE ES EL CAMPO NUEVO QUE NECESITAS AÑADIR A LA LISTA! ---
            'likes_count', 
        ]

    # --- ¡ESTE ES EL MÉTODO NUEVO QUE NECESITAS AÑADIR! ---
    def get_likes_count(self, obj):
        # 'obj' es la instancia del modelo Profile actual que se está serializando.
        # 'likes_received' es el related_name del campo 'to_profile' en tu modelo Like.
        return obj.likes_received.count()

    def update(self, instance, validated_data):
        # Asegúrate de que este método 'update' esté correctamente indentado dentro de la clase.
        instance.sobre_mi = validated_data.get('sobre_mi', instance.sobre_mi)
        instance.save()

        educacion_data = validated_data.pop('educations', None)
        if educacion_data is not None:
            instance.educations.all().delete()
            for edu in educacion_data:
                Education.objects.create(profile=instance, **edu)

        experiencia_data = validated_data.pop('experiences', None)
        if experiencia_data is not None:
            instance.experiences.all().delete()
            for exp in experiencia_data:
                Experience.objects.create(profile=instance, **exp)

        habilidades_data = validated_data.pop('skills', None)
        if habilidades_data is not None:
            instance.skills.all().delete()
            for skill in habilidades_data:
                Skill.objects.create(profile=instance, **skill)

        return instance

class ProfileListSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')  # ✅ Necesario para que devuelva el ID del usuario
    titulo = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user_id', 'nombre', 'apellido', 'ubicacion', 'img_profile', 'titulo']

    def get_titulo(self, obj):
        educacion = Education.objects.filter(profile=obj).order_by('id').first()
        return educacion.titulo if educacion else None
