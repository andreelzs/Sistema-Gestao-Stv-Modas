# Sistema de Gerenciamento para ONG Renato Rodrigues

Este projeto é um sistema de gerenciamento desenvolvido para a ONG Renato Rodrigues, com o objetivo de auxiliar na organização de voluntários, beneficiários, tarefas e outras atividades da organização.

## Funcionalidades Principais

O sistema é modularizado e conta com as seguintes funcionalidades principais:

*   **Core (`core`)**: Funcionalidades centrais e páginas estáticas, como a página inicial e a base para os templates.
*   **Contas (`contas`)**: Gerenciamento de usuários e autenticação no sistema. Utiliza um modelo de usuário personalizado.
*   **Voluntários (`voluntarios`)**: Cadastro e gerenciamento de informações dos voluntários da ONG.
*   **Beneficiários (`beneficiarios`)**: Cadastro e gerenciamento de informações dos beneficiários atendidos pela ONG.
*   **Tarefas (`tarefas`)**: Criação, atribuição e acompanhamento de tarefas para os voluntários.
*   **Dashboard (`dashboard`)**: Painel com visões gerais e estatísticas relevantes para a gestão da ONG.

## Tecnologias Utilizadas

*   **Backend**:
    *   Python 3.x
    *   Django 4.2.9
*   **Frontend**:
    *   HTML
    *   CSS
    *   JavaScript (implícito pelo Django e possíveis bibliotecas)
*   **Banco de Dados**:
    *   SQLite3 (configuração padrão de desenvolvimento)
*   **Principais Bibliotecas Python (do `requirements.txt`)**:
    *   `asgiref`
    *   `crispy-bootstrap5`
    *   `Django`
    *   `django-cors-headers`
    *   `django-crispy-forms`
    *   `django-debug-toolbar` (para desenvolvimento)
    *   `django-extensions`
    *   `django-filter`
    *   `django-import-export`
    *   `django-tables2`
    *   `django-widget-tweaks`
    *   `psycopg2-binary` (sugere que PostgreSQL pode ser usado em produção)
    *   `python-dotenv`
    *   `whitenoise` (para servir arquivos estáticos)

## Aprendizados Aplicados e Conceitos Chave

Este projeto serviu como uma plataforma para aplicar e consolidar diversos conceitos importantes do desenvolvimento web com Django, incluindo:

*   **Arquitetura MVT (Model-View-Template)**: Organização do código seguindo o padrão de design do Django, separando a lógica de dados (Models), a lógica de apresentação (Templates) e a lógica de negócios/controle (Views).
*   **ORM do Django**: Utilização do Object-Relational Mapper para interagir com o banco de dados de forma pythonica, abstraindo consultas SQL complexas. Isso inclui a definição de modelos, relacionamentos (ForeignKey, ManyToManyField), e a execução de queries.
*   **Sistema de Templates**: Criação de interfaces dinâmicas utilizando a linguagem de templates do Django, incluindo herança de templates (`{% extends %}`), inclusão de trechos (`{% include %}`), tags e filtros.
*   **Formulários Django**: Implementação de formulários para entrada de dados, utilizando `ModelForm` para criar formulários a partir de modelos, e bibliotecas como `django-crispy-forms` e `crispy-bootstrap5` para estilização e renderização facilitada com Bootstrap.
*   **Autenticação e Autorização**: Implementação de um sistema de login e gerenciamento de usuários, utilizando o sistema de autenticação embutido do Django e um modelo de usuário personalizado (`contas.Usuario`).
*   **Desenvolvimento Modular com Apps**: Estruturação do projeto em aplicações Django reutilizáveis e independentes (`voluntarios`, `tarefas`, `beneficiarios`, etc.), promovendo uma melhor organização e manutenibilidade do código.
*   **Migrações de Banco de Dados**: Gerenciamento da evolução do esquema do banco de dados de forma controlada e versionada através do sistema de migrações do Django.
*   **Gerenciamento de Arquivos Estáticos**: Configuração e uso de `whitenoise` para servir arquivos estáticos (CSS, JavaScript, imagens) de forma eficiente, especialmente em ambientes de produção.
*   **Boas Práticas de Desenvolvimento**:
    *   Uso de ambientes virtuais (`venv`) para isolamento de dependências.
    *   Gerenciamento de dependências com `pip` e `requirements.txt`.
    *   Configuração de `SECRET_KEY` e `DEBUG` para ambientes de desenvolvimento e produção.
*   **Configurações para Deploy**: Considerações iniciais para o deploy da aplicação, como a configuração de `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS`.

## Pré-requisitos

Antes de começar, garanta que você tem os seguintes softwares instalados:

*   Python (versão 3.x recomendada)
*   pip (gerenciador de pacotes Python)
*   Git (para clonar o repositório, opcional se você já tem os arquivos)

## Instruções de Instalação e Configuração

1.  **Clone o Repositório (se aplicável):**
    ```bash
    git clone <URL_DO_REPOSITORIO>
    cd gerenciamento_ong # ou o nome da pasta raiz do projeto
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.
    ```bash
    python -m venv venv
    # No Windows
    .\venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as Dependências:**
    Com o ambiente virtual ativado, instale todas as dependências listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Aplique as Migrações do Banco de Dados:**
    As migrações criam as tabelas necessárias no banco de dados.
    ```bash
    python manage.py migrate
    ```

5.  **Crie um Superusuário (Administrador):**
    Isso permitirá que você acesse a interface de administração do Django.
    ```bash
    python manage.py createsuperuser
    ```
    Siga as instruções para definir nome de usuário, email e senha.

## Como Executar o Projeto

Após a instalação e configuração, você pode iniciar o servidor de desenvolvimento do Django:

```bash
python manage.py runserver
