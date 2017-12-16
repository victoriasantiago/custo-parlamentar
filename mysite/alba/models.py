from django.db import models
from django.utils import timezone

class Deputado(models.Model):
    id = models.AutoField(primary_key=True)

    id_site = models.IntegerField()
    nome = models.CharField(max_length=50)
    foto = models.ImageField(upload_to='deputados_perfil/')
    partido = models.ForeignKey('Partido', on_delete=models.CASCADE)
    sigla = models.CharField('Partido.sigla_partido', max_length=20)
    slug = models.CharField(max_length=20)
    biografia = models.TextField()


    def __str__(self):
        return self.nome

class Partido(models.Model):
    id = models.AutoField(primary_key=True)

    nome_partido = models.CharField(max_length=50)
    sigla_partido = models.CharField(max_length=20)
    descricao = models.TextField()

    def __str__(self):
        return self.nome_partido
