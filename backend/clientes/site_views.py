from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from .site_models import SiteSettings
from .site_serializers import SiteSettingsSerializer


class SiteSettingsView(APIView):
    """
    GET: Retorna configurações do site (público)
    PUT/PATCH: Atualiza configurações (apenas admin)
    """
    authentication_classes = [TokenAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    def get_permissions(self):
        # GET é público, PUT/PATCH requer admin
        if self.request.method == 'GET':
            return []
        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request):
        """Retorna configurações atuais do site"""
        settings = SiteSettings.get_settings()
        serializer = SiteSettingsSerializer(settings, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        """Atualiza configurações do site (admin only)"""
        settings = SiteSettings.get_settings()
        serializer = SiteSettingsSerializer(
            settings, 
            data=request.data, 
            partial=True,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Configurações atualizadas com sucesso',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    patch = put  # PATCH usa a mesma lógica do PUT
