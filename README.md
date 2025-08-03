Stryn
Back-end do projeto Stryn, uma aplicação Django que fornece uma API RESTful para gerenciamento de pedidos, pagamentos e e-mails, integrada com serviços como Stripe, ASAAS e AWS S3 (opcional). Este projeto utiliza Python 3.12.11, PostgreSQL como banco de dados em produção, e é configurado para deploy no Railway com Nixpacks e Gunicorn.
Estrutura do Projeto

Arquivos Principais:

requirements.txt: Inclui as dependências principais, referenciando requirements-dev.txt e adicionando o gunicorn para produção.
requirements-dev.txt: Lista todas as dependências do projeto, incluindo Django, Django REST Framework, Djoser, e bibliotecas para integrações como Stripe e AWS S3.
nixpacks.toml: Configura o ambiente de build no Railway, especificando pacotes Nix (como Python 3.12 e PostgreSQL), comandos de instalação e inicialização com Gunicorn.
Procfile: Define o comando para rodar o servidor web com Gunicorn no Railway (web: gunicorn stryn.wsgi).
settings.py: Configurações do Django, incluindo INSTALLED_APPS (com apps personalizados como core, pagamentos, pedidos, emails), middlewares, autenticação via JWT, e configurações para banco de dados, CORS, e-mails e storage.
.env: Contém variáveis de ambiente sensíveis, como SECRET_KEY, DATABASE_URL, chaves do Stripe, e configurações de e-mail. Não versionado (ignorado pelo .gitignore).
.gitignore: Ignora arquivos desnecessários, como bancos SQLite, arquivos de cache Python, e o arquivo .env.


Apps Personalizados:

core, pagamentos, pedidos, emails: Contêm a lógica principal do aplicativo, incluindo modelos, views e endpoints da API.
Integrações com django-rest-framework, djoser, rest_framework_simplejwt para autenticação, e drf-spectacular para documentação da API.


Integrações:

Banco de Dados: PostgreSQL no Railway, configurado via DATABASE_URL.
Autenticação: Suporte a login por username ou e-mail com JWT (rest_framework_simplejwt).
Pagamentos: Integração com Stripe e ASAAS para processamento de pagamentos.
E-mails: Configuração SMTP para envio de e-mails (ex.: redefinição de senha).
Storage: Suporte opcional a AWS S3 para arquivos estáticos e de mídia (controlado pela variável USE_AWS).


Ambiente de Produção:

Deploy no Railway com Nixpacks para build e Gunicorn como servidor WSGI.
Banco de dados PostgreSQL hospedado como serviço separado no Railway.
Variáveis de ambiente configuradas no painel do Railway.



1. Rodar o Projeto Localmente
Para desenvolvimento local, siga os passos abaixo para configurar e executar o projeto em sua máquina.
Pré-requisitos

Python 3.12.11 instalado.
Git instalado.
Um banco de dados local (SQLite para testes ou PostgreSQL para desenvolvimento mais próximo da produção).
Ferramentas como Postman ou curl para testar a API (opcional).

Passos

Clone o repositório:
git clone git@github.com:s-m-kawase/stryn-back-end.git
cd stryn-back-end


Crie e ative um ambiente virtual:

Fora da pasta raiz do projeto, crie um ambiente virtual:# Linux/MacOS
python3 -m venv venv
. venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate




Instale as dependências:
pip install -r requirements-dev.txt


Nota: Se houver erro com o psycopg2-binary (necessário para PostgreSQL), instale-o separadamente:pip install psycopg2-binary


