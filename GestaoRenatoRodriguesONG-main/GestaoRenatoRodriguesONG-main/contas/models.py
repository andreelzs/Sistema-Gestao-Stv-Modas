from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    TIPOS_USUARIO = [
        ('ADMIN', 'Administrador'),
        ('VOLUNT', 'Voluntário'),
    ]
    tipo_usuario = models.CharField(
        max_length=6, 
        choices=TIPOS_USUARIO,
        default='VOLUNT',
        verbose_name='Tipo de Usuário'
    )

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='grupos',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence. Um usuário receberá todas as permissões concedidas a cada um de seus grupos.',
        related_name="usuario_set_contas",  # Nome único para related_name
        related_query_name="usuario_contas",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='permissões do usuário',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        related_name="usuario_set_contas_perm",  # Nome único para related_name
        related_query_name="usuario_contas_perm",
    )

    def __str__(self):
        return self.username
