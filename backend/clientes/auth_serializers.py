from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import uuid

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Senhas não conferem'})
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Este email já está cadastrado'})
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Este usuário já existe'})
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password')

        if not username and not email:
            raise serializers.ValidationError('Forneça um email ou nome de usuário')

        user = None

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                pass

        if not user and username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError('Usuário ou email não encontrado')

        if not user.check_password(password):
            raise serializers.ValidationError('Senha incorreta')
        data['user'] = user
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email não encontrado')
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        # Gerar token de reset
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # URL de reset
        reset_url = f"http://localhost:5174/reset-password/{uid}/{token}/"
        
        # Enviar email
        subject = 'Recuperação de Senha - Oficina Moto'
        message = f'''
Olá {user.username},

Você solicitou recuperação de senha. Clique no link abaixo para resetar sua senha:

{reset_url}

Este link é válido por 1 hora.

Se você não solicitou isso, ignore este email.

Atenciosamente,
Oficina Moto
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return {'status': 'Email enviado com sucesso'}
        except Exception as e:
            raise serializers.ValidationError(f'Erro ao enviar email: {str(e)}')


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField()
    uid = serializers.CharField()

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password': 'Senhas não conferem'})
        return data

    def save(self):
        try:
            uid = urlsafe_base64_decode(self.validated_data['uid']).decode()
            user = User.objects.get(pk=uid)
            
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, self.validated_data['token']):
                raise serializers.ValidationError('Token inválido ou expirado')
            
            user.set_password(self.validated_data['password'])
            user.save()
            
            return {'status': 'Senha alterada com sucesso'}
        except Exception as e:
            raise serializers.ValidationError(f'Erro: {str(e)}')


class UserSerializer(serializers.ModelSerializer):
    idade = serializers.SerializerMethodField()
    telefone = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'idade', 'telefone', 'avatar']
    
    def get_idade(self, obj):
        try:
            return obj.profile.idade
        except:
            return None
    
    def get_telefone(self, obj):
        try:
            return obj.profile.telefone
        except:
            return ''

    def get_avatar(self, obj):
        try:
            if obj.profile.avatar:
                request = self.context.get('request')
                url = obj.profile.avatar.url
                if request is not None:
                    return request.build_absolute_uri(url)
                return url
        except Exception:
            return None
        return None


class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    last_name = serializers.CharField(required=False, max_length=150, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    idade = serializers.IntegerField(required=False, min_value=1, max_value=150, allow_null=True)
    telefone = serializers.CharField(required=False, max_length=20, allow_blank=True)
    avatar = serializers.ImageField(required=False, allow_null=True)

    def validate_avatar(self, value):
        if value is None:
            return value
        max_size = 3 * 1024 * 1024  # 3MB
        try:
            if value.size > max_size:
                raise serializers.ValidationError('Imagem muito grande. Limite: 3MB')
            if hasattr(value, 'content_type') and value.content_type:
                if not value.content_type.startswith('image/'):
                    raise serializers.ValidationError('Arquivo inválido. Envie uma imagem.')
        except Exception:
            # Falha ao ler tamanho/tipo, prossegue com cautela
            pass
        return value
    
    def validate_email(self, value):
        if not value:  # Se está vazio, não valida
            return value
        user = self.context.get('request').user
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError('Este email já está em uso')
        return value
    
    def update(self, instance, validated_data):
        try:
            idade = validated_data.pop('idade', None)
            telefone = validated_data.pop('telefone', None)
            avatar = validated_data.pop('avatar', None)
            
            # Atualizar campos do usuário
            if 'first_name' in validated_data:
                instance.first_name = validated_data.get('first_name', '')
            if 'last_name' in validated_data:
                instance.last_name = validated_data.get('last_name', '')
            if 'email' in validated_data:
                instance.email = validated_data.get('email', '')
            
            instance.save()
            
            # Atualizar profile
            from .models import UserProfile
            
            try:
                profile = instance.profile
            except UserProfile.DoesNotExist:
                # Se não existir profile, cria um
                profile = UserProfile.objects.create(user=instance)
            
            if idade is not None:
                profile.idade = idade
            if telefone is not None:
                profile.telefone = telefone
            if avatar is not None:
                profile.avatar = avatar
            
            profile.save()
            
            return instance
        except Exception as e:
            raise serializers.ValidationError(f'Erro ao atualizar perfil: {str(e)}')
