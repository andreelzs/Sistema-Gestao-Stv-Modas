"""
ASGI config for gestao_stv_modas project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

<<<<<<< HEAD:config/asgi.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestao_stv_modas.settings')
=======
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gerenciamento_ong.settings')
>>>>>>> Do-zero:stv modas teste inteiro ia/GestaoRenatoRodriguesONG-main/GestaoRenatoRodriguesONG-main/gerenciamento_ong/asgi.py

application = get_asgi_application()
