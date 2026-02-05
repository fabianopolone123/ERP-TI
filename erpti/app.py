import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from erpti.database import DatabaseManager


DEFAULT_ACCESS_FOLDERS = [
    "Comun",
    "Almoxarifado",
    "Contabil",
    "Comercial",
    "Compras",
    "Contratos",
    "Financeiro",
    "Fiscal",
    "Eventos",
    "Gerencia",
    "Manutencao",
    "Obras",
    "Obras PCP",
    "Orcamentos",
    "Planejamento",
    "Qualidade",
    "Producao",
    "Projetos",
    "Projetos PCP",
    "RH",
    "Romaneios",
    "SAC",
    "Seguranca Trabalho",
    "Terceiros",
    "TI",
]


class ERPDesktopApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("ERP TI - Painel Principal")
        self.geometry("1366x768")
        self.state("zoomed")
        self.minsize(1200, 700)
        self.configure(bg="#0A1B2A")

        self._fullscreen = False
        self.bind("<F11>", self._toggle_fullscreen)
        self.bind("<Escape>", self._exit_fullscreen)

        self.modules = [
            ("Usuarios", "Controle de usuarios"),
            ("Acessos", "Permissoes e niveis de acesso"),
            ("Equipamentos", "Inventario e status dos equipamentos"),
            ("IPs", "Gestao de enderecamento IP"),
            ("Emails", "Contas, grupos e distribuicao"),
            ("Ramais", "Telefonia interna"),
            ("Softwares", "Licencas e versoes"),
            ("Insumos", "Estoque e consumo"),
            ("Requisicoes", "Pedidos internos"),
            ("Emprestimos", "Controle de itens emprestados"),
            ("Chamados", "Suporte e atendimento"),
        ]

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self._configure_styles()

        self.current_user = tk.StringVar(value="Administrador")
        self.users_data = []
        self.equipment_data = []
        self.ip_data = []
        self.email_data = []
        self.ramal_data = []
        self.software_data = []
        self.insumo_data = []
        self.requisicao_data = []
        self.emprestimo_data = []
        self.chamado_data = []
        self.access_folders = []

        self.db = DatabaseManager("erpti.db")
        self.db.initialize(DEFAULT_ACCESS_FOLDERS)
        self._load_data_from_db()
        self._show_login()

    def _load_data_from_db(self) -> None:
        self.users_data = self.db.fetch_rows(
            "users",
            ("id", "departamento", "nome", "perfil", "username", "senha", "telefone", "ramal", "email"),
        )
        self._sync_user_group_labels()
        self.equipment_data = self.db.fetch_rows(
            "equipments",
            (
                "id_interno",
                "patrimonio",
                "selo_patrimonio",
                "equipamento",
                "modelo",
                "marca",
                "serie",
                "mem",
                "processador",
                "geracao",
                "hd",
                "mod_hd",
            ),
        )
        self.ip_data = self.db.fetch_rows(
            "ips",
            ("ip", "nome", "fabricante", "endereco_mac"),
        )
        self.email_data = self.db.fetch_rows(
            "emails",
            ("nro", "nome", "sobrenome", "email", "grupo", "situacao"),
        )
        self.ramal_data = self.db.fetch_rows(
            "ramais",
            ("nro", "nome", "sobrenome", "email", "grupo", "situacao"),
        )
        self.software_data = self.db.fetch_rows(
            "softwares",
            ("nome", "computador", "setor", "serial", "conta"),
        )
        self.insumo_data = self.db.fetch_rows(
            "insumos",
            ("insumo", "data", "qtd", "nome", "departamento"),
        )
        self.requisicao_data = self.db.fetch_rows(
            "requisicoes",
            (
                "solicitacao",
                "qtd",
                "valor",
                "total",
                "requisitado",
                "aprovado",
                "recebido",
                "nf",
                "tipo",
                "fornecedor",
                "link",
            ),
        )
        self.emprestimo_data = self.db.fetch_rows(
            "emprestimos",
            ("nome", "equipamento", "documento", "arquivo", "situacao", "data"),
        )
        self.chamado_data = self.db.fetch_rows(
            "chamados",
            (
                "id",
                "titulo",
                "descricao",
                "autor",
                "tipo",
                "urgencia",
                "arquivo",
                "status",
                "legacy_source",
                "legacy_id",
            ),
        )
        self.access_folders = self.db.fetch_access_folders()

    def _sync_user_group_labels(self) -> None:
        group_map = self.db.fetch_user_group_map()
        for user in self.users_data:
            user["perfil"] = group_map.get(int(user["id"]), "")

    def _configure_styles(self) -> None:
        self.style.configure("Card.TFrame", background="#11273B")
        self.style.configure("App.TFrame", background="#0A1B2A")
        self.style.configure(
            "Title.TLabel",
            background="#11273B",
            foreground="#F7FAFC",
            font=("Segoe UI Semibold", 18),
        )
        self.style.configure(
            "Sub.TLabel",
            background="#11273B",
            foreground="#9AB3C7",
            font=("Segoe UI", 11),
        )
        self.style.configure(
            "PanelTitle.TLabel",
            background="#0D2336",
            foreground="#EAF3F9",
            font=("Segoe UI Semibold", 13),
        )
        self.style.configure(
            "Module.TButton",
            font=("Segoe UI Semibold", 11),
            foreground="#EDF4FA",
            background="#1B3A52",
            padding=10,
            borderwidth=0,
            focusthickness=0,
        )
        self.style.map(
            "Module.TButton",
            background=[("active", "#225172"), ("pressed", "#143750")],
        )
        self.style.configure(
            "Action.TButton",
            font=("Segoe UI Semibold", 11),
            foreground="#F7FAFC",
            background="#227D74",
            padding=8,
            borderwidth=0,
            focusthickness=0,
        )
        self.style.map(
            "Action.TButton",
            background=[("active", "#2B958A"), ("pressed", "#1A6C64")],
        )
        self.style.configure(
            "Logout.TButton",
            font=("Segoe UI", 10),
            foreground="#F7FAFC",
            background="#995D34",
            padding=7,
            borderwidth=0,
            focusthickness=0,
        )
        self.style.map(
            "Logout.TButton",
            background=[("active", "#B36F3E"), ("pressed", "#7F4E2B")],
        )
        self.style.configure("TNotebook", background="#0A1B2A", borderwidth=0)
        self.style.configure(
            "TNotebook.Tab",
            background="#16344C",
            foreground="#D4E2EC",
            padding=(16, 8),
            font=("Segoe UI", 10),
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", "#227D74")],
            foreground=[("selected", "#FFFFFF")],
        )

    def _clear_screen(self) -> None:
        for child in self.winfo_children():
            child.destroy()

    def _show_login(self) -> None:
        self._clear_screen()

        root = ttk.Frame(self, style="App.TFrame")
        root.pack(fill="both", expand=True)

        card = ttk.Frame(root, style="Card.TFrame", padding=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(card, text="ERP TI", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Plataforma integrada para gestao de TI",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(2, 26))

        ttk.Label(card, text="Usuario", style="Sub.TLabel").pack(anchor="w", pady=(0, 5))
        self.login_user = ttk.Entry(card, font=("Segoe UI", 11))
        self.login_user.pack(fill="x", ipady=6)

        ttk.Label(card, text="Senha", style="Sub.TLabel").pack(anchor="w", pady=(18, 5))
        self.login_password = ttk.Entry(card, show="*", font=("Segoe UI", 11))
        self.login_password.pack(fill="x", ipady=6)
        self.login_password.bind("<Return>", lambda _event: self._login())

        ttk.Button(card, text="Entrar", command=self._login, style="Action.TButton").pack(
            fill="x", pady=(28, 0)
        )

    def _login(self) -> None:
        username = self.login_user.get().strip()
        senha = self.login_password.get().strip()
        auth_user = self.db.authenticate_user(username, senha)
        if auth_user:
            self.current_user.set(auth_user.get("nome") or auth_user.get("username") or username)
            self._show_dashboard()
            return

        has_credentials = any(
            user.get("username", "").strip() and user.get("senha", "").strip() for user in self.users_data
        )
        # Compatibilidade inicial: enquanto nao houver login cadastrado, permite entrar com usuario digitado.
        if not has_credentials and username:
            self.current_user.set(username)
            self._show_dashboard()
            return

        messagebox.showerror("Login invalido", "Usuario ou senha incorretos.")

    def _show_dashboard(self) -> None:
        self._clear_screen()

        container = ttk.Frame(self, style="App.TFrame", padding=14)
        container.pack(fill="both", expand=True)
        container.columnconfigure(0, weight=1)
        container.rowconfigure(1, weight=1)

        header = ttk.Frame(container, style="Card.TFrame", padding=16)
        header.grid(row=0, column=0, sticky="nsew", pady=(0, 12))
        header.columnconfigure(1, weight=1)

        ttk.Label(header, text="Painel de Controle TI", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            header,
            text="Selecione um modulo para iniciar",
            style="Sub.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        ttk.Label(
            header,
            text=f"Usuario: {self.current_user.get()}",
            style="Sub.TLabel",
        ).grid(row=0, column=1, sticky="e")

        ttk.Button(header, text="Sair", command=self._show_login, style="Logout.TButton").grid(
            row=1, column=1, sticky="e", pady=(4, 0)
        )

        self.notebook = ttk.Notebook(container)
        self.notebook.grid(row=1, column=0, sticky="nsew")

        self._tabs_by_name = {}
        for index, (name, description) in enumerate(self.modules, start=1):
            tab = ttk.Frame(self.notebook, padding=24, style="Card.TFrame")
            self._tabs_by_name[name] = tab
            self.notebook.add(tab, text=name)
            self._build_module_content(tab, name, description)

        self._open_module(self.modules[0][0])

    def _open_module(self, module_name: str) -> None:
        tab = self._tabs_by_name[module_name]
        self.notebook.select(tab)

    def _open_form_dialog(self, title: str, fields: list[tuple], on_submit) -> None:
        dialog = tk.Toplevel(self)
        dialog.title(title)
        width = 560
        height = 520
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg="#0A1B2A")
        dialog.transient(self)
        dialog.grab_set()
        dialog.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        pos_x = parent_x + (parent_w - width) // 2
        pos_y = parent_y + (parent_h - height) // 2
        dialog.geometry(f"{width}x{height}+{max(pos_x, 0)}+{max(pos_y, 0)}")

        form = ttk.Frame(dialog, style="Card.TFrame", padding=18)
        form.pack(fill="both", expand=True, padx=12, pady=12)
        form.columnconfigure(1, weight=1)

        values = {}
        first_input = None
        for row, field in enumerate(fields):
            label = field[0]
            key = field[1]
            options = field[2] if len(field) > 2 else None

            ttk.Label(form, text=label, style="Sub.TLabel").grid(
                row=row, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
            )
            values[key] = tk.StringVar()
            if options:
                widget = ttk.Combobox(
                    form,
                    textvariable=values[key],
                    values=options,
                    state="readonly",
                    font=("Segoe UI", 11),
                )
            else:
                widget = ttk.Entry(form, textvariable=values[key], font=("Segoe UI", 11))
            widget.grid(row=row, column=1, sticky="ew", pady=(0, 8))
            if first_input is None:
                first_input = widget

        actions = ttk.Frame(form, style="Card.TFrame")
        actions.grid(row=len(fields), column=0, columnspan=2, sticky="ew", pady=(10, 0))
        actions.columnconfigure(0, weight=1)

        def clear_form() -> None:
            for var in values.values():
                var.set("")
            if first_input:
                first_input.focus_set()

        def submit(close_after_save: bool) -> None:
            payload = {key: var.get().strip() for key, var in values.items()}
            if on_submit(payload):
                if close_after_save:
                    dialog.destroy()
                else:
                    clear_form()

        ttk.Button(
            actions,
            text="Salvar",
            style="Action.TButton",
            command=lambda: submit(True),
        ).grid(row=0, column=1, sticky="e")
        ttk.Button(
            actions,
            text="Salvar e cadastrar outro",
            style="Action.TButton",
            command=lambda: submit(False),
        ).grid(row=0, column=2, sticky="e", padx=(8, 0))

        if first_input:
            first_input.focus_set()

    def _build_module_content(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        if module_name == "Usuarios":
            self._build_users_module(tab, module_name, description)
            return
        if module_name == "Acessos":
            self._build_access_module(tab, module_name, description)
            return
        if module_name == "Equipamentos":
            self._build_equipments_module(tab, module_name, description)
            return
        if module_name == "IPs":
            self._build_ips_module(tab, module_name, description)
            return
        if module_name == "Emails":
            self._build_emails_module(tab, module_name, description)
            return
        if module_name == "Ramais":
            self._build_ramais_module(tab, module_name, description)
            return
        if module_name == "Softwares":
            self._build_softwares_module(tab, module_name, description)
            return
        if module_name == "Insumos":
            self._build_insumos_module(tab, module_name, description)
            return
        if module_name == "Requisicoes":
            self._build_requisicoes_module(tab, module_name, description)
            return
        if module_name == "Emprestimos":
            self._build_emprestimos_module(tab, module_name, description)
            return
        if module_name == "Chamados":
            self._build_chamados_module(tab, module_name, description)
            return

        ttk.Label(tab, text=module_name, style="Title.TLabel").pack(anchor="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").pack(anchor="w", pady=(4, 16))
        ttk.Label(
            tab,
            text="Este modulo esta pronto para receber as proximas funcionalidades.",
            style="Sub.TLabel",
        ).pack(anchor="w")

    def _build_users_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar usuario",
            command=lambda: self._open_form_dialog(
                "Cadastrar usuario",
                [
                    ("Departamento", "departamento"),
                    ("Nome completo", "nome"),
                ],
                self._register_user,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")
        ttk.Button(
            tab,
            text="Grupos",
            command=self._open_user_groups_dialog,
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="e")

        columns = ("departamento", "nome", "perfil")
        users_table_frame = ttk.Frame(tab, style="Card.TFrame")
        users_table_frame.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        users_table_frame.columnconfigure(0, weight=1)
        users_table_frame.rowconfigure(0, weight=1)

        self.users_table = ttk.Treeview(users_table_frame, columns=columns, show="headings", height=12)
        self._users_sort_reverse = {column: False for column in columns}
        self.users_table.heading(
            "departamento",
            text="Departamento",
            command=lambda: self._sort_users_table("departamento"),
        )
        self.users_table.heading(
            "nome",
            text="Nome completo",
            command=lambda: self._sort_users_table("nome"),
        )
        self.users_table.heading(
            "perfil",
            text="Grupos",
            command=lambda: self._sort_users_table("perfil"),
        )
        self.users_table.column("departamento", width=180)
        self.users_table.column("nome", width=320)
        self.users_table.column("perfil", width=260)
        self.users_table.grid(row=0, column=0, sticky="nsew")

        users_scroll = ttk.Scrollbar(users_table_frame, orient="vertical", command=self.users_table.yview)
        users_scroll.grid(row=0, column=1, sticky="ns")
        self.users_table.configure(yscrollcommand=users_scroll.set)
        self._refresh_users_table()

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_user(self, new_user: dict[str, str]) -> bool:
        if not new_user.get("departamento") or not new_user.get("nome"):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha departamento e nome completo.",
            )
            return False

        # Mantem compatibilidade com o schema atual do banco.
        user_to_save = {
            "departamento": new_user["departamento"],
            "nome": new_user["nome"],
            "perfil": "",
            "username": "",
            "senha": "",
            "telefone": "",
            "ramal": "",
            "email": "",
        }

        self.db.insert_row("users", user_to_save)
        self.users_data = self.db.fetch_rows(
            "users",
            ("id", "departamento", "nome", "perfil", "username", "senha", "telefone", "ramal", "email"),
        )
        self._sync_user_group_labels()
        self._refresh_users_table()
        return True

    def _refresh_users_table(self) -> None:
        if not hasattr(self, "users_table"):
            return
        self.users_table.delete(*self.users_table.get_children())
        for user in self.users_data:
            self.users_table.insert(
                "",
                "end",
                values=(
                    user["departamento"],
                    user["nome"],
                    user.get("perfil", ""),
                ),
            )

    def _sort_users_table(self, column: str) -> None:
        if not hasattr(self, "users_table"):
            return
        rows = [
            (self.users_table.set(item_id, column).lower(), item_id)
            for item_id in self.users_table.get_children("")
        ]
        reverse = self._users_sort_reverse.get(column, False)
        rows.sort(reverse=reverse)
        for index, (_value, item_id) in enumerate(rows):
            self.users_table.move(item_id, "", index)
        self._users_sort_reverse[column] = not reverse

    def _open_user_groups_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Grupos de usuarios")
        width = 860
        height = 560
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg="#0A1B2A")
        dialog.transient(self)
        dialog.grab_set()
        dialog.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        pos_x = parent_x + (parent_w - width) // 2
        pos_y = parent_y + (parent_h - height) // 2
        dialog.geometry(f"{width}x{height}+{max(pos_x, 0)}+{max(pos_y, 0)}")

        root = ttk.Frame(dialog, style="Card.TFrame", padding=14)
        root.pack(fill="both", expand=True, padx=12, pady=12)
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(1, weight=1)

        left = ttk.Frame(root, style="Card.TFrame", padding=8)
        left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 8))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(2, weight=1)

        ttk.Label(left, text="Novo grupo", style="Sub.TLabel").grid(row=0, column=0, sticky="w")
        group_name_var = tk.StringVar()
        ttk.Entry(left, textvariable=group_name_var, font=("Segoe UI", 11)).grid(
            row=1, column=0, sticky="ew", pady=(4, 8)
        )

        groups_list = tk.Listbox(
            left,
            selectmode="browse",
            bg="#0D2336",
            fg="#EAF3F9",
            selectbackground="#227D74",
            selectforeground="#FFFFFF",
            font=("Segoe UI", 10),
            activestyle="none",
            highlightthickness=0,
            relief="flat",
        )
        groups_list.grid(row=2, column=0, sticky="nsew")

        right = ttk.Frame(root, style="Card.TFrame", padding=8)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)

        ttk.Label(right, text="Usuario", style="Sub.TLabel").grid(row=0, column=0, sticky="w")
        user_combo_var = tk.StringVar()
        user_combo = ttk.Combobox(right, textvariable=user_combo_var, state="readonly")
        user_combo.grid(row=1, column=0, sticky="ew", pady=(4, 8))

        members_frame = ttk.Frame(root, style="Card.TFrame", padding=8)
        members_frame.grid(row=1, column=1, sticky="nsew")
        members_frame.columnconfigure(0, weight=1)
        members_frame.rowconfigure(1, weight=1)
        ttk.Label(members_frame, text="Membros do grupo", style="Sub.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        members_list = tk.Listbox(
            members_frame,
            selectmode="browse",
            bg="#0D2336",
            fg="#EAF3F9",
            selectbackground="#227D74",
            selectforeground="#FFFFFF",
            font=("Segoe UI", 10),
            activestyle="none",
            highlightthickness=0,
            relief="flat",
        )
        members_list.grid(row=1, column=0, sticky="nsew")

        state = {
            "groups": [],
            "users": [],
            "selected_group_id": None,
            "user_map": {},
        }
        login_username_var = tk.StringVar()
        login_password_var = tk.StringVar()

        def refresh_groups() -> None:
            groups = self.db.fetch_user_groups()
            state["groups"] = groups
            groups_list.delete(0, tk.END)
            for item in groups:
                groups_list.insert(tk.END, item["nome"])

        def refresh_users() -> None:
            users = self.db.fetch_rows("users", ("id", "departamento", "nome", "perfil", "username", "senha"))
            state["users"] = users
            display = []
            user_map = {}
            for item in users:
                label = f"{item['nome']} ({item['departamento']}) [id:{item['id']}]"
                display.append(label)
                user_map[label] = int(item["id"])
            state["user_map"] = user_map
            user_combo["values"] = display
            if display:
                user_combo.current(0)
                load_user_credentials()

        def refresh_members() -> None:
            members_list.delete(0, tk.END)
            group_id = state["selected_group_id"]
            if not group_id:
                return
            for member in self.db.fetch_group_members(group_id):
                members_list.insert(
                    tk.END,
                    f"{member['nome']} - {member['departamento']} ({member.get('perfil', '')})",
                )

        def add_group() -> None:
            group_name = group_name_var.get().strip()
            if not group_name:
                messagebox.showwarning("Campo obrigatorio", "Informe o nome do grupo.")
                return
            if not self.db.add_user_group(group_name):
                messagebox.showwarning("Grupo existente", "Este grupo ja foi cadastrado.")
                return
            group_name_var.set("")
            refresh_groups()

        def select_group(_event=None) -> None:
            idx = groups_list.curselection()
            if not idx:
                state["selected_group_id"] = None
                refresh_members()
                return
            selected = state["groups"][idx[0]]
            state["selected_group_id"] = int(selected["id"])
            refresh_members()

        def add_user_to_group() -> None:
            group_id = state["selected_group_id"]
            if not group_id:
                messagebox.showwarning("Selecao obrigatoria", "Selecione um grupo.")
                return
            user_label = user_combo_var.get().strip()
            user_id = state["user_map"].get(user_label)
            if not user_id:
                messagebox.showwarning("Selecao obrigatoria", "Selecione um usuario.")
                return
            if not self.db.assign_user_to_group(group_id, user_id):
                messagebox.showwarning("Ja vinculado", "Usuario ja esta neste grupo.")
                return
            refresh_members()
            self._sync_user_group_labels()
            self._refresh_users_table()

        def load_user_credentials(_event=None) -> None:
            user_label = user_combo_var.get().strip()
            user_id = state["user_map"].get(user_label)
            if not user_id:
                login_username_var.set("")
                login_password_var.set("")
                return
            selected_user = next((user for user in state["users"] if int(user["id"]) == int(user_id)), None)
            if not selected_user:
                login_username_var.set("")
                login_password_var.set("")
                return
            login_username_var.set(selected_user.get("username", ""))
            login_password_var.set(selected_user.get("senha", ""))

        def save_user_credentials() -> None:
            user_label = user_combo_var.get().strip()
            user_id = state["user_map"].get(user_label)
            if not user_id:
                messagebox.showwarning("Selecao obrigatoria", "Selecione um usuario.")
                return
            username = login_username_var.get().strip()
            password = login_password_var.get().strip()
            if not username or not password:
                messagebox.showwarning("Campos obrigatorios", "Preencha username e senha.")
                return
            if not self.db.set_user_credentials(user_id, username, password):
                messagebox.showwarning("Username em uso", "Este username ja esta cadastrado para outro usuario.")
                return
            messagebox.showinfo("Sucesso", "Credenciais salvas.")
            selected_label = user_label
            refresh_users()
            if selected_label in state["user_map"]:
                user_combo_var.set(selected_label)
            self.users_data = self.db.fetch_rows(
                "users",
                ("id", "departamento", "nome", "perfil", "username", "senha", "telefone", "ramal", "email"),
            )
            self._sync_user_group_labels()
            self._refresh_users_table()

        ttk.Button(left, text="Cadastrar grupo", style="Action.TButton", command=add_group).grid(
            row=3, column=0, sticky="ew", pady=(8, 0)
        )
        ttk.Button(
            right,
            text="Vincular usuario ao grupo",
            style="Action.TButton",
            command=add_user_to_group,
        ).grid(row=2, column=0, sticky="w")
        ttk.Label(right, text="Username", style="Sub.TLabel").grid(row=3, column=0, sticky="w", pady=(10, 0))
        ttk.Entry(right, textvariable=login_username_var, font=("Segoe UI", 11)).grid(
            row=4, column=0, sticky="ew", pady=(4, 0)
        )
        ttk.Label(right, text="Senha", style="Sub.TLabel").grid(row=5, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(right, textvariable=login_password_var, show="*", font=("Segoe UI", 11)).grid(
            row=6, column=0, sticky="ew", pady=(4, 0)
        )
        ttk.Button(
            right,
            text="Salvar login do usuario",
            style="Action.TButton",
            command=save_user_credentials,
        ).grid(row=7, column=0, sticky="w", pady=(8, 0))

        groups_list.bind("<<ListboxSelect>>", select_group)
        user_combo.bind("<<ComboboxSelected>>", load_user_credentials)
        refresh_groups()
        refresh_users()

    def _build_access_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        actions = ttk.Frame(tab, style="Card.TFrame")
        actions.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        actions.columnconfigure(0, weight=1)
        ttk.Button(
            actions,
            text="Adicionar pasta",
            command=lambda: self._open_form_dialog(
                "Adicionar pasta de acesso",
                [("Pasta", "nome")],
                self._add_access_folder,
            ),
            style="Action.TButton",
        ).grid(row=0, column=0, sticky="w")

        list_frame = ttk.Frame(tab, style="Card.TFrame")
        list_frame.grid(row=3, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.access_listbox = tk.Listbox(
            list_frame,
            selectmode="extended",
            bg="#0D2336",
            fg="#EAF3F9",
            selectbackground="#227D74",
            selectforeground="#FFFFFF",
            font=("Segoe UI", 11),
            activestyle="none",
            highlightthickness=0,
            relief="flat",
        )
        self.access_listbox.grid(row=0, column=0, sticky="nsew")

        scroll = ttk.Scrollbar(list_frame, orient="vertical", command=self.access_listbox.yview)
        scroll.grid(row=0, column=1, sticky="ns")
        self.access_listbox.configure(yscrollcommand=scroll.set)

        ttk.Button(
            tab,
            text="Excluir pasta(s) selecionada(s)",
            command=self._remove_access_folders,
            style="Logout.TButton",
        ).grid(row=4, column=0, sticky="w", pady=(12, 0))

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
        self._refresh_access_list()

    def _refresh_access_list(self) -> None:
        self.access_listbox.delete(0, tk.END)
        for folder in self.access_folders:
            self.access_listbox.insert(tk.END, folder)

    def _add_access_folder(self, payload: dict[str, str]) -> bool:
        folder_name = payload["nome"].strip()
        if not folder_name:
            messagebox.showwarning("Campo obrigatorio", "Informe o nome da pasta.")
            return False
        if folder_name in self.access_folders:
            messagebox.showwarning("Pasta existente", "Esta pasta ja foi cadastrada.")
            return False

        self.db.add_access_folder(folder_name)
        self.access_folders.append(folder_name)
        self.access_folders.sort(key=str.lower)
        self._refresh_access_list()
        return True

    def _remove_access_folders(self) -> None:
        selected_indexes = self.access_listbox.curselection()
        if not selected_indexes:
            messagebox.showwarning("Selecao obrigatoria", "Selecione ao menos uma pasta.")
            return

        selected_folders = {self.access_listbox.get(index) for index in selected_indexes}
        self.db.remove_access_folders(list(selected_folders))
        self.access_folders = [folder for folder in self.access_folders if folder not in selected_folders]
        self._refresh_access_list()

    def _build_equipments_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar equipamento",
            command=lambda: self._open_form_dialog(
                "Cadastrar equipamento",
                [
                    ("ID interno", "id_interno"),
                    ("N? patrimonio", "patrimonio"),
                    ("Selo de patrimonio", "selo_patrimonio"),
                    ("Equipamento", "equipamento"),
                    ("Modelo", "modelo"),
                    ("Marca", "marca"),
                    ("Serie", "serie"),
                    ("Mem", "mem"),
                    ("Processador", "processador"),
                    ("Geracao", "geracao"),
                    ("HD", "hd"),
                    ("MOD HD", "mod_hd"),
                ],
                self._register_equipment,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = (
            "id_interno",
            "patrimonio",
            "selo_patrimonio",
            "equipamento",
            "modelo",
            "marca",
            "serie",
            "mem",
            "processador",
            "geracao",
            "hd",
            "mod_hd",
        )
        self.equipment_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.equipment_table.heading("id_interno", text="ID interno")
        self.equipment_table.heading("patrimonio", text="N? patrimonio")
        self.equipment_table.heading("selo_patrimonio", text="Selo patrimonio")
        self.equipment_table.heading("equipamento", text="Equipamento")
        self.equipment_table.heading("modelo", text="Modelo")
        self.equipment_table.heading("marca", text="Marca")
        self.equipment_table.heading("serie", text="Serie")
        self.equipment_table.heading("mem", text="Mem")
        self.equipment_table.heading("processador", text="Processador")
        self.equipment_table.heading("geracao", text="Geracao")
        self.equipment_table.heading("hd", text="HD")
        self.equipment_table.heading("mod_hd", text="MOD HD")

        self.equipment_table.column("id_interno", width=110)
        self.equipment_table.column("patrimonio", width=120)
        self.equipment_table.column("selo_patrimonio", width=130)
        self.equipment_table.column("equipamento", width=160)
        self.equipment_table.column("modelo", width=130)
        self.equipment_table.column("marca", width=120)
        self.equipment_table.column("serie", width=140)
        self.equipment_table.column("mem", width=100)
        self.equipment_table.column("processador", width=170)
        self.equipment_table.column("geracao", width=100)
        self.equipment_table.column("hd", width=100)
        self.equipment_table.column("mod_hd", width=120)
        self.equipment_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for equipment in self.equipment_data:
            self.equipment_table.insert(
                "",
                "end",
                values=(
                    equipment["id_interno"],
                    equipment["patrimonio"],
                    equipment["selo_patrimonio"],
                    equipment["equipamento"],
                    equipment["modelo"],
                    equipment["marca"],
                    equipment["serie"],
                    equipment["mem"],
                    equipment["processador"],
                    equipment["geracao"],
                    equipment["hd"],
                    equipment["mod_hd"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_equipment(self, equipment_row: dict[str, str]) -> bool:
        if not all(equipment_row.values()):
            messagebox.showwarning("Campos obrigatorios", "Preencha todos os campos do equipamento.")
            return False

        self.db.insert_row("equipments", equipment_row)
        self.equipment_data.append(equipment_row)
        self.equipment_table.insert(
            "",
            "end",
            values=(
                equipment_row["id_interno"],
                equipment_row["patrimonio"],
                equipment_row["selo_patrimonio"],
                equipment_row["equipamento"],
                equipment_row["modelo"],
                equipment_row["marca"],
                equipment_row["serie"],
                equipment_row["mem"],
                equipment_row["processador"],
                equipment_row["geracao"],
                equipment_row["hd"],
                equipment_row["mod_hd"],
            ),
        )
        return True

    def _build_ips_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar IP",
            command=lambda: self._open_form_dialog(
                "Cadastrar IP",
                [
                    ("IP", "ip"),
                    ("Nome", "nome"),
                    ("Fabricante", "fabricante"),
                    ("Endereco MAC", "endereco_mac"),
                ],
                self._register_ip,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = ("ip", "nome", "fabricante", "endereco_mac")
        self.ip_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.ip_table.heading("ip", text="IP")
        self.ip_table.heading("nome", text="Nome")
        self.ip_table.heading("fabricante", text="Fabricante")
        self.ip_table.heading("endereco_mac", text="Endereco MAC")

        self.ip_table.column("ip", width=160)
        self.ip_table.column("nome", width=260)
        self.ip_table.column("fabricante", width=240)
        self.ip_table.column("endereco_mac", width=240)
        self.ip_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for ip_row in self.ip_data:
            self.ip_table.insert(
                "",
                "end",
                values=(ip_row["ip"], ip_row["nome"], ip_row["fabricante"], ip_row["endereco_mac"]),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_ip(self, ip_row: dict[str, str]) -> bool:
        if not all(ip_row.values()):
            messagebox.showwarning("Campos obrigatorios", "Preencha IP, nome, fabricante e endereco MAC.")
            return False

        self.db.insert_row("ips", ip_row)
        self.ip_data.append(ip_row)
        self.ip_table.insert(
            "",
            "end",
            values=(ip_row["ip"], ip_row["nome"], ip_row["fabricante"], ip_row["endereco_mac"]),
        )
        return True

    def _build_emails_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar email",
            command=lambda: self._open_form_dialog(
                "Cadastrar email",
                [
                    ("Nro", "nro"),
                    ("Nome", "nome"),
                    ("Sobrenome", "sobrenome"),
                    ("Email", "email"),
                    ("Grupo", "grupo"),
                    ("Situacao", "situacao"),
                ],
                self._register_email,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = ("nro", "nome", "sobrenome", "email", "grupo", "situacao")
        self.email_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.email_table.heading("nro", text="Nro")
        self.email_table.heading("nome", text="Nome")
        self.email_table.heading("sobrenome", text="Sobrenome")
        self.email_table.heading("email", text="Email")
        self.email_table.heading("grupo", text="Grupo")
        self.email_table.heading("situacao", text="Situacao")

        self.email_table.column("nro", width=80)
        self.email_table.column("nome", width=170)
        self.email_table.column("sobrenome", width=180)
        self.email_table.column("email", width=260)
        self.email_table.column("grupo", width=180)
        self.email_table.column("situacao", width=120)
        self.email_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for email_row in self.email_data:
            self.email_table.insert(
                "",
                "end",
                values=(
                    email_row["nro"],
                    email_row["nome"],
                    email_row["sobrenome"],
                    email_row["email"],
                    email_row["grupo"],
                    email_row["situacao"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_email(self, email_row: dict[str, str]) -> bool:
        if not all(email_row.values()):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha Nro, nome, sobrenome, email, grupo e situacao.",
            )
            return False

        self.db.insert_row("emails", email_row)
        self.email_data.append(email_row)
        self.email_table.insert(
            "",
            "end",
            values=(
                email_row["nro"],
                email_row["nome"],
                email_row["sobrenome"],
                email_row["email"],
                email_row["grupo"],
                email_row["situacao"],
            ),
        )
        return True

    def _build_ramais_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar ramal",
            command=lambda: self._open_form_dialog(
                "Cadastrar ramal",
                [
                    ("Nro", "nro"),
                    ("Nome", "nome"),
                    ("Sobrenome", "sobrenome"),
                    ("Email", "email"),
                    ("Grupo", "grupo"),
                    ("Situacao", "situacao"),
                ],
                self._register_ramal,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = ("nro", "nome", "sobrenome", "email", "grupo", "situacao")
        self.ramal_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.ramal_table.heading("nro", text="Nro")
        self.ramal_table.heading("nome", text="Nome")
        self.ramal_table.heading("sobrenome", text="Sobrenome")
        self.ramal_table.heading("email", text="Email")
        self.ramal_table.heading("grupo", text="Grupo")
        self.ramal_table.heading("situacao", text="Situacao")

        self.ramal_table.column("nro", width=80)
        self.ramal_table.column("nome", width=170)
        self.ramal_table.column("sobrenome", width=180)
        self.ramal_table.column("email", width=260)
        self.ramal_table.column("grupo", width=180)
        self.ramal_table.column("situacao", width=120)
        self.ramal_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for ramal_row in self.ramal_data:
            self.ramal_table.insert(
                "",
                "end",
                values=(
                    ramal_row["nro"],
                    ramal_row["nome"],
                    ramal_row["sobrenome"],
                    ramal_row["email"],
                    ramal_row["grupo"],
                    ramal_row["situacao"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_ramal(self, ramal_row: dict[str, str]) -> bool:
        if not all(ramal_row.values()):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha Nro, nome, sobrenome, email, grupo e situacao.",
            )
            return False

        self.db.insert_row("ramais", ramal_row)
        self.ramal_data.append(ramal_row)
        self.ramal_table.insert(
            "",
            "end",
            values=(
                ramal_row["nro"],
                ramal_row["nome"],
                ramal_row["sobrenome"],
                ramal_row["email"],
                ramal_row["grupo"],
                ramal_row["situacao"],
            ),
        )
        return True

    def _build_softwares_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar software",
            command=lambda: self._open_form_dialog(
                "Cadastrar software",
                [
                    ("Nome", "nome"),
                    ("Computador", "computador"),
                    ("Setor", "setor"),
                    ("Serial", "serial"),
                    ("Conta", "conta"),
                ],
                self._register_software,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = ("nome", "computador", "setor", "serial", "conta")
        self.software_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.software_table.heading("nome", text="Nome")
        self.software_table.heading("computador", text="Computador")
        self.software_table.heading("setor", text="Setor")
        self.software_table.heading("serial", text="Serial")
        self.software_table.heading("conta", text="Conta")

        self.software_table.column("nome", width=200)
        self.software_table.column("computador", width=220)
        self.software_table.column("setor", width=180)
        self.software_table.column("serial", width=220)
        self.software_table.column("conta", width=220)
        self.software_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for software_row in self.software_data:
            self.software_table.insert(
                "",
                "end",
                values=(
                    software_row["nome"],
                    software_row["computador"],
                    software_row["setor"],
                    software_row["serial"],
                    software_row["conta"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_software(self, software_row: dict[str, str]) -> bool:
        if not all(software_row.values()):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha nome, computador, setor, serial e conta.",
            )
            return False

        self.db.insert_row("softwares", software_row)
        self.software_data.append(software_row)
        self.software_table.insert(
            "",
            "end",
            values=(
                software_row["nome"],
                software_row["computador"],
                software_row["setor"],
                software_row["serial"],
                software_row["conta"],
            ),
        )
        return True

    def _build_insumos_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar insumo",
            command=lambda: self._open_form_dialog(
                "Cadastrar insumo",
                [
                    ("Insumo", "insumo"),
                    ("Data", "data"),
                    ("Qtd", "qtd"),
                    ("Nome", "nome"),
                    ("Departamento", "departamento"),
                ],
                self._register_insumo,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = ("insumo", "data", "qtd", "nome", "departamento")
        self.insumo_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.insumo_table.heading("insumo", text="Insumo")
        self.insumo_table.heading("data", text="Data")
        self.insumo_table.heading("qtd", text="Qtd")
        self.insumo_table.heading("nome", text="Nome")
        self.insumo_table.heading("departamento", text="Departamento")

        self.insumo_table.column("insumo", width=220)
        self.insumo_table.column("data", width=120)
        self.insumo_table.column("qtd", width=90)
        self.insumo_table.column("nome", width=220)
        self.insumo_table.column("departamento", width=220)
        self.insumo_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for insumo_row in self.insumo_data:
            self.insumo_table.insert(
                "",
                "end",
                values=(
                    insumo_row["insumo"],
                    insumo_row["data"],
                    insumo_row["qtd"],
                    insumo_row["nome"],
                    insumo_row["departamento"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_insumo(self, insumo_row: dict[str, str]) -> bool:
        if not all(insumo_row.values()):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha insumo, data, qtd, nome e departamento.",
            )
            return False

        self.db.insert_row("insumos", insumo_row)
        self.insumo_data.append(insumo_row)
        self.insumo_table.insert(
            "",
            "end",
            values=(
                insumo_row["insumo"],
                insumo_row["data"],
                insumo_row["qtd"],
                insumo_row["nome"],
                insumo_row["departamento"],
            ),
        )
        return True

    def _build_requisicoes_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar requisicao",
            command=lambda: self._open_form_dialog(
                "Cadastrar requisicao",
                [
                    ("Solicitacao", "solicitacao"),
                    ("Qtd", "qtd"),
                    ("Valor", "valor"),
                    ("Total", "total"),
                    ("Data requisitado", "requisitado"),
                    ("Aprovado", "aprovado", ("Sim", "Nao", "Esperando")),
                    ("Data recebido", "recebido"),
                    ("NF", "nf"),
                    ("Tipo", "tipo"),
                    ("Fornecedor", "fornecedor"),
                    ("Link", "link"),
                ],
                self._register_requisicao,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = (
            "solicitacao",
            "qtd",
            "valor",
            "total",
            "requisitado",
            "aprovado",
            "recebido",
            "nf",
            "tipo",
            "fornecedor",
            "link",
        )
        self.requisicao_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.requisicao_table.heading("solicitacao", text="Solicitacao")
        self.requisicao_table.heading("qtd", text="Qtd")
        self.requisicao_table.heading("valor", text="Valor")
        self.requisicao_table.heading("total", text="Total")
        self.requisicao_table.heading("requisitado", text="Requisitado")
        self.requisicao_table.heading("aprovado", text="Aprovado")
        self.requisicao_table.heading("recebido", text="Recebido")
        self.requisicao_table.heading("nf", text="NF")
        self.requisicao_table.heading("tipo", text="Tipo")
        self.requisicao_table.heading("fornecedor", text="Fornecedor")
        self.requisicao_table.heading("link", text="Link")

        self.requisicao_table.column("solicitacao", width=260)
        self.requisicao_table.column("qtd", width=70)
        self.requisicao_table.column("valor", width=90)
        self.requisicao_table.column("total", width=90)
        self.requisicao_table.column("requisitado", width=110)
        self.requisicao_table.column("aprovado", width=95)
        self.requisicao_table.column("recebido", width=95)
        self.requisicao_table.column("nf", width=80)
        self.requisicao_table.column("tipo", width=120)
        self.requisicao_table.column("fornecedor", width=180)
        self.requisicao_table.column("link", width=220)
        self.requisicao_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for requisicao_row in self.requisicao_data:
            self.requisicao_table.insert(
                "",
                "end",
                values=(
                    requisicao_row["solicitacao"],
                    requisicao_row["qtd"],
                    requisicao_row["valor"],
                    requisicao_row["total"],
                    requisicao_row["requisitado"],
                    requisicao_row["aprovado"],
                    requisicao_row["recebido"],
                    requisicao_row["nf"],
                    requisicao_row["tipo"],
                    requisicao_row["fornecedor"],
                    requisicao_row["link"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_requisicao(self, requisicao_row: dict[str, str]) -> bool:
        if not all(requisicao_row.values()):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha todos os campos da requisicao (sem aprovado2).",
            )
            return False

        self.db.insert_row("requisicoes", requisicao_row)
        self.requisicao_data.append(requisicao_row)
        self.requisicao_table.insert(
            "",
            "end",
            values=(
                requisicao_row["solicitacao"],
                requisicao_row["qtd"],
                requisicao_row["valor"],
                requisicao_row["total"],
                requisicao_row["requisitado"],
                requisicao_row["aprovado"],
                requisicao_row["recebido"],
                requisicao_row["nf"],
                requisicao_row["tipo"],
                requisicao_row["fornecedor"],
                requisicao_row["link"],
            ),
        )
        return True

    def _build_emprestimos_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 18)
        )

        ttk.Button(
            tab,
            text="Cadastrar emprestimo",
            command=lambda: self._open_form_dialog(
                "Cadastrar emprestimo",
                [
                    ("Nome", "nome"),
                    ("Equipamento", "equipamento"),
                    ("Documento", "documento"),
                    ("Arquivo", "arquivo"),
                    ("Situacao", "situacao"),
                    ("Data", "data"),
                ],
                self._register_emprestimo,
            ),
            style="Action.TButton",
        ).grid(row=2, column=0, sticky="w")

        columns = ("nome", "equipamento", "documento", "arquivo", "situacao", "data")
        self.emprestimo_table = ttk.Treeview(tab, columns=columns, show="headings", height=12)
        self.emprestimo_table.heading("nome", text="Nome")
        self.emprestimo_table.heading("equipamento", text="Equipamento")
        self.emprestimo_table.heading("documento", text="Documento")
        self.emprestimo_table.heading("arquivo", text="Arquivo")
        self.emprestimo_table.heading("situacao", text="Situacao")
        self.emprestimo_table.heading("data", text="Data")

        self.emprestimo_table.column("nome", width=220)
        self.emprestimo_table.column("equipamento", width=220)
        self.emprestimo_table.column("documento", width=160)
        self.emprestimo_table.column("arquivo", width=260)
        self.emprestimo_table.column("situacao", width=120)
        self.emprestimo_table.column("data", width=120)
        self.emprestimo_table.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        for emprestimo_row in self.emprestimo_data:
            self.emprestimo_table.insert(
                "",
                "end",
                values=(
                    emprestimo_row["nome"],
                    emprestimo_row["equipamento"],
                    emprestimo_row["documento"],
                    emprestimo_row["arquivo"],
                    emprestimo_row["situacao"],
                    emprestimo_row["data"],
                ),
            )

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)

    def _register_emprestimo(self, emprestimo_row: dict[str, str]) -> bool:
        if not all(emprestimo_row.values()):
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha nome, equipamento, documento, arquivo, situacao e data.",
            )
            return False

        self.db.insert_row("emprestimos", emprestimo_row)
        self.emprestimo_data.append(emprestimo_row)
        self.emprestimo_table.insert(
            "",
            "end",
            values=(
                emprestimo_row["nome"],
                emprestimo_row["equipamento"],
                emprestimo_row["documento"],
                emprestimo_row["arquivo"],
                emprestimo_row["situacao"],
                emprestimo_row["data"],
            ),
        )
        return True

    def _build_chamados_module(self, tab: ttk.Frame, module_name: str, description: str) -> None:
        ttk.Label(tab, text=module_name, style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(tab, text=description, style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 14)
        )

        actions = ttk.Frame(tab, style="Card.TFrame")
        actions.grid(row=2, column=0, sticky="ew", pady=(0, 12))
        ttk.Button(
            actions,
            text="Abrir novo chamado",
            style="Action.TButton",
            command=self._open_new_chamado_dialog,
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(
            actions,
            text="Chamados finalizados",
            style="Logout.TButton",
            command=self._finalize_selected_chamado,
        ).grid(row=0, column=1, sticky="w", padx=(8, 0))

        board = ttk.Frame(tab, style="Card.TFrame")
        board.grid(row=3, column=0, sticky="nsew")
        ti_users = self._get_ti_group_users()
        columns = [("pendente", "Chamados pendentes")] + [
            (f"user_{user['id']}", user["nome"]) for user in ti_users
        ]
        for idx in range(len(columns)):
            board.columnconfigure(idx, weight=1)
        board.rowconfigure(0, weight=1)

        self.chamado_lists = {}
        self._chamado_list_to_status = {}
        self._chamado_selected_id = None
        self._chamado_drag = None
        self._chamado_assignee_lookup = {
            user["nome"].strip().lower(): f"user_{user['id']}" for user in ti_users
        }

        for col_index, (status_key, title) in enumerate(columns):
            column_frame = ttk.Frame(board, style="Card.TFrame", padding=8)
            column_frame.grid(row=0, column=col_index, sticky="nsew", padx=4)
            column_frame.rowconfigure(1, weight=1)
            column_frame.columnconfigure(0, weight=1)

            ttk.Label(column_frame, text=title, style="PanelTitle.TLabel").grid(
                row=0, column=0, sticky="w", pady=(0, 6)
            )

            list_frame = ttk.Frame(column_frame, style="Card.TFrame")
            list_frame.grid(row=1, column=0, sticky="nsew")
            list_frame.rowconfigure(0, weight=1)
            list_frame.columnconfigure(0, weight=1)

            listbox = tk.Listbox(
                list_frame,
                selectmode="browse",
                bg="#0D2336",
                fg="#EAF3F9",
                selectbackground="#227D74",
                selectforeground="#FFFFFF",
                font=("Segoe UI", 10),
                activestyle="none",
                highlightthickness=0,
                relief="flat",
            )
            listbox.grid(row=0, column=0, sticky="nsew")
            scroll = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
            scroll.grid(row=0, column=1, sticky="ns")
            listbox.configure(yscrollcommand=scroll.set)

            listbox.bind("<<ListboxSelect>>", self._on_chamado_select)
            listbox.bind("<ButtonPress-1>", self._on_chamado_press)
            listbox.bind("<ButtonRelease-1>", self._on_chamado_release)
            listbox.bind("<Double-Button-1>", self._on_chamado_double_click)

            self.chamado_lists[status_key] = listbox
            self._chamado_list_to_status[listbox] = status_key

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(3, weight=1)
        self._refresh_chamado_board()

    def _refresh_chamado_board(self) -> None:
        for listbox in self.chamado_lists.values():
            listbox.delete(0, tk.END)

        for chamado in self.chamado_data:
            status = self._resolve_chamado_status(chamado)
            if status not in self.chamado_lists:
                status = "pendente"
            item_label = f"{chamado['id']} - [{chamado.get('urgencia', '')}] {chamado['titulo']}"
            self.chamado_lists[status].insert(tk.END, item_label)

    def _get_ti_group_users(self) -> list[dict[str, str]]:
        groups = self.db.fetch_user_groups()
        ti_group = next((group for group in groups if group["nome"].strip().lower() == "ti"), None)
        if not ti_group:
            return []
        users = self.db.fetch_group_members(int(ti_group["id"]))
        users.sort(key=lambda user: user["nome"].lower())
        return users

    def _is_current_user_in_ti_group(self) -> bool:
        current_name = self.current_user.get().strip().lower()
        if not current_name:
            return False
        return any(user["nome"].strip().lower() == current_name for user in self._get_ti_group_users())

    def _resolve_chamado_status(self, chamado: dict[str, str]) -> str:
        raw_status = str(chamado.get("status", "pendente")).strip().lower()
        if raw_status in self.chamado_lists:
            return raw_status
        mapped = self._chamado_assignee_lookup.get(raw_status)
        if mapped and mapped in self.chamado_lists:
            return mapped
        return "pendente"

    def _import_legacy_chamados(self) -> None:
        default_path = "dbchamados antigos.sqlite3"
        legacy_path = default_path
        try:
            open(legacy_path, "rb").close()
        except OSError:
            legacy_path = filedialog.askopenfilename(
                title="Selecione o banco antigo de chamados",
                filetypes=[("SQLite", "*.sqlite3 *.db"), ("Todos os arquivos", "*.*")],
            )
            if not legacy_path:
                return

        imported, skipped = self.db.import_legacy_chamados(legacy_path)
        self.chamado_data = self.db.fetch_rows(
            "chamados",
            (
                "id",
                "titulo",
                "descricao",
                "autor",
                "tipo",
                "urgencia",
                "arquivo",
                "status",
                "legacy_source",
                "legacy_id",
            ),
        )
        self._refresh_chamado_board()
        messagebox.showinfo(
            "Importacao concluida",
            f"Chamados importados: {imported}\nChamados ja existentes: {skipped}",
        )

    def _register_chamado(self, chamado_row: dict[str, str]) -> bool:
        titulo = chamado_row.get("titulo", "").strip()
        descricao = chamado_row.get("descricao", "").strip()
        tipo = chamado_row.get("tipo", "").strip()
        urgencia = chamado_row.get("urgencia", "").strip()
        arquivo = chamado_row.get("arquivo", "").strip()
        autor = self.current_user.get().strip() or "Administrador"
        if not titulo or not descricao or not tipo or not urgencia:
            messagebox.showwarning(
                "Campos obrigatorios",
                "Preencha titulo, descricao, tipo e urgencia.",
            )
            return False

        new_id = self.db.insert_chamado(
            titulo,
            descricao,
            autor,
            tipo,
            urgencia,
            arquivo,
            "pendente",
        )
        self.chamado_data.append(
            {
                "id": new_id,
                "titulo": titulo,
                "descricao": descricao,
                "autor": autor,
                "tipo": tipo,
                "urgencia": urgencia,
                "arquivo": arquivo,
                "status": "pendente",
            }
        )
        self._refresh_chamado_board()
        return True

    def _open_new_chamado_dialog(self) -> None:
        dialog = tk.Toplevel(self)
        dialog.title("Novo chamado")
        width = 620
        height = 520
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg="#0A1B2A")
        dialog.transient(self)
        dialog.grab_set()
        dialog.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        pos_x = parent_x + (parent_w - width) // 2
        pos_y = parent_y + (parent_h - height) // 2
        dialog.geometry(f"{width}x{height}+{max(pos_x, 0)}+{max(pos_y, 0)}")

        form = ttk.Frame(dialog, style="Card.TFrame", padding=18)
        form.pack(fill="both", expand=True, padx=12, pady=12)
        form.columnconfigure(1, weight=1)

        values = {
            "titulo": tk.StringVar(),
            "descricao": tk.StringVar(),
            "tipo": tk.StringVar(),
            "urgencia": tk.StringVar(),
            "arquivo": tk.StringVar(),
        }

        ttk.Label(form, text="Titulo", style="Sub.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
        )
        entry_titulo = ttk.Entry(form, textvariable=values["titulo"], font=("Segoe UI", 11))
        entry_titulo.grid(row=0, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(form, text="Descricao", style="Sub.TLabel").grid(
            row=1, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
        )
        ttk.Entry(form, textvariable=values["descricao"], font=("Segoe UI", 11)).grid(
            row=1, column=1, sticky="ew", pady=(0, 8)
        )

        ttk.Label(form, text="Tipo", style="Sub.TLabel").grid(
            row=2, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
        )
        ttk.Combobox(
            form,
            textvariable=values["tipo"],
            values=("Incidente", "Solicitacao", "Melhoria", "Programado"),
            state="readonly",
            font=("Segoe UI", 11),
        ).grid(row=2, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(form, text="Urgencia", style="Sub.TLabel").grid(
            row=3, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
        )
        ttk.Combobox(
            form,
            textvariable=values["urgencia"],
            values=("Normal", "Baixa", "Media", "Alta", "Urgente"),
            state="readonly",
            font=("Segoe UI", 11),
        ).grid(row=3, column=1, sticky="ew", pady=(0, 8))

        ttk.Label(form, text="Arquivo", style="Sub.TLabel").grid(
            row=4, column=0, sticky="w", padx=(0, 10), pady=(0, 8)
        )
        file_row = ttk.Frame(form, style="Card.TFrame")
        file_row.grid(row=4, column=1, sticky="ew", pady=(0, 8))
        file_row.columnconfigure(0, weight=1)
        ttk.Entry(file_row, textvariable=values["arquivo"], font=("Segoe UI", 11)).grid(
            row=0, column=0, sticky="ew"
        )

        def select_file() -> None:
            file_path = filedialog.askopenfilename(
                title="Selecionar arquivo do chamado",
                filetypes=[("Todos os arquivos", "*.*")],
            )
            if file_path:
                values["arquivo"].set(file_path)

        ttk.Button(file_row, text="Anexar", style="Action.TButton", command=select_file).grid(
            row=0, column=1, sticky="w", padx=(8, 0)
        )

        actions = ttk.Frame(form, style="Card.TFrame")
        actions.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        actions.columnconfigure(0, weight=1)

        def clear_form() -> None:
            for var in values.values():
                var.set("")
            entry_titulo.focus_set()

        def submit(close_after_save: bool) -> None:
            payload = {key: var.get().strip() for key, var in values.items()}
            if self._register_chamado(payload):
                if close_after_save:
                    dialog.destroy()
                else:
                    clear_form()

        ttk.Button(
            actions,
            text="Salvar",
            style="Action.TButton",
            command=lambda: submit(True),
        ).grid(row=0, column=1, sticky="e")
        ttk.Button(
            actions,
            text="Salvar e cadastrar outro",
            style="Action.TButton",
            command=lambda: submit(False),
        ).grid(row=0, column=2, sticky="e", padx=(8, 0))

        entry_titulo.focus_set()

    def _on_chamado_select(self, event) -> None:
        listbox = event.widget
        selection = listbox.curselection()
        if not selection:
            self._chamado_selected_id = None
            return
        item_text = listbox.get(selection[0])
        chamado_id = int(item_text.split(" - ", 1)[0])
        self._chamado_selected_id = chamado_id

    def _on_chamado_press(self, event) -> None:
        listbox = event.widget
        index = listbox.nearest(event.y)
        if index < 0 or index >= listbox.size():
            self._chamado_drag = None
            return
        item_text = listbox.get(index)
        chamado_id = int(item_text.split(" - ", 1)[0])
        source_status = self._chamado_list_to_status[listbox]
        self._chamado_drag = {"id": chamado_id, "source_status": source_status}
        self._chamado_selected_id = chamado_id

    def _on_chamado_release(self, event) -> None:
        if not self._chamado_drag:
            return
        target_widget = event.widget.winfo_containing(event.x_root, event.y_root)
        while target_widget and target_widget not in self._chamado_list_to_status:
            target_widget = target_widget.master
        if not target_widget:
            self._chamado_drag = None
            return

        target_status = self._chamado_list_to_status[target_widget]
        source_status = self._chamado_drag["source_status"]
        chamado_id = self._chamado_drag["id"]
        self._chamado_drag = None

        if source_status == target_status:
            return
        self._move_chamado_to_status(chamado_id, target_status)

    def _on_chamado_double_click(self, event) -> None:
        listbox = event.widget
        index = listbox.nearest(event.y)
        if index < 0 or index >= listbox.size():
            return
        item_text = listbox.get(index)
        chamado_id = int(item_text.split(" - ", 1)[0])
        self._open_chamado_details(chamado_id)

    def _open_chamado_details(self, chamado_id: int) -> None:
        chamado = next((c for c in self.chamado_data if int(c["id"]) == int(chamado_id)), None)
        if not chamado:
            return

        dialog = tk.Toplevel(self)
        dialog.title(f"Detalhes do chamado #{chamado_id}")
        width = 980
        height = 720
        dialog.geometry(f"{width}x{height}")
        dialog.configure(bg="#0A1B2A")
        dialog.transient(self)
        dialog.grab_set()
        dialog.update_idletasks()

        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_w = self.winfo_width()
        parent_h = self.winfo_height()
        pos_x = parent_x + (parent_w - width) // 2
        pos_y = parent_y + (parent_h - height) // 2
        dialog.geometry(f"{width}x{height}+{max(pos_x, 0)}+{max(pos_y, 0)}")

        frame = ttk.Frame(dialog, style="Card.TFrame", padding=14)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(6, weight=1)
        frame.rowconfigure(7, weight=1)

        details = [
            ("Titulo", chamado.get("titulo", "")),
            ("Autor", chamado.get("autor", "") or "-"),
            ("Status", chamado.get("status", "")),
            ("Tipo", chamado.get("tipo", "")),
            ("Urgencia", chamado.get("urgencia", "")),
            ("Arquivo", chamado.get("arquivo", "")),
        ]
        for row, (label, value) in enumerate(details):
            ttk.Label(frame, text=label, style="Sub.TLabel").grid(
                row=row, column=0, sticky="nw", padx=(0, 10), pady=(0, 6)
            )
            ttk.Label(frame, text=value or "-", style="Sub.TLabel", wraplength=700).grid(
                row=row, column=1, sticky="nw", pady=(0, 6)
            )

        ttk.Label(frame, text="Descricao", style="Sub.TLabel").grid(
            row=6, column=0, sticky="nw", padx=(0, 10), pady=(2, 6)
        )
        desc = tk.Text(
            frame,
            height=5,
            wrap="word",
            bg="#0D2336",
            fg="#EAF3F9",
            font=("Segoe UI", 10),
            relief="flat",
            highlightthickness=0,
        )
        desc.grid(row=6, column=1, sticky="nsew", pady=(2, 6))
        desc.insert("1.0", chamado.get("descricao", ""))
        desc.configure(state="disabled")

        chats = ttk.Frame(frame, style="Card.TFrame")
        chats.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=(6, 0))
        chats.columnconfigure(0, weight=1)
        chats.columnconfigure(1, weight=1)
        chats.rowconfigure(1, weight=1)

        current_author = self.current_user.get().strip() or "Administrador"

        # Chat publico (solicitante e TI veem)
        ttk.Label(chats, text="Chat publico", style="PanelTitle.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )
        public_text = tk.Text(
            chats,
            wrap="word",
            bg="#0D2336",
            fg="#EAF3F9",
            font=("Segoe UI", 10),
            relief="flat",
            highlightthickness=0,
        )
        public_text.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        public_text.configure(state="disabled")

        public_input = ttk.Frame(chats, style="Card.TFrame")
        public_input.grid(row=2, column=0, sticky="ew", padx=(0, 8), pady=(6, 0))
        public_input.columnconfigure(0, weight=1)
        public_message_var = tk.StringVar()
        public_file_var = tk.StringVar()
        ttk.Entry(public_input, textvariable=public_message_var, font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Entry(public_input, textvariable=public_file_var, font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="ew", pady=(4, 0)
        )

        def pick_public_file() -> None:
            path = filedialog.askopenfilename(title="Anexar arquivo (chat publico)")
            if path:
                public_file_var.set(path)

        ttk.Button(public_input, text="Anexar", style="Action.TButton", command=pick_public_file).grid(
            row=1, column=1, padx=(6, 0), pady=(4, 0)
        )

        # Chat interno TI (apenas TI)
        ttk.Label(chats, text="Chat interno TI", style="PanelTitle.TLabel").grid(
            row=0, column=1, sticky="w", pady=(0, 6)
        )
        interno_text = tk.Text(
            chats,
            wrap="word",
            bg="#0D2336",
            fg="#EAF3F9",
            font=("Segoe UI", 10),
            relief="flat",
            highlightthickness=0,
        )
        interno_text.grid(row=1, column=1, sticky="nsew")
        interno_text.configure(state="disabled")

        interno_input = ttk.Frame(chats, style="Card.TFrame")
        interno_input.grid(row=2, column=1, sticky="ew", pady=(6, 0))
        interno_input.columnconfigure(0, weight=1)
        interno_message_var = tk.StringVar()
        interno_file_var = tk.StringVar()
        ttk.Entry(interno_input, textvariable=interno_message_var, font=("Segoe UI", 10)).grid(
            row=0, column=0, sticky="ew"
        )
        ttk.Entry(interno_input, textvariable=interno_file_var, font=("Segoe UI", 10)).grid(
            row=1, column=0, sticky="ew", pady=(4, 0)
        )

        def pick_interno_file() -> None:
            path = filedialog.askopenfilename(title="Anexar arquivo (chat interno)")
            if path:
                interno_file_var.set(path)

        ttk.Button(interno_input, text="Anexar", style="Action.TButton", command=pick_interno_file).grid(
            row=1, column=1, padx=(6, 0), pady=(4, 0)
        )

        is_ti_user = self._is_current_user_in_ti_group()
        if not is_ti_user:
            interno_input.grid_remove()
            interno_text.configure(state="normal")
            interno_text.insert("1.0", "Apenas usuarios do grupo TI visualizam o chat interno.\n")
            interno_text.configure(state="disabled")

        def load_messages() -> None:
            public_msgs = self.db.fetch_chamado_messages(chamado_id, "publico")
            interno_msgs = self.db.fetch_chamado_messages(chamado_id, "interno")

            public_text.configure(state="normal")
            public_text.delete("1.0", tk.END)
            for msg in public_msgs:
                line = f"[{msg['criado_em']}] {msg['autor']}: {msg['mensagem']}\n"
                public_text.insert(tk.END, line)
                if msg.get("arquivo"):
                    public_text.insert(tk.END, f"  anexo: {msg['arquivo']}\n")
            public_text.configure(state="disabled")

            interno_text.configure(state="normal")
            if is_ti_user:
                interno_text.delete("1.0", tk.END)
                for msg in interno_msgs:
                    line = f"[{msg['criado_em']}] {msg['autor']}: {msg['mensagem']}\n"
                    interno_text.insert(tk.END, line)
                    if msg.get("arquivo"):
                        interno_text.insert(tk.END, f"  anexo: {msg['arquivo']}\n")
            interno_text.configure(state="disabled")

        def send_public() -> None:
            message = public_message_var.get().strip()
            file_path = public_file_var.get().strip()
            if not message:
                messagebox.showwarning("Campo obrigatorio", "Digite a mensagem no chat publico.")
                return
            self.db.add_chamado_message(chamado_id, "publico", current_author, message, file_path)
            public_message_var.set("")
            public_file_var.set("")
            load_messages()

        def send_interno() -> None:
            if not is_ti_user:
                return
            message = interno_message_var.get().strip()
            file_path = interno_file_var.get().strip()
            if not message:
                messagebox.showwarning("Campo obrigatorio", "Digite a mensagem no chat interno.")
                return
            self.db.add_chamado_message(chamado_id, "interno", current_author, message, file_path)
            interno_message_var.set("")
            interno_file_var.set("")
            load_messages()

        ttk.Button(public_input, text="Enviar", style="Action.TButton", command=send_public).grid(
            row=0, column=1, padx=(6, 0)
        )
        ttk.Button(interno_input, text="Enviar", style="Action.TButton", command=send_interno).grid(
            row=0, column=1, padx=(6, 0)
        )

        load_messages()

    def _move_chamado_to_status(self, chamado_id: int, target_status: str) -> None:
        for chamado in self.chamado_data:
            if int(chamado["id"]) == int(chamado_id):
                chamado["status"] = target_status
                break
        self.db.update_chamado_status(chamado_id, target_status)
        self._refresh_chamado_board()

    def _finalize_selected_chamado(self) -> None:
        if not self._chamado_selected_id:
            messagebox.showwarning("Selecao obrigatoria", "Selecione um chamado para finalizar.")
            return
        self._move_chamado_to_status(self._chamado_selected_id, "finalizado")
        self._chamado_selected_id = None

    def _toggle_fullscreen(self, _event=None):
        self._fullscreen = not self._fullscreen
        self.attributes("-fullscreen", self._fullscreen)

    def _exit_fullscreen(self, _event=None):
        self._fullscreen = False
        self.attributes("-fullscreen", False)
