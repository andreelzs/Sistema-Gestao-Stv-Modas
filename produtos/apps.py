from django.apps import AppConfig

class ProdutosConfig(AppConfig):  # ALTERADO DE BeneficiariosConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'produtos'             # ALTERADO DE beneficiarios