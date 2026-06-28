Aqui está um roteiro completo e atualizado para fazer deploy de uma aplicação Django REST com SQLite no Back4App:

---

## **ROTEIRO DE DEPLOY: Django REST + SQLite no Back4App**

### **📋 Pré-requisitos**
- Conta no [Back4App](https://www.back4app.com/) (gratuita)
- Git instalado
- Aplicação Django REST funcional localmente
- Arquivo `requirements.txt` atualizado

---

## **1. PREPARAÇÃO DA APLICAÇÃO LOCAL**

### 1.1 Estrutura mínima do projeto
```
meu_projeto/
├── manage.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── meu_projeto/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── app/
    ├── models.py
    ├── views.py
    └── ...
```

### 1.2 Criar arquivos essenciais para deploy

**`requirements.txt`** (versões compatíveis):
```txt
Django==4.2.11
djangorestframework==3.14.0
gunicorn==21.2.0
whitenoise==6.6.0
dj-database-url==2.1.0
python-decouple==3.8
django-cors-headers==4.3.1
```

**`runtime.txt`** (versão do Python):
```
python-3.10.13
```

**`Procfile`** (sem extensão, arquivo texto puro):
```
web: gunicorn meu_projeto.wsgi --log-file -
release: python manage.py migrate
```

**`back4app.json`** (configuração opcional do Back4App):
```json
{
  "name": "Meu Projeto Django",
  "description": "API Django REST",
  "env": {
    "DJANGO_SECRET_KEY": {
      "description": "Chave secreta do Django",
      "value": "sua-chave-secreta-aqui"
    },
    "DJANGO_DEBUG": {
      "description": "Modo debug",
      "value": "False"
    },
    "DJANGO_ALLOWED_HOSTS": {
      "description": "Hosts permitidos",
      "value": ".back4app.com"
    }
  }
}
```

---

## **2. CONFIGURAÇÃO DO SETTINGS.PY**

### 2.1 Configurações para produção

```python
import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = config('DJANGO_SECRET_KEY', default='chave-secreta-local')
DEBUG = config('DJANGO_DEBUG', default='True', cast=bool)

ALLOWED_HOSTS = config(
    'DJANGO_ALLOWED_HOSTS', 
    default='localhost,127.0.0.1'
).split(',')

# APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Terceiros
    'rest_framework',
    'corsheaders',
    'whitenoise.runserver_nostatic',  # Whitenoise
    # Seus apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Whitenoise (após Security)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'meu_projeto.urls'
WSGI_APPLICATION = 'meu_projeto.wsgi.application'

# DATABASE - SQLite (Back4App permite persistência em /app)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# STATIC FILES (Whitenoise)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS (permitir todas origens - ajuste conforme necessário)
CORS_ALLOW_ALL_ORIGINS = True

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Para não expor dados sensíveis
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### 2.2 Arquivo wsgi.py (já existente, mas verifique)
```python
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meu_projeto.settings')
application = get_wsgi_application()
```

---

## **3. PREPARAÇÃO DO GIT**

### 3.1 Inicializar e commitar
```bash
# No diretório do projeto
git init

# Criar .gitignore
echo "*.pyc" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.sqlite3" >> .gitignore
echo "db.sqlite3" >> .gitignore
echo "*.db" >> .gitignore
echo "venv/" >> .gitignore
echo "env/" >> .gitignore
echo ".env" >> .gitignore
echo "staticfiles/" >> .gitignore
echo ".DS_Store" >> .gitignore

# Adicionar arquivos ao git
git add .
git commit -m "Preparação para deploy no Back4App"
```

### 3.2 Criar repositório no GitHub (opcional)
```bash
# Crie um repo no GitHub e conecte
git remote add origin https://github.com/seuusuario/seurepo.git
git branch -M main
git push -u origin main
```

---

## **4. CONFIGURAÇÃO NO BACK4APP**

### 4.1 Criar nova aplicação
1. Acesse [Dashboard Back4App](https://dashboard.back4app.com/)
2. Clique em **"Build New App"**
3. Escolha **"Custom Application"** (ou "Container as a Service")
4. Nomeie sua aplicação
5. Selecione o plano **Free** (ou pago conforme necessidade)

### 4.2 Configurar variáveis de ambiente
No dashboard da app, vá em **App Settings > Server Settings > Environment Variables**:

```
DJANGO_SECRET_KEY = sua-chave-secreta-muito-longa-e-segura
DJANGO_DEBUG = False
DJANGO_ALLOWED_HOSTS = .back4app.com,seuapp.back4app.com
```

**⚠️ Importante:** Gere uma SECRET_KEY forte:
```python
# Rode localmente para gerar
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 4.3 Fazer deploy
**Opção A - Via GitHub:**
1. Em **"App Settings > Connect GitHub"**
2. Autorize e selecione o repositório
3. Configure a branch (`main`)
4. Ative **"Auto Deploy"** (opcional)
5. Clique em **"Deploy"**

**Opção B - Via Back4App CLI:**
```bash
# Instalar CLI
npm install -g back4app-cli

# Login
b4a login

# Deploy
b4a deploy
```

**Opção C - Via upload direto:**
1. No dashboard, vá em **"Deploy"**
2. Arraste o projeto compactado (.zip) ou
3. Use o terminal integrado do Back4App

---

## **5. VERIFICAÇÃO E RESOLUÇÃO DE PROBLEMAS**

### 5.1 Verificar logs
No dashboard do Back4App:
- **App Settings > Web Hosting > Logs**
- Ou pelo terminal: `b4a logs`

### 5.2 Comandos úteis pós-deploy
No terminal web do Back4App ou via SSH:
```bash
# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Verificar migrações
python manage.py showmigrations

# Aplicar migrações (normalmente automático pelo Procfile)
python manage.py migrate
```

### 5.3 Estrutura após deploy
Seu app estará disponível em:
```
https://seuapp.back4app.com/
https://seuapp.back4app.com/admin/
https://seuapp.back4app.com/api/  (suas rotas da API)
```

---

## **6. PROBLEMAS COMUNS E SOLUÇÕES**

### ❌ **Erro 500 - Internal Server Error**
```bash
# Verificar logs
b4a logs --tail 50

# Causas comuns:
# 1. Variáveis de ambiente não configuradas
# 2. Migrations não aplicadas
# 3. Static files não coletados
```

### ❌ **DisallowedHost**
```python
# No settings.py, adicione o domínio do Back4App
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', 
    default='localhost,127.0.0.1,.back4app.com'
).split(',')
```

### ❌ **SQLite - Database locked**
```bash
# O SQLite não é ideal para produção com múltiplas requisições
# Soluções:
# 1. Aumentar timeout no settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {
            'timeout': 20,
        }
    }
}

# 2. OU migrar para PostgreSQL (recomendado para produção)
```

### ❌ **Arquivos estáticos não carregam**
```bash
# No Procfile, adicione antes do web:
release: python manage.py collectstatic --noinput && python manage.py migrate

# E garanta que Whitenoise está configurado corretamente
```

### ❌ **CSRF verification failed**
```python
# Se for API pública, adicione:
CSRF_TRUSTED_ORIGINS = ['https://*.back4app.com']
```

---

## **7. OTIMIZAÇÕES ADICIONAIS**

### 7.1 Para APIs REST puramente (sem admin Django)
```python
# Desabilitar apps não necessários em INSTALLED_APPS
# Remover 'django.contrib.admin' se não usar
# Remover 'django.contrib.sessions' se for stateless
```

### 7.2 Cache e performance
```python
# No Procfile, ajustar workers do Gunicorn:
web: gunicorn meu_projeto.wsgi --log-file - --workers=2 --timeout=30
```

### 7.3 Migrar para PostgreSQL (recomendado para produção)
```bash
# No Back4App, crie um database PostgreSQL gratuito
# Adicione ao requirements.txt:
psycopg2-binary==2.9.9

# Atualize settings.py:
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='sqlite:///db.sqlite3')
    )
}
```

---

## **8. CHECKLIST FINAL DE DEPLOY**

- [ ] `requirements.txt` com todas dependências
- [ ] `Procfile` configurado
- [ ] `runtime.txt` com versão Python
- [ ] `.gitignore` configurado
- [ ] `DEBUG = False` em produção
- [ ] `SECRET_KEY` configurada como variável de ambiente
- [ ] `ALLOWED_HOSTS` incluindo domínio Back4App
- [ ] Whitenoise configurado para estáticos
- [ ] Static files coletados (`collectstatic`)
- [ ] Migrações aplicadas
- [ ] CORS configurado (se necessário)
- [ ] Teste local com `gunicorn meu_projeto.wsgi`
- [ ] Logs verificados após deploy
- [ ] Superusuário criado (se necessário)
- [ ] Endpoints da API testados

---

## **🎯 Pronto!**
Sua API Django REST com SQLite estará rodando no Back4App. Para aplicações em produção com muitos usuários, considere migrar para PostgreSQL e configurar um domínio personalizado.

**Monitoramento:** Acompanhe os logs regularmente e configure alertas no dashboard do Back4App para erros e consumo de recursos.