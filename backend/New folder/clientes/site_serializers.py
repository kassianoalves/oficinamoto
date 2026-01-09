from rest_framework import serializers
from .site_models import SiteSettings


class SiteSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteSettings
        fields = ['id', 'site_name', 'logo', 'logo_url', 'updated_at']
        read_only_fields = ['id', 'updated_at']
    
    def get_logo_url(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None
