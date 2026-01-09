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
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise serializers.ValidationError('Senha incorreta')
        except User.DoesNotExist:
            raise serializers.ValidationError('Email não encontrado')
        
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
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
