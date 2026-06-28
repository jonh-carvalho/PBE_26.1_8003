from django.utils import timezone
recent_contents = Content.objects.filter(upload_date__gte=timezone.now() - timezone.timedelta(days=7))
for content in recent_contents:
    print(content.title)