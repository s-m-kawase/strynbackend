# Stryn

Back-end do projeto Stryn, uma aplicação Django que fornece uma API RESTful para gerenciamento de pedidos, pagamentos e e-mails, integrada com serviços como Stripe, ASAAS e AWS S3 (opcional). Este projeto utiliza Python 3.12.11, PostgreSQL como banco de dados em produção, e é configurado para deploy no Railway com Nixpacks e Gunicorn.

## Estrutura do Projeto

- **Arquivos Principais**:
  - `requirements.txt`: Inclui as dependências principais, referenciando `requirements-dev.txt` e adicionando o `gunicorn` para produção.
  - `requirements-dev.txt`: Lista todas as dependências do projeto, incluindo Django, Django REST Framework, Djoser, e bibliotecas para integrações como Stripe e AWS S3.
  - `nixpacks.toml`: Configura o ambiente de build no Railway, especificando pacotes Nix (como Python 3.12 e PostgreSQL), comandos de instalação e inicialização com Gunicorn.
  - `Procfile`: Define o comando para rodar o servidor web com Gunicorn no Railway (`web: gunicorn stryn.wsgi`).
  - `settings.py`: Configurações do Django, incluindo `INSTALLED_APPS` (com apps personalizados como `core`, `pagamentos`, `pedidos`, `emails`), middlewares, autenticação via JWT, e configurações para banco de dados, CORS, e-mails e storage.
  - `.env`: Contém variáveis de ambiente sensíveis, como `SECRET_KEY`, `DATABASE_URL`, chaves do Stripe, e configurações de e-mail. Não versionado (ignorado pelo `.gitignore`).
  - `.gitignore`: Ignora arquivos desnecessários, como bancos SQLite, arquivos de cache Python, e o arquivo `.env`.

- **Apps Personalizados**:
  - `core`, `pagamentos`, `pedidos`, `emails`: Contêm a lógica principal do aplicativo, incluindo modelos, views e endpoints da API.
  - Integrações com `django-rest-framework`, `djoser`, `rest_framework_simplejwt` para autenticação, e `drf-spectacular` para documentação da API.

- **Integrações**:
  - **Banco de Dados**: PostgreSQL no Railway, configurado via `DATABASE_URL`.
  - **Autenticação**: Suporte a login por username ou e-mail com JWT (`rest_framework_simplejwt`).
  - **Pagamentos**: Integração com Stripe e ASAAS para processamento de pagamentos.
  - **E-mails**: Configuração SMTP para envio de e-mails (ex.: redefinição de senha).
  - **Storage**: Suporte opcional a AWS S3 para arquivos estáticos e de mídia (controlado pela variável `USE_AWS`).

- **Ambiente de Produção**:
  - Deploy no Railway com Nixpacks para build e Gunicorn como servidor WSGI.
  - Banco de dados PostgreSQL hospedado como serviço separado no Railway.
  - Variáveis de ambiente configuradas no painel do Railway.

## 1. Rodar o Projeto Localmente

Para desenvolvimento local, siga os passos abaixo para configurar e executar o projeto em sua máquina.

### Pré-requisitos
- Python 3.12.11 instalado.
- Git instalado.
- Um banco de dados local (SQLite para testes ou PostgreSQL para desenvolvimento mais próximo da produção).
- Ferramentas como Postman ou curl para testar a API (opcional).

### Passos
1. **Clone o repositório**:
   ```bash
   git clone git@github.com:s-m-kawase/stryn-back-end.git
   cd stryn-back-end
   ```

2. **Crie e ative um ambiente virtual**:
   - Fora da pasta raiz do projeto, crie um ambiente virtual:
     ```bash
     # Linux/MacOS
     python3 -m venv venv
     . venv/bin/activate

     # Windows
     python -m venv venv
     .\venv\Scripts\activate
     ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements-dev.txt
   ```
   - **Nota**: Se houver erro com o `psycopg2-binary` (necessário para PostgreSQL), instale-o separadamente:
     ```bash
     pip install psycopg2-binary
     ```
   - Certifique-se de ter o `libpq-dev` instalado no sistema para compilar o `psycopg2` (ex.: `sudo apt-get install libpq-dev` no Ubuntu).

4. **Configure as variáveis de ambiente**:
   - Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:
     ```env
     SECRET_KEY=seu_secret_key
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
     ```
   - Para desenvolvimento local com SQLite, use `DATABASE_URL=sqlite:///db.sqlite3`. Para PostgreSQL, configure um banco local e use o formato `postgresql://user:password@localhost:5432/dbname`.

5. **Aplique as migrações do banco de dados**:
   ```bash
   python3 manage.py migrate
   ```

6. **Crie um superusuário** (para acessar o painel admin `/admin/`):
   ```bash
   python3 manage.py createsuperuser
   ```
   - Siga as instruções para definir username, e-mail e senha.

7. **Rode o servidor de desenvolvimento**:
   ```bash
   python3 manage.py runserver
   ```
   - Acesse a aplicação em `http://localhost:8000`.
   - O painel admin está em `http://localhost:8000/admin/`.
   - A documentação da API (via `drf-spectacular`) está em `http://localhost:8000/api/schema/`.

