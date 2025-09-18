from django.apps import AppConfig

class ClientesConfig(AppConfig):  # ALTERADO DE VoluntariosConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clientes'             # ALTERADO DE voluntarios