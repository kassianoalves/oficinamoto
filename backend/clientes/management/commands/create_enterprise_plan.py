from django.core.management.base import BaseCommand
from clientes.models import Plan

class Command(BaseCommand):
    help = 'Cria o plano Enterprise'

    def handle(self, *args, **options):
        # Criar plano Enterprise
        enterprise_plan, created = Plan.objects.get_or_create(
            name='enterprise',
            defaults={
                'price': 499.90,
                'max_clientes': 999999,
                'max_motos': 999999,
                'max_agendamentos': 999999,
                'has_app_mobile': True,
                'has_whatsapp': True,
                'has_lembretes': True,
                'has_fornecedores': True,
                'has_chat_suporte': True,
                'has_backup_nuvem': True,
                'has_ia_diagnostico': True,
                'has_plano_fidelidade': True,
                'has_agendamentos_prioritarios': True,
                'has_loja': True,
                'has_imagem_3d': True,
                'has_manuais': True,
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('✅ Plano Enterprise criado com sucesso!'))
        else:
            self.stdout.write(self.style.WARNING('✅ Plano Enterprise já existe'))

        self.stdout.write("\n=== Planos Cadastrados ===\n")
        for plan in Plan.objects.all().order_by('price'):
            resources = []
            if plan.has_loja:
                resources.append("🛍️ Loja")
            if plan.has_imagem_3d:
                resources.append("🎨 3D")
            if plan.has_manuais:
                resources.append("📚 Manuais")
            
            resources_text = f" + {', '.join(resources)}" if resources else ""
            self.stdout.write(f"\n{plan.name.upper()}: R$ {plan.price}")
            self.stdout.write(f"  Limites: {plan.max_clientes} clientes{resources_text}")
