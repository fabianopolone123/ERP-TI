from dataclasses import dataclass

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import (
    AcessoForm,
    ChamadoForm,
    EmailForm,
    EmprestimoForm,
    EquipamentoForm,
    InsumoForm,
    IPForm,
    RamalForm,
    RequisicaoForm,
    SoftwareForm,
    UsuarioForm,
)
from .models import Acesso, Chamado, Email, Emprestimo, Equipamento, Insumo, IP, Ramal, Requisicao, Software, Usuario


@dataclass(frozen=True)
class ModuleConfig:
    key: str
    title: str
    model: type
    form: type
    columns: tuple[str, ...]


MODULES: tuple[ModuleConfig, ...] = (
    ModuleConfig("usuarios", "Usuarios", Usuario, UsuarioForm, ("departamento", "nome_completo", "perfil")),
    ModuleConfig("acessos", "Acessos", Acesso, AcessoForm, ("pasta",)),
    ModuleConfig("equipamentos", "Equipamentos", Equipamento, EquipamentoForm, ("equipamento", "modelo", "marca", "patrimonio")),
    ModuleConfig("ips", "IPs", IP, IPForm, ("ip", "nome", "fabricante", "endereco_mac")),
    ModuleConfig("emails", "Emails", Email, EmailForm, ("nro", "nome", "sobrenome", "email", "grupo", "situacao")),
    ModuleConfig("ramais", "Ramais", Ramal, RamalForm, ("nro", "nome", "sobrenome", "email", "grupo", "situacao")),
    ModuleConfig("softwares", "Softwares", Software, SoftwareForm, ("nome", "computador", "setor", "serial", "conta")),
    ModuleConfig("insumos", "Insumos", Insumo, InsumoForm, ("insumo", "data", "qtd", "nome", "departamento")),
    ModuleConfig("requisicoes", "Requisicoes", Requisicao, RequisicaoForm, ("solicitacao", "qtd", "valor", "total", "aprovado", "fornecedor")),
    ModuleConfig("emprestimos", "Emprestimos", Emprestimo, EmprestimoForm, ("nome", "equipamento", "documento", "situacao", "data")),
    ModuleConfig("chamados", "Chamados", Chamado, ChamadoForm, ("titulo", "autor", "tipo", "urgencia", "status", "responsavel")),
)

MODULE_MAP = {module.key: module for module in MODULES}


@login_required
def dashboard(request):
    return render(request, "portal/dashboard.html", {"modules": MODULES})


@login_required
def module_page(request, module_key: str):
    module = MODULE_MAP.get(module_key)
    if not module:
        return redirect("dashboard")

    if request.method == "POST":
        form = module.form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"{module.title[:-1]} cadastrado com sucesso.")
            return redirect(reverse("module-page", args=[module_key]))
    else:
        form = module.form()

    rows = module.model.objects.all()[:500]
    context = {
        "modules": MODULES,
        "active_module": module,
        "rows": rows,
        "columns": module.columns,
        "form": form,
    }
    return render(request, "portal/module_page.html", context)

# Create your views here.