Certifique-se de ter o libpq-dev instalado no sistema para compilar o psycopg2 (ex.: sudo apt-get install libpq-dev no Ubuntu).


Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto com base no .env.example:SECRET_KEY=seu_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3  # ou postgresql://user:password@localhost:5432/dbname para PostgreSQL
EMAIL_HOST_USER=seu_email
EMAIL_HOST_PASSWORD=sua_senha
STRIPE_SECRET_KEY=sua_chave
STRIPE_PUBLISHABLE_KEY=sua_chave
STRIPE_WEBHOOK_SECRET=sua_chave
STRIPE_PRICE_ID=sua_chave
ASAAS_API_KEY=sua_chave
ASAAS_ENVIRONMENT=production
ASAAS_WEBHOOK_SECRET=sua_chave
DOMAIN_FRONT=http://localhost:9000  # URL do front-end local
USE_AWS=False
AWS_ACCESS_KEY_ID=sua_chave
AWS_SECRET_ACCESS_KEY=sua_chave
AWS_STORAGE_BUCKET_NAME=seu_bucket


Para desenvolvimento local com SQLite, use DATABASE_URL=sqlite:///db.sqlite3. Para PostgreSQL, configure um banco local e use o formato postgresql://user:password@localhost:5432/dbname.


Aplique as migrações do banco de dados:
python3 manage.py migrate


Crie um superusuário (para acessar o painel admin /admin/):
python3 manage.py createsuperuser


Siga as instruções para definir username, e-mail e senha.


Rode o servidor de desenvolvimento:
python3 manage.py runserver


Acesse a aplicação em http://localhost:8000.
O painel admin está em http://localhost:8000/admin/.
A documentação da API (via drf-spectacular) está em http://localhost:8000/api/schema/.


Teste a aplicação:

Use Postman ou um navegador para testar endpoints da API.
Verifique o CORS para o front-end (configurado para http://localhost:9000 por padrão no settings.py).
Teste integrações como Stripe e envio de e-mails localmente, se configurado.



2. Rodar o Projeto no Railway
O projeto está configurado para deploy automático no Railway, utilizando Nixpacks para o ambiente de build e Gunicorn como servidor WSGI. O banco de dados é um serviço PostgreSQL separado no Railway.
Pré-requisitos

Conta no Railway (https://railway.app).
Repositório GitHub conectado ao Railway (s-m-kawase/stryn-back-end).
Acesso ao painel do Railway para configurar variáveis de ambiente.

Passos

Configure o projeto no Railway:

Crie um novo projeto no Railway.
Conecte o repositório GitHub (s-m-kawase/stryn-back-end) ao projeto.
Adicione um serviço PostgreSQL no Railway:
No painel do Railway, clique em "New Service" > "Database" > "PostgreSQL".
O Railway gerará automaticamente uma variável DATABASE_URL para o serviço.


Adicione as variáveis de ambiente no painel do Railway (aba "Variables"):
Copie as variáveis do arquivo .env (ex.: SECRET_KEY, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, STRIPE_SECRET_KEY, etc.).
Certifique-se de que DATABASE_URL está configurado com o valor fornecido pelo serviço PostgreSQL.
Defina DEBUG=False para produção.
Configure DOMAIN_FRONT com a URL do front-end (ex.: https://seu-front-no-netlify-ou-dominio.com).
Se usar AWS S3, defina USE_AWS=True e configure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, e AWS_STORAGE_BUCKET_NAME.




Deploy automático:

O Railway iniciará o deploy automaticamente após cada push no branch principal do GitHub.
O arquivo nixpacks.toml configura o ambiente com Python 3.12, PostgreSQL, e dependências necessárias, instalando as dependências do requirements.txt e executando python manage.py collectstatic --noinput.
O servidor é iniciado com:gunicorn stryn.wsgi:application --bind 0.0.0.0:${PORT} --workers=3 --timeout=180 --log-file -




Aplique as migrações:

Após o deploy, as migrações do banco de dados não são executadas automaticamente. Execute-as manualmente:
Opção 1: Console do Railway:
No painel do Railway, vá até o serviço do aplicativo, abra o console (aba "Deployments" ou "Logs"), e execute:python3 manage.py migrate




Opção 2: Railway CLI:
Instale a Railway CLI (npm install -g @railway/cli).
Conecte-se ao projeto com `railway