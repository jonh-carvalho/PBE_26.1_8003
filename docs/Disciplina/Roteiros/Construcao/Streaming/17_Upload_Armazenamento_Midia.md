# 17 - **Upload e Armazenamento de Mídia**

## Introdução

Neste roteiro, vamos transformar o projeto de Streaming de um cenário com URLs simuladas para um fluxo real de upload de mídia.

Até aqui, é comum salvar apenas links de arquivos. Em aplicações reais, precisamos receber, validar, armazenar e servir arquivos com segurança.

## Objetivos de Aprendizagem

Ao final deste roteiro, você será capaz de:

1. Implementar upload de arquivos com `multipart/form-data` no DRF.
2. Configurar `MEDIA_ROOT` e `MEDIA_URL` no Django.
3. Validar tamanho e tipo de arquivo no backend.
4. Consumir endpoint de upload no frontend com `FormData`.

## Pré-requisitos

1. Projeto Django com DRF funcionando.
2. Autenticação e autorização básicas já implementadas.
3. Endpoint CRUD existente para o recurso de conteúdo (ou similar).

## Conceitos Essenciais

### 1) `multipart/form-data`

Formato de requisição usado para enviar arquivos no corpo da requisição HTTP.

### 2) Campos de arquivo no Django

- `FileField`: arquivo genérico.
- `ImageField`: imagem (exige biblioteca Pillow).

### 3) Configuração de mídia

- `MEDIA_ROOT`: pasta física onde arquivos serão armazenados.
- `MEDIA_URL`: URL pública para acessar esses arquivos.

### 4) Segurança em upload

Sempre valide:

1. Extensão/tipo permitido.
2. Tamanho máximo.
3. Perfil autorizado para envio.

## Passo 1: Ajustar modelagem para arquivos

Exemplo em `models.py`:

```python
from django.db import models
from django.contrib.auth.models import User


class Content(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    media_file = models.FileField(upload_to='contents/media/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='contents/covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Depois execute:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Passo 2: Configurar mídia no `settings.py`

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Passo 3: Expor mídia em desenvolvimento no `urls.py`

```python
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('api/', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## Passo 4: Ajustar serializer com validações

Exemplo em `serializers.py`:

```python
from rest_framework import serializers
from .models import Content


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ['owner']

    def validate_media_file(self, file_obj):
        if not file_obj:
            return file_obj

        max_mb = 100
        if file_obj.size > max_mb * 1024 * 1024:
            raise serializers.ValidationError(
                f'Arquivo excede o limite de {max_mb}MB.'
            )

        allowed_extensions = ['.mp4', '.mp3', '.mkv']
        filename = file_obj.name.lower()
        if not any(filename.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError('Extensão de arquivo não permitida.')

        return file_obj
```

## Passo 5: Ajustar ViewSet para aceitar upload

```python
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Content
from .serializers import ContentSerializer


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
```

## Passo 6: Testar upload na API

Exemplo com `curl`:

```bash
curl -X POST http://localhost:8000/api/contents/ \
  -H "Authorization: Token SEU_TOKEN" \
  -F "title=Meu Video" \
  -F "description=Conteudo de teste" \
  -F "media_file=@C:/caminho/video.mp4" \
  -F "cover_image=@C:/caminho/capa.jpg"
```

## Passo 7: Consumir upload no frontend com `FormData`

```javascript
const formData = new FormData();
formData.append('title', 'Meu Video');
formData.append('description', 'Conteudo enviado via frontend');
formData.append('media_file', mediaInput.files[0]);
formData.append('cover_image', coverInput.files[0]);

fetch('http://localhost:8000/api/contents/', {
  method: 'POST',
  headers: {
    Authorization: 'Token SEU_TOKEN',
  },
  body: formData,
})
  .then((response) => response.json())
  .then((data) => {
    console.log('Upload realizado:', data);
  })
  .catch((error) => {
    console.error('Erro no upload:', error);
  });
```

## Testes Recomendados

1. Upload válido de arquivo dentro do limite.
2. Upload de arquivo acima do tamanho máximo.
3. Upload de extensão não permitida.
4. Usuário sem permissão tentando enviar arquivo.

## Exercício Prático

Implemente e demonstre os cenários abaixo:

1. Envio de vídeo válido com capa.
2. Rejeição de arquivo inválido com mensagem clara.
3. Exibição da mídia salva via URL de retorno da API.

## Checklist de Conclusão

- [ ] Campos de mídia adicionados ao modelo.
- [ ] `MEDIA_ROOT` e `MEDIA_URL` configurados.
- [ ] Endpoint recebe `multipart/form-data`.
- [ ] Validação de tamanho e extensão implementada.
- [ ] Frontend envia arquivo com `FormData`.
- [ ] Casos de erro foram testados.

## Erros Comuns

1. Tentar enviar arquivo com `Content-Type: application/json`.
2. Não configurar `parser_classes` para multipart.
3. Não validar tamanho/extensão e abrir risco de abuso.
4. Esquecer regra de autorização para upload.

## Conclusão

Com esse fluxo, a plataforma passa a operar com mídia real e tratamento adequado de segurança e validação.

Como próximo avanço, você pode integrar armazenamento em nuvem (como S3) e políticas de acesso mais refinadas para arquivos privados.
