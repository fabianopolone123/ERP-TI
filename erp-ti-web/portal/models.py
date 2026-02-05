from django.db import models


class Usuario(models.Model):
    departamento = models.CharField(max_length=120)
    nome_completo = models.CharField(max_length=180)
    perfil = models.CharField(max_length=120, blank=True)
    telefone = models.CharField(max_length=80, blank=True)
    ramal = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["nome_completo"]

    def __str__(self) -> str:
        return self.nome_completo


class Acesso(models.Model):
    pasta = models.CharField(max_length=180, unique=True)

    class Meta:
        ordering = ["pasta"]

    def __str__(self) -> str:
        return self.pasta


class Equipamento(models.Model):
    id_interno = models.CharField(max_length=60, blank=True)
    patrimonio = models.CharField(max_length=60, blank=True)
    selo_patrimonio = models.CharField(max_length=60, blank=True)
    equipamento = models.CharField(max_length=120)
    modelo = models.CharField(max_length=120, blank=True)
    marca = models.CharField(max_length=120, blank=True)
    serie = models.CharField(max_length=120, blank=True)
    mem = models.CharField(max_length=40, blank=True)
    processador = models.CharField(max_length=120, blank=True)
    geracao = models.CharField(max_length=60, blank=True)
    hd = models.CharField(max_length=80, blank=True)
    mod_hd = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["equipamento"]

    def __str__(self) -> str:
        return self.equipamento


class IP(models.Model):
    ip = models.CharField(max_length=45)
    nome = models.CharField(max_length=120, blank=True)
    fabricante = models.CharField(max_length=120, blank=True)
    endereco_mac = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["ip"]

    def __str__(self) -> str:
        return self.ip


class Email(models.Model):
    nro = models.CharField(max_length=30, blank=True)
    nome = models.CharField(max_length=120, blank=True)
    sobrenome = models.CharField(max_length=120, blank=True)
    email = models.EmailField()
    grupo = models.CharField(max_length=120, blank=True)
    situacao = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:
        return self.email


class Ramal(models.Model):
    nro = models.CharField(max_length=30, blank=True)
    nome = models.CharField(max_length=120, blank=True)
    sobrenome = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    grupo = models.CharField(max_length=120, blank=True)
    situacao = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome or self.nro or f"Ramal {self.pk}"


class Software(models.Model):
    nome = models.CharField(max_length=120)
    computador = models.CharField(max_length=120, blank=True)
    setor = models.CharField(max_length=120, blank=True)
    serial = models.CharField(max_length=140, blank=True)
    conta = models.CharField(max_length=140, blank=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self) -> str:
        return self.nome


class Insumo(models.Model):
    insumo = models.CharField(max_length=120)
    data = models.DateField(null=True, blank=True)
    qtd = models.CharField(max_length=40, blank=True)
    nome = models.CharField(max_length=120, blank=True)
    departamento = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.insumo


class Requisicao(models.Model):
    STATUS_APROVACAO = [
        ("sim", "Sim"),
        ("nao", "Nao"),
        ("esperando", "Esperando"),
    ]
    solicitacao = models.CharField(max_length=200)
    qtd = models.CharField(max_length=30, blank=True)
    valor = models.CharField(max_length=50, blank=True)
    total = models.CharField(max_length=50, blank=True)
    requisitado = models.DateField(null=True, blank=True)
    aprovado = models.CharField(max_length=20, choices=STATUS_APROVACAO, default="esperando")
    recebido = models.DateField(null=True, blank=True)
    nf = models.CharField(max_length=80, blank=True)
    tipo = models.CharField(max_length=80, blank=True)
    fornecedor = models.CharField(max_length=160, blank=True)
    link = models.URLField(blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.solicitacao


class Emprestimo(models.Model):
    nome = models.CharField(max_length=120)
    equipamento = models.CharField(max_length=120, blank=True)
    documento = models.CharField(max_length=120, blank=True)
    arquivo = models.CharField(max_length=255, blank=True)
    situacao = models.CharField(max_length=80, blank=True)
    data = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"{self.nome} - {self.equipamento}"


class Chamado(models.Model):
    TIPO_CHOICES = [
        ("incidente", "Incidente"),
        ("solicitacao", "Solicitacao"),
        ("melhoria", "Melhoria"),
        ("programado", "Programado"),
    ]
    URGENCIA_CHOICES = [
        ("normal", "Normal"),
        ("baixa", "Baixa"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("urgente", "Urgente"),
    ]
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("em_atendimento", "Em atendimento"),
        ("fechado", "Fechado"),
    ]
    titulo = models.CharField(max_length=180)
    descricao = models.TextField(blank=True)
    autor = models.CharField(max_length=120, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="solicitacao")
    urgencia = models.CharField(max_length=20, choices=URGENCIA_CHOICES, default="normal")
    arquivo = models.CharField(max_length=255, blank=True)
    responsavel = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pendente")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.titulo

# Create your models here.
