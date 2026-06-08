Para implementar QR codes em uma API Django REST para um sistema de gerenciamento de eventos, você tem duas abordagens principais: gerar os QR codes **dinamicamente** (sob demanda) ou **pré-gerá-los** como arquivos estáticos.

A abordagem recomendada para a maioria dos casos é a **geração dinâmica**, que é mais flexível e econômica .

Aqui está um guia prático para implementar ambas as soluções.

---

## Visão Geral da Solução

- **Geração Dinâmica (Recomendada)**: O QR code é criado em tempo real por uma view sempre que a URL é acessada. É ideal quando a URL de check-in pode mudar ou para economizar espaço em disco.
- **Pré-geração com Models**: O QR code é criado e salvo fisicamente no servidor/Storage no momento da criação do ingresso, via signals ou sobrescrita do `save()`.

---

## 1. Setup Inicial

Primeiro, instale a biblioteca `qrcode` no seu ambiente virtual:

```bash
pip install qrcode[pil]
```

**Estrutura de Model Sugerida:**
Para funcionar, seu modelo de Ticket/Ingresso precisa ter um campo que aponte para a URL de validação.

```python
# models.py
from django.db import models
from django.conf import settings

class Ticket(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True, db_index=True)
    is_valid = models.BooleanField(default=True)

    def get_checkin_url(self):
        # Gera a URL completa para validação (ex: https://meusite.com/checkin/token)
        return f"{settings.BASE_URL}/api/checkin/{self.token}/"
```

---

## 2. Abordagem 1: Geração Dinâmica (Via API Endpoint)

Esta é a forma mais "RESTful". Você não salva imagens; cria uma view que retorna a imagem PNG ou SVG diretamente .

### Implementação da View

```python
# views.py
from io import BytesIO
from qrcode import make
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Ticket

class TicketQRCodeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        # Busca o ingresso e garante que pertence ao usuário logado
        ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        
        # Dados que serão codificados no QR Code (a URL de check-in)
        qr_data = ticket.get_checkin_url()
        
        # Gera a imagem QR code em memória
        img = make(qr_data)
        
        # Salva em um buffer de bytes
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Retorna a resposta com o content-type correto
        return HttpResponse(buffer, content_type="image/png")
```

### URL da API

```python
# urls.py
from django.urls import path
from .views import TicketQRCodeView

urlpatterns = [
    # ...
    path('api/tickets/<int:ticket_id>/qr-code/', TicketQRCodeView.as_view(), name='ticket-qr'),
]
```

### Como o Frontend Consome
No React, Vue.js ou mobile, basta usar a URL da API no atributo `src` de uma tag `<img>`:
```html
<img src="https://seusite.com/api/tickets/123/qr-code/" alt="QR Code do Ingresso" />
```

---

## 3. Abordagem 2: Pré-geração (Salvando no Model)

Se você precisa gerar o QR uma única vez (ex: anexar em email de confirmação), salve a imagem no campo `ImageField` do Django.

### Utilizando Signal (post_save)

```python
# models.py
from django.db import models
from django.core.files.base import ContentFile
from io import BytesIO
from qrcode import make

class Ticket(models.Model):
    # ... outros campos ...
    qr_code_image = models.ImageField(upload_to='tickets/qrcodes/', blank=True, null=True)

    def save_qr_code(self):
        buffer = BytesIO()
        make(self.get_checkin_url()).save(buffer, format="PNG")
        file_name = f"ticket_{self.id}_qr.png"
        self.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=False)

# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Ticket)
def generate_qr_code(sender, instance, created, **kwargs):
    if created:  # Gera apenas na primeira criação
        instance.save_qr_code()
        instance.save()
```

---

## 4. Segurança e Validação (Check-in)

O QR code em si é apenas uma URL. A segurança está no **token** dessa URL e na **validação** do check-in. Para isso, implemente uma view pública de validação:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def validate_checkin(request, token):
    try:
        ticket = Ticket.objects.get(token=token)
    except Ticket.DoesNotExist:
        return Response({"error": "Invalid ticket"}, status=404)

    if not ticket.is_valid:
        return Response({"error": "Already used"}, status=400)

    # Marca como utilizado e registra horário
    ticket.is_valid = False
    ticket.checked_in_at = timezone.now()
    ticket.save()

    return Response({"message": "Check-in successful", "event": ticket.event.name})
```

### Recomendações de Segurança:
- **Use tokens aleatórios longos**: Prefira `secrets.token_urlsafe(32)` em vez de IDs sequenciais.
- **Expiração**: Adicione um campo `expires_at` se os QR codes forem temporários.
- **Validação de Ambiente (Opcional)**: Implemente JWT dentro do QR code para evitar reaproveitamento .

---

## 5. Customização e Boas Práticas

- **Formato SVG**: Para alta qualidade na web, utilize SVG em vez de PNG, passando `image_factory=SvgPathImage` .
- **Versão em Lote**: Para gerar centenas de QR codes, utilize tarefas assíncronas com **Celery** ou **Django Q** para não travar a requisição.
- **Cache**: Se o QR code nunca muda, configure o header `Cache-Control: max-age=31536000` na view dinâmica para otimizar o carregamento.

### Fontes e Referências
- Este padrão de geração dinâmica evita armazenar arquivos desnecessários no disco, seguindo as melhores práticas da comunidade Django .
- A biblioteca `qrcode` é a mais utilizada para este fim, sendo compatível com Python moderno .
- Caso precise de uma interface administrativa robusta para gerenciar eventos e ingressos, você pode se inspirar em projetos como Eventify .