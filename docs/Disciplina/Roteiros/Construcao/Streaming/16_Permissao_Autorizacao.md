# 16 - **Permissão e Autorização**

## Introdução

Neste roteiro, vamos evoluir a API de Streaming de um cenário apenas autenticado para um cenário realmente seguro.

Autenticar responde "quem é o usuário".
Autorizar responde "o que esse usuário pode fazer".

Sem autorização, qualquer usuário autenticado pode alterar ou excluir recursos que não são seus.

## Objetivos de Aprendizagem

Ao final deste roteiro, você será capaz de:

1. Diferenciar autenticação de autorização no Django REST Framework (DRF).
2. Aplicar permissões globais e permissões por objeto.
3. Restringir edição/exclusão para dono do recurso ou administrador.
4. Implementar regras de visibilidade para recursos privados.

## Pré-requisitos

1. Projeto Django com DRF configurado.
2. Autenticação funcional (exemplo: Token).
3. Endpoints CRUD funcionando para pelo menos um recurso (ex.: Content ou Playlist).

## Conceitos Essenciais

### 1) Permissão Global

É aplicada antes de buscar um objeto específico.

Exemplo comum:

- `IsAuthenticated`: exige usuário logado para acessar a rota.

### 2) Permissão por Objeto

É aplicada quando já existe um objeto alvo da ação.

Exemplo comum:

- Só o dono do conteúdo (ou admin) pode editar/excluir.

### 3) Matriz de Regras (exemplo)

| Ação | Assinante | Criador (dono) | Admin |
|------|-----------|----------------|-------|
| Listar conteúdos públicos | Sim | Sim | Sim |
| Criar conteúdo | Não | Sim | Sim |
| Editar conteúdo próprio | Não | Sim | Sim |
| Editar conteúdo de terceiros | Não | Não | Sim |
| Excluir conteúdo próprio | Não | Sim | Sim |
| Excluir conteúdo de terceiros | Não | Não | Sim |
| Ver playlist privada de terceiros | Não | Não | Sim |

## Passo 1: Definir permissões globais

No DRF, você pode começar exigindo autenticação por padrão e abrindo exceções de leitura pública em views específicas.

Exemplo no `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

Se quiser leitura pública para algumas rotas, ajuste as permissões diretamente na View/ViewSet.

## Passo 2: Criar permissão customizada por objeto

Crie um arquivo de permissões no app, por exemplo `permissions.py`:

```python
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """
    Permite leitura para métodos seguros.
    Permite escrita apenas para dono do objeto ou admin.
    """

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            return True

        # Admin tem acesso total
        if request.user and request.user.is_staff:
            return True

        # Ajuste o atributo do dono conforme seu modelo (owner, user, creator etc.)
        owner = getattr(obj, 'owner', None) or getattr(obj, 'user', None)
        return owner == request.user
```

## Passo 3: Aplicar a permissão na ViewSet

Exemplo de uso em uma ViewSet de conteúdos:

```python
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Content
from .serializers import ContentSerializer
from .permissions import IsOwnerOrAdmin


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer

    # Leitura liberada; escrita exige autenticação
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        # Garante que o dono do recurso seja o usuário logado
        serializer.save(owner=self.request.user)
```

Observação: se seu modelo usar `creator`, `author` ou outro campo, adapte o código.

## Passo 4: Regras para recurso privado (ex.: Playlist)

Para playlists privadas, além da regra de edição, controle também a leitura.

Exemplo de lógica de acesso:

1. Playlist pública: qualquer usuário pode visualizar.
2. Playlist privada: apenas dono ou admin pode visualizar.

Você pode aplicar essa regra em:

- `get_queryset` (filtrando o que o usuário pode ver).
- Permissão custom com `has_object_permission`.

## Passo 5: Validar cenários de segurança

Teste os seguintes casos:

1. Usuário A edita conteúdo próprio: deve funcionar (`200 OK` ou `202/204`).
2. Usuário B tenta editar conteúdo de A: deve falhar (`403 Forbidden`).
3. Usuário B tenta ver playlist privada de A: deve falhar (`403` ou `404`, conforme sua estratégia).
4. Admin executa ação em conteúdo de terceiros: deve funcionar.

## Exercício Prático

Implemente as regras abaixo e registre evidências (print de resposta ou log):

1. Usuário comum não pode excluir conteúdo de terceiros.
2. Criador pode editar e excluir apenas o que criou.
3. Admin pode editar/excluir qualquer conteúdo.
4. Playlist privada só é visível para dono e admin.

## Checklist de Conclusão

- [ ] Existe uma política de permissões documentada.
- [ ] Permissões globais estão configuradas.
- [ ] Permissões por objeto foram implementadas.
- [ ] Recursos privados têm controle de visibilidade.
- [ ] Cenários positivos e negativos foram testados.

## Erros Comuns

1. Confiar apenas em autenticação e esquecer autorização.
2. Permitir `PUT/PATCH/DELETE` sem checar dono do objeto.
3. Não sobrescrever `perform_create`, deixando o dono indefinido.
4. Expor recursos privados por falha de filtro no `queryset`.

## Conclusão

Com permissões globais e por objeto, sua API deixa de ser apenas funcional e passa a ser segura e coerente com as regras de negócio.

No próximo roteiro, o ideal é aplicar o mesmo cuidado ao fluxo de upload e armazenamento de mídia, garantindo que arquivos também respeitem as políticas de acesso.
