from rest_framework import serializers
from .models import Content, Playlist

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    # Exibe os detalhes dos conteúdos na playlist
    contents = ContentSerializer(many=True, read_only=True)
    # Permite adicionar conteúdos à playlist usando seus IDs
    content_ids = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all(), write_only=True, many=True, source='contents'
    )

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'description', 'user', 'contents', 'content_ids', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        # Remove 'contents' do validated_data para evitar erros, já que será tratado separadamente
        content_data = validated_data.pop('contents', [])
        # Cria a playlist sem os conteúdos
        playlist = super().create(validated_data)
        # Adiciona os conteúdos à playlist usando os IDs fornecidos
        playlist.contents.set(content_data)
        # Retorna a playlist criada
        return playlist

    def update(self, instance, validated_data):
        # Remove 'contents' do validated_data para evitar erros, já que será tratado separadamente
        content_data = validated_data.pop('contents', None)
        # Atualiza a playlist sem os conteúdos
        playlist = super().update(instance, validated_data)
        # Se 'contents' foi fornecido, atualiza os conteúdos da playlist
        if content_data is not None:
            playlist.contents.set(content_data)
        return playlist