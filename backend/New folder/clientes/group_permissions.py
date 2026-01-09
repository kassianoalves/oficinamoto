from rest_framework.permissions import BasePermission
from rest_framework import status
from rest_framework.response import Response


class IsAdminGroup(BasePermission):
    """Verifica se o usuário está no grupo 'admin'"""
    message = "Você não tem permissão para realizar esta ação. Apenas administradores podem fazer isso."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Superuser sempre tem acesso
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Verificar se está no grupo 'admin'
        return request.user.groups.filter(name__in=['admin', 'Admin', 'ADMIN']).exists()


class HasGroupPermission(BasePermission):
    """Verifica se o usuário pertence a algum grupo"""
    message = "Usuário deve pertencer a um grupo."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        return request.user.groups.exists()


class CanViewOnly(BasePermission):
    """Permite apenas visualizar (GET)"""
    message = "Você só tem permissão para visualizar dados."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Permite GET, HEAD, OPTIONS
        return request.method in ['GET', 'HEAD', 'OPTIONS']


class CanModify(BasePermission):
    """Permite criar, editar e deletar"""
    message = "Você não tem permissão para modificar dados."
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser or request.user.is_staff:
            return True
        
        # Permite todas as operações
        return True

