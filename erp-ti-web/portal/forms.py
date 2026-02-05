from django import forms

from .models import (
    Acesso,
    Chamado,
    Email,
    Emprestimo,
    Equipamento,
    IP,
    Insumo,
    Ramal,
    Requisicao,
    Software,
    Usuario,
)


class DateInput(forms.DateInput):
    input_type = "date"


def _styled_fields(form: forms.ModelForm) -> forms.ModelForm:
    for field in form.fields.values():
        css_class = "form-control"
        if isinstance(field.widget, forms.Select):
            css_class = "form-select"
        field.widget.attrs["class"] = css_class
    return form


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class AcessoForm(forms.ModelForm):
    class Meta:
        model = Acesso
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class IPForm(forms.ModelForm):
    class Meta:
        model = IP
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class RamalForm(forms.ModelForm):
    class Meta:
        model = Ramal
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields = "__all__"
        widgets = {"data": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Requisicao
        fields = "__all__"
        widgets = {"requisitado": DateInput(), "recebido": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class EmprestimoForm(forms.ModelForm):
    class Meta:
        model = Emprestimo
        fields = "__all__"
        widgets = {"data": DateInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)


class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _styled_fields(self)
