import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from contas.models import Usuario
from voluntarios.models import Voluntario
from tarefas.models import Tarefa
from beneficiarios.models import Beneficiario

class Command(BaseCommand):
    help = 'Populates the database with sample test data for Voluntarios, Tarefas, and Beneficiarios.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate test data...'))

        users_volunteers_data = [
            {'username': 'voluntario_ana', 'password': 'password123', 'email': 'ana.silva@example.com', 
             'first_name': 'Ana', 'last_name': 'Silva', 'cpf': '111.111.111-11', 'rg': '111111111',
             'data_nascimento': datetime.date(1990, 5, 15), 'telefone': '(11) 91111-1111', 'cep': '01001-000', 'logradouro': 'Praça da Sé', 'numero_endereco': '1', 'bairro': 'Sé', 'cidade': 'São Paulo', 'estado': 'SP',
             'areas_interesse': 'Eventos, Arrecadação de fundos', 'disp_sab_m': True, 'disp_dom_t': True},
            {'username': 'voluntario_bruno', 'password': 'password123', 'email': 'bruno.costa@example.com',
             'first_name': 'Bruno', 'last_name': 'Costa', 'cpf': '222.222.222-22', 'rg': '222222222',
             'data_nascimento': datetime.date(1985, 8, 20), 'telefone': '(21) 92222-2222', 'cep': '20040-001', 'logradouro': 'Av. Rio Branco', 'numero_endereco': '100', 'bairro': 'Centro', 'cidade': 'Rio de Janeiro', 'estado': 'RJ',
             'areas_interesse': 'Aulas de reforço, Mentoria', 'disp_ter_n': True, 'disp_qui_n': True},
            {'username': 'voluntaria_carla', 'password': 'password123', 'email': 'carla.dias@example.com',
             'first_name': 'Carla', 'last_name': 'Dias', 'cpf': '555.555.555-55', 'rg': '555555555',
             'data_nascimento': datetime.date(1995, 1, 10), 'telefone': '(31) 95555-5555', 'cep': '30130-001', 'logradouro': 'Av. Afonso Pena', 'numero_endereco': '50', 'bairro': 'Centro', 'cidade': 'Belo Horizonte', 'estado': 'MG',
             'areas_interesse': 'Comunicação, Redes Sociais', 'disp_seg_t': True, 'disp_qua_t': True, 'disp_sex_t': True},
            {'username': 'voluntario_daniel', 'password': 'password123', 'email': 'daniel.lima@example.com',
             'first_name': 'Daniel', 'last_name': 'Lima', 'cpf': '666.666.666-66', 'rg': '666666666',
             'data_nascimento': datetime.date(1980, 12, 1), 'telefone': '(71) 96666-6666', 'cep': '40020-001', 'logradouro': 'Largo do Pelourinho', 'numero_endereco': '20', 'bairro': 'Pelourinho', 'cidade': 'Salvador', 'estado': 'BA',
             'areas_interesse': 'Logística, Organização de Espaços', 'disp_qua_m': True, 'disp_sab_m': True},
            {'username': 'voluntaria_elisa', 'password': 'password123', 'email': 'elisa.rocha@example.com',
             'first_name': 'Elisa', 'last_name': 'Rocha', 'cpf': '777.777.777-77', 'rg': '777777777',
             'data_nascimento': datetime.date(2000, 6, 25), 'telefone': '(41) 97777-7777', 'cep': '80010-001', 'logradouro': 'Rua XV de Novembro', 'numero_endereco': '300', 'bairro': 'Centro', 'cidade': 'Curitiba', 'estado': 'PR',
             'areas_interesse': 'Cuidados com animais, Recepção', 'disp_sex_m': True, 'disp_sex_t': True},
            {'username': 'colaborador_carlos', 'password': 'password123', 'email': 'carlos.adm@example.com',
             'first_name': 'Carlos', 'last_name': 'Pereira', 'tipo_usuario': 'ADMIN'}
        ]

        created_volunteers_objects = [] # Lista para armazenar objetos Voluntario
        created_users_objects = [] # Lista para armazenar objetos Usuario

        for data in users_volunteers_data:
            user, created = Usuario.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data.get('email', f"{data['username']}@example.com"),
                    'first_name': data.get('first_name', data['username'].split('_')[-1].capitalize()),
                    'last_name': data.get('last_name', 'Sobrenome'),
                    'tipo_usuario': data.get('tipo_usuario', 'COLAB') # Padrão para Colaborador
                }
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User "{user.username}" created.'))
            # else:
                # self.stdout.write(self.style.WARNING(f'User "{user.username}" already exists.'))
            created_users_objects.append(user)

            if 'cpf' in data: # Indica que este usuário também é um voluntário
                voluntario_defaults = {
                    'usuario': user,
                    'nome_completo': f"{data['first_name']} {data['last_name']}",
                    'rg': data['rg'],
                    'data_nascimento': data['data_nascimento'],
                    'telefone': data.get('telefone'),
                    'cep': data.get('cep'),
                    'logradouro': data.get('logradouro'),
                    'numero_endereco': data.get('numero_endereco'),
                    'complemento_endereco': data.get('complemento_endereco'),
                    'bairro': data.get('bairro'),
                    'cidade': data.get('cidade'),
                    'estado': data.get('estado'),
                    'areas_interesse': data.get('areas_interesse'),
                    'disp_seg_m': data.get('disp_seg_m', False), 'disp_seg_t': data.get('disp_seg_t', False), 'disp_seg_n': data.get('disp_seg_n', False),
                    'disp_ter_m': data.get('disp_ter_m', False), 'disp_ter_t': data.get('disp_ter_t', False), 'disp_ter_n': data.get('disp_ter_n', False),
                    'disp_qua_m': data.get('disp_qua_m', False), 'disp_qua_t': data.get('disp_qua_t', False), 'disp_qua_n': data.get('disp_qua_n', False),
                    'disp_qui_m': data.get('disp_qui_m', False), 'disp_qui_t': data.get('disp_qui_t', False), 'disp_qui_n': data.get('disp_qui_n', False),
                    'disp_sex_m': data.get('disp_sex_m', False), 'disp_sex_t': data.get('disp_sex_t', False), 'disp_sex_n': data.get('disp_sex_n', False),
                    'disp_sab_m': data.get('disp_sab_m', False), 'disp_sab_t': data.get('disp_sab_t', False), 'disp_sab_n': data.get('disp_sab_n', False),
                    'disp_dom_m': data.get('disp_dom_m', False), 'disp_dom_t': data.get('disp_dom_t', False), 'disp_dom_n': data.get('disp_dom_n', False),
                    'ativo': True
                }
                voluntario, v_created = Voluntario.objects.get_or_create(
                    cpf=data['cpf'], # CPF como chave única para voluntário
                    defaults=voluntario_defaults
                )
                if v_created:
                    self.stdout.write(self.style.SUCCESS(f'Voluntario "{voluntario.nome_completo}" created.'))
                # else:
                    # self.stdout.write(self.style.WARNING(f'Voluntario com CPF "{data["cpf"]}" already exists.'))
                created_volunteers_objects.append(voluntario) # Adiciona à lista mesmo se já existia
        
        # Garante que temos uma lista de voluntários para atribuir às tarefas
        if not created_volunteers_objects: # Se a lista estiver vazia após o loop
            created_volunteers_objects = list(Voluntario.objects.filter(ativo=True)[:5]) # Pega até 5 voluntários ativos
            if not created_volunteers_objects:
                 self.stdout.write(self.style.WARNING('No active volunteers found or created to assign to tasks.'))


        admin_user = Usuario.objects.filter(tipo_usuario='ADMIN').first()
        if not admin_user and created_users_objects: # Se não houver admin, pega o primeiro usuário criado
            admin_user = created_users_objects[0]
        elif not admin_user: # Se ainda não houver admin e nenhum usuário foi criado
            self.stdout.write(self.style.ERROR('No admin user found or created. Tasks might not be assigned "atribuido_por".'))
            # Você pode querer criar um usuário admin padrão aqui se necessário

        tarefas_data = [
            {'titulo': 'Organizar doações de alimentos', 'descricao': 'Separar e catalogar alimentos doados esta semana.', 
             'status': 'PEND', 'prioridade': 3, 'data_prevista_conclusao': timezone.now().date() + datetime.timedelta(days=7),
             'vol_indices': [0] if len(created_volunteers_objects) > 0 else [], 'atribuido_por': admin_user},
            {'titulo': 'Planejar evento de arrecadação', 'descricao': 'Definir data, local e atividades para o próximo evento.',
             'status': 'FAZE', 'prioridade': 4, 'data_prevista_conclusao': timezone.now().date() + datetime.timedelta(days=30),
             'vol_indices': [0, 1] if len(created_volunteers_objects) > 1 else ([0] if len(created_volunteers_objects) > 0 else []), 'atribuido_por': admin_user},
            {'titulo': 'Atualizar site da ONG', 'descricao': 'Publicar novas fotos e notícias no site.',
             'status': 'PEND', 'prioridade': 2,
             'vol_indices': [1] if len(created_volunteers_objects) > 1 else [], 'atribuido_por': admin_user},
            {'titulo': 'Ligar para doadores', 'descricao': 'Agradecer aos doadores recentes pelas contribuições.',
             'status': 'CONC', 'prioridade': 1, 'data_prevista_conclusao': timezone.now().date() - datetime.timedelta(days=2),
             'data_conclusao_efetiva': timezone.now().date() - datetime.timedelta(days=1),
             'vol_indices': [], 'atribuido_por': admin_user},
            {'titulo': 'Preparar material para aula de reforço', 'descricao': 'Criar apostilas e exercícios para as crianças.',
             'status': 'PEND', 'prioridade': 3,
             'vol_indices': [2] if len(created_volunteers_objects) > 2 else ([0] if len(created_volunteers_objects) > 0 else []), 'atribuido_por': admin_user}
        ]

        for data_t in tarefas_data:
            vol_indices_para_atribuir = data_t.pop('vol_indices', [])
            voluntarios_para_tarefa = []
            for index in vol_indices_para_atribuir:
                if index < len(created_volunteers_objects):
                    voluntarios_para_tarefa.append(created_volunteers_objects[index])
            
            # Remover 'voluntario_responsavel' se ainda estiver presente nos defaults
            data_t.pop('voluntario_responsavel', None) 

            tarefa, t_created = Tarefa.objects.get_or_create(
                titulo=data_t['titulo'],
                defaults=data_t
            )
            if t_created:
                if voluntarios_para_tarefa:
                    tarefa.voluntarios_responsaveis.set(voluntarios_para_tarefa)
                self.stdout.write(self.style.SUCCESS(f'Tarefa "{tarefa.titulo}" created.'))
            # else:
                # self.stdout.write(self.style.WARNING(f'Tarefa "{data_t["titulo"]}" already exists.'))

        beneficiarios_data = [
            {
                'nome_completo': 'Maria Oliveira', 'data_nascimento': datetime.date(1975, 3, 22), 
                'genero': 'F', 'cpf': '333.333.333-33', 'rg': '333333333',
                'cep': '20000-001', 'logradouro': 'Rua das Palmeiras', 'numero_endereco': '10', 'bairro': 'Centro', 'cidade': 'Rio de Janeiro', 'estado': 'RJ',
                'telefone_principal': '(21) 93333-3333', 'email': 'maria.oliveira@example.com', 'escolaridade': 'MC'
            },
            {
                'nome_completo': 'João Santos', 'data_nascimento': datetime.date(2010, 7, 10),
                'genero': 'M', 'cpf': '444.444.444-44', 'rg': '444444444',
                'cep': '01000-002', 'logradouro': 'Avenida Principal', 'numero_endereco': '250', 'bairro': 'Sé', 'cidade': 'São Paulo', 'estado': 'SP',
                'telefone_principal': '(11) 94444-4444', 'escolaridade': 'FI'
            },
            {
                'nome_completo': 'Ana Clara Souza', 'data_nascimento': datetime.date(1998, 11, 5),
                'genero': 'F', 'rg': '555666777', # Adicionado RG para Ana Clara
                'logradouro': 'Travessa das Flores', 'numero_endereco': '7B', 'bairro': 'Jardim', 'cidade': 'Belo Horizonte', 'estado': 'MG',
                'email': 'ana.clara@example.com', 'escolaridade': 'SC', 'ocupacao': 'Estudante'
            },
        ]

        for data_b in beneficiarios_data:
            unique_key = {}
            if data_b.get('cpf'):
                unique_key['cpf'] = data_b['cpf']
            else: # Se não tiver CPF, usa nome e data de nascimento como chave composta (menos ideal)
                unique_key['nome_completo'] = data_b['nome_completo']
                unique_key['data_nascimento'] = data_b['data_nascimento']

            # Garante que todos os campos obrigatórios do modelo Beneficiario estejam nos defaults
            # Exemplo: se 'rg' for obrigatório e não estiver em data_b, adicione um valor padrão
            if 'rg' not in data_b and Beneficiario._meta.get_field('rg').blank is False:
                data_b['rg'] = '000000000' # RG fictício padrão

            beneficiario, b_created = Beneficiario.objects.get_or_create(
                **unique_key,
                defaults=data_b
            )
            if b_created:
                self.stdout.write(self.style.SUCCESS(f'Beneficiario "{beneficiario.nome_completo}" created.'))
            # else:
                # self.stdout.write(self.style.WARNING(f'Beneficiario com dados ({unique_key}) already exists.'))

        self.stdout.write(self.style.SUCCESS('Successfully populated test data.'))