8. **Teste a aplicação**:
   - Use Postman ou um navegador para testar endpoints da API.
   - Verifique o CORS para o front-end (configurado para `http://localhost:9000` por padrão no `settings.py`).
   - Teste integrações como Stripe e envio de e-mails localmente, se configurado.

## 2. Rodar o Projeto no Railway

O projeto está configurado para deploy automático no Railway, utilizando Nixpacks para o ambiente de build e Gunicorn como servidor WSGI. O banco de dados é um serviço PostgreSQL separado no Railway.

### Pré-requisitos
- Conta no Railway (https://railway.app).
- Repositório GitHub conectado ao Railway (`s-m-kawase/stryn-back-end`).
- Acesso ao painel do Railway para configurar variáveis de ambiente.

### Passos
1. **Configure o projeto no Railway**:
   - Crie um novo projeto no Railway.
   - Conecte o repositório GitHub (`s-m-kawase/stryn-back-end`) ao projeto.
   - Adicione um serviço PostgreSQL no Railway:
     - No painel do Railway, clique em "New Service" > "Database" > "PostgreSQL".
     - O Railway gerará automaticamente uma variável `DATABASE_URL` para o serviço.
   - Adicione as variáveis de ambiente no painel do Railway (aba "Variables"):
     - Copie as variáveis do arquivo `.env` (ex.: `SECRET_KEY`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `STRIPE_SECRET_KEY`, etc.).
     - Certifique-se de que `DATABASE_URL` está configurado com o valor fornecido pelo serviço PostgreSQL.
     - Defina `DEBUG=False` para produção.
     - Configure `DOMAIN_FRONT` com a URL do front-end (ex.: `https://seu-front-no-netlify-ou-dominio.com`).
     - Se usar AWS S3, defina `USE_AWS=True` e configure `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, e `AWS_STORAGE_BUCKET_NAME`.

2. **Deploy automático**:
   - O Railway iniciará o deploy automaticamente após cada push no branch principal do GitHub.
   - O arquivo `nixpacks.toml` configura o ambiente com Python 3.12, PostgreSQL, e dependências necessárias, instalando as dependências do `requirements.txt` e executando `python manage.py collectstatic --noinput`.
   - O servidor é iniciado com:
     ```bash
     gunicorn stryn.wsgi:application --bind 0.0.0.0:${PORT} --workers=3 --timeout=180 --log-file -
     ```

3. **Aplique as migrações**:
   - Após o deploy, as migrações do banco de dados não são executadas automaticamente. Execute-as manualmente:
     - **Opção 1: Console do Railway**:
       - No painel do Railway, vá até o serviço do aplicativo, abra o console (aba "Deployments" ou "Logs"), e execute:
         ```bash
         python3 manage.py migrate
         ```
     - **Opção 2: Railway CLI**:
       - Instale a Railway CLI (`npm install -g @railway/cli`).
       - Conecte-se ao projeto com `railway login` e `railway link`.
       - Execute:
         ```bash
         railway run python3 manage.py migrate
         ```
   - Verifique os logs para confirmar que as migrações foram aplicadas (ex.: `Applying <app_name>.0001_initial... OK`).

4. **Crie um superusuário** (se necessário):
   - Se o banco PostgreSQL é novo, crie um superusuário para acessar o painel admin:
     - No console do Railway ou via Railway CLI, execute:
       ```bash
       python3 manage.py createsuperuser
       ```
     - Siga as instruções para definir username, e-mail e senha.

5. **Verifique o deploy**:
   - Acesse o domínio gerado pelo Railway (ex.: `https://<seu-projeto>.up.railway.app`).
   - Teste o painel admin em `/admin/` com o superusuário criado.
   - Acesse a documentação da API em `/api/schema/` (via `drf-spectacular`).
   - Verifique os logs no Railway (aba "Deployments" > "Logs") para identificar erros.

6. **Teste integrações**:
   - Confirme que o CORS permite o front-end (definido em `DOMAIN_FRONT`).
   - Teste pagamentos com Stripe e ASAAS usando endpoints da API.
   - Verifique o envio de e-mails (ex.: redefinição de senha) com as configurações SMTP.
   - Se `USE_AWS=True`, confirme que arquivos estáticos e de mídia estão sendo servidos do S3.

## Notas Adicionais
- **Ambiente Virtual no Railway**: O ambiente virtual é criado automaticamente pelo `nixpacks.toml` em `/opt/venv`, e as dependências são instaladas a partir do `requirements.txt`.
- **Banco de Dados**: O Railway usa PostgreSQL em produção. Para desenvolvimento local, você pode usar SQLite (mais simples) ou PostgreSQL (mais próximo da produção).
- **Segurança**: Nunca versionar o arquivo `.env`. Use o painel do Railway para configurar variáveis sensíveis.
- **Documentação da API**: Acesse `/api/schema/` para a documentação gerada pelo `drf-spectacular`.
- **Troubleshooting**:
  - Se o deploy falhar, verifique os logs no Railway.
  - Para erros de banco de dados, confirme que `DATABASE_URL` está correto.
  - Para erros de dependências, verifique o `requirements-dev.txt` e o `nixpacks.toml`.
