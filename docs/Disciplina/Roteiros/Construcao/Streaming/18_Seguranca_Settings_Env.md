# 18 - **Seguranca de Configuracao (settings e .env)**

## Introducao

Neste roteiro, vamos fortalecer a seguranca da aplicacao de Streaming no nivel de configuracao do Django.

A maioria dos incidentes em APIs web comeca por configuracoes inseguras: `DEBUG=True` em producao, `SECRET_KEY` exposta no repositorio, `ALLOWED_HOSTS` aberto demais e ausencia de variaveis de ambiente.

## Objetivos de Aprendizagem

Ao final deste roteiro, voce sera capaz de:

1. Separar configuracoes sensiveis usando arquivo `.env`.
2. Remover segredos do codigo-fonte.
3. Configurar `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS` e CORS com seguranca.
4. Criar um fluxo minimo de configuracao para desenvolvimento e producao.

## Pre-requisitos

1. Projeto Django funcional.
2. Conhecimento basico de `settings.py`.
3. Ambiente virtual ativo.

## Conceitos Essenciais

### 1) Segredo nao vai para Git

Dados sensiveis devem ficar fora do repositorio:

- `SECRET_KEY`
- Senhas de banco
- Tokens de API
- Chaves de servicos externos

### 2) Configuracao por ambiente

Cada ambiente deve ter seus valores:

1. Desenvolvimento: mais flexivel.
2. Producao: mais restritivo.

### 3) Principio do menor privilegio

Abrir apenas o necessario: hosts, origens CORS e sessoes seguras.

## Passo 1: Instalar biblioteca para ler variaveis de ambiente

Exemplo com `python-decouple`:

```bash
pip install python-decouple
```

## Passo 2: Criar arquivo `.env`

Na raiz do projeto Django, crie `.env`:

```env
SECRET_KEY=troque_esta_chave
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,seu-dominio.onrender.com
CSRF_TRUSTED_ORIGINS=https://seu-dominio.onrender.com
CORS_ALLOWED_ORIGINS=https://seu-frontend.com,http://localhost:5173
```

## Passo 3: Garantir que `.env` nao seja versionado

No `.gitignore`, adicione:

```gitignore
.env
*.env
```

Opcional: criar um `.env.example` com valores ficticios para documentacao do time.

## Passo 4: Ler variaveis no `settings.py`

```python
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=Csv()
)

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='',
    cast=Csv()
)
```

## Passo 5: Endurecer configuracoes para producao

No `settings.py`, configure cookies e cabecalhos de seguranca:

```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
```

Observacao: `SECURE_SSL_REDIRECT=True` exige HTTPS em producao.

## Passo 6: Ajustar CORS com lista explicita

Evite `CORS_ALLOW_ALL_ORIGINS=True` em producao.

Use lista explicita no `.env` e no `settings.py`.

Exemplo valido:

```env
CORS_ALLOWED_ORIGINS=https://seu-frontend.com,http://localhost:5173
```

## Passo 7: Criar um `.env.example`

Arquivo recomendado para onboarding da equipe:

```env
SECRET_KEY=change_me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

## Passo 8: Validar configuracao

Checklist rapido de validacao:

1. Projeto sobe normalmente lendo variaveis do `.env`.
2. `.env` nao aparece em `git status`.
3. `DEBUG=False` em ambiente de deploy.
4. `ALLOWED_HOSTS` sem `*` em producao.
5. CORS restrito a dominios conhecidos.

## Exercicios Praticos

1. Externalizar pelo menos 5 configuracoes sensiveis para `.env`.
2. Criar `.env.example` para o projeto.
3. Simular ambiente de producao (`DEBUG=False`) e validar API.
4. Testar chamada de origem nao autorizada e confirmar bloqueio de CORS.

## Checklist de Conclusao

- [ ] Segredos removidos do codigo-fonte.
- [ ] `.env` ignorado no Git.
- [ ] `.env.example` criado.
- [ ] `DEBUG`, `ALLOWED_HOSTS`, CORS e CSRF configurados por ambiente.
- [ ] Configuracoes de cookies/cabecalhos de seguranca revisadas.

## Erros Comuns

1. Commitar `.env` por engano.
2. Deixar `DEBUG=True` em producao.
3. Usar `ALLOWED_HOSTS = ['*']` em ambiente publico.
4. Liberar CORS para qualquer origem em producao.
5. Nao documentar variaveis obrigatorias para o time.

## Conclusao

Com configuracao segura no `settings.py` e uso correto de `.env`, a aplicacao reduz riscos de exposicao de segredos e falhas de configuracao em producao.

Esse roteiro complementa os anteriores de autenticacao, autorizacao e upload, criando uma base mais robusta para deploy seguro.
