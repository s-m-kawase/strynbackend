
# Stryn

Back-end do projeto Stryn.

## Passo a passo para rodar o projeto:
- Clone o repositório:
```bash
   git@github.com:TimeNovaData/stryn-back.git
```

- Criação de env (crie fora da pasta raíz clonada do back):
```bash
  #Linux
  python3 -m venv <nome da env>

  #Windows
  python -m venv <nome da env>
```

- Após criar a env, utilize os comandos:
```bash
  #caso seja linux
  . <nome da env>/bin/activate

  #caso seja windows
  . <nome da env>/Scripts/activate
```

- Após criar a env, utilize os comandos:
```bash
  cd stryn-back
  pip install -r requirements-dev.txt

  #caso dê erro no requirements pelo  psycopg2-binary 
   pip install psycopg2-binary 
```

- Caso o banco utilizado seja existente, rodar o comando:
```bash
  python3 manage.py migrate
```
- Se estiver usando um banco novo, use o comando:
```bash
  python3 manage.py createsuperuser
```
- Após isso tudo, para rodar o projeto:
```bash
  python3 manage.py runserver
```
