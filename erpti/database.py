import sqlite3
from pathlib import Path


class DatabaseManager:
    def __init__(self, db_path: str = "erpti.db") -> None:
        self.db_path = Path(db_path)

    def initialize(self, default_access_folders: list[str]) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    departamento TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    perfil TEXT NOT NULL DEFAULT '',
                    telefone TEXT NOT NULL,
                    ramal TEXT NOT NULL,
                    email TEXT NOT NULL
                )
                """
            )
            user_columns = {row[1] for row in cursor.execute("PRAGMA table_info(users)").fetchall()}
            if "perfil" not in user_columns:
                cursor.execute("ALTER TABLE users ADD COLUMN perfil TEXT NOT NULL DEFAULT ''")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS access_folders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_groups (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL UNIQUE
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS user_group_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    group_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    UNIQUE(group_id, user_id),
                    FOREIGN KEY(group_id) REFERENCES user_groups(id),
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS equipments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_interno TEXT NOT NULL,
                    patrimonio TEXT NOT NULL,
                    selo_patrimonio TEXT NOT NULL,
                    equipamento TEXT NOT NULL,
                    modelo TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    serie TEXT NOT NULL,
                    mem TEXT NOT NULL,
                    processador TEXT NOT NULL,
                    geracao TEXT NOT NULL,
                    hd TEXT NOT NULL,
                    mod_hd TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    fabricante TEXT NOT NULL,
                    endereco_mac TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nro TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    grupo TEXT NOT NULL,
                    situacao TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS ramais (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nro TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    sobrenome TEXT NOT NULL,
                    email TEXT NOT NULL,
                    grupo TEXT NOT NULL,
                    situacao TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS softwares (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    computador TEXT NOT NULL,
                    setor TEXT NOT NULL,
                    serial TEXT NOT NULL,
                    conta TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS insumos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    insumo TEXT NOT NULL,
                    data TEXT NOT NULL,
                    qtd TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    departamento TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS requisicoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    solicitacao TEXT NOT NULL,
                    qtd TEXT NOT NULL,
                    valor TEXT NOT NULL,
                    total TEXT NOT NULL,
                    requisitado TEXT NOT NULL,
                    aprovado TEXT NOT NULL,
                    recebido TEXT NOT NULL,
                    nf TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    fornecedor TEXT NOT NULL,
                    link TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS emprestimos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    equipamento TEXT NOT NULL,
                    documento TEXT NOT NULL,
                    arquivo TEXT NOT NULL,
                    situacao TEXT NOT NULL,
                    data TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chamados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titulo TEXT NOT NULL,
                    descricao TEXT NOT NULL,
                    tipo TEXT NOT NULL DEFAULT '',
                    urgencia TEXT NOT NULL DEFAULT '',
                    arquivo TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL
                )
                """
            )
            chamado_columns = {
                row[1] for row in cursor.execute("PRAGMA table_info(chamados)").fetchall()
            }
            if "tipo" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN tipo TEXT NOT NULL DEFAULT ''")
            if "urgencia" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN urgencia TEXT NOT NULL DEFAULT ''")
            if "arquivo" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN arquivo TEXT NOT NULL DEFAULT ''")
            if "legacy_source" not in chamado_columns:
                cursor.execute(
                    "ALTER TABLE chamados ADD COLUMN legacy_source TEXT NOT NULL DEFAULT ''"
                )
            if "legacy_id" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN legacy_id INTEGER DEFAULT NULL")

            has_access_rows = cursor.execute("SELECT COUNT(*) FROM access_folders").fetchone()[0]
            if has_access_rows == 0:
                cursor.executemany(
                    "INSERT INTO access_folders (nome) VALUES (?)",
                    [(folder,) for folder in default_access_folders],
                )

            conn.commit()

    def fetch_rows(self, table: str, columns: tuple[str, ...]) -> list[dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            sql = f"SELECT {', '.join(columns)} FROM {table} ORDER BY id"
            rows = cursor.execute(sql).fetchall()
            return [dict(row) for row in rows]

    def fetch_access_folders(self) -> list[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            rows = cursor.execute("SELECT nome FROM access_folders ORDER BY LOWER(nome)").fetchall()
            return [row[0] for row in rows]

    def insert_row(self, table: str, row: dict[str, str]) -> None:
        columns = list(row.keys())
        placeholders = ", ".join(["?"] * len(columns))
        column_list = ", ".join(columns)
        values = [row[column] for column in columns]
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            sql = f"INSERT INTO {table} ({column_list}) VALUES ({placeholders})"
            cursor.execute(sql, values)
            conn.commit()

    def add_access_folder(self, folder_name: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO access_folders (nome) VALUES (?)", (folder_name,))
            conn.commit()

    def remove_access_folders(self, folder_names: list[str]) -> None:
        if not folder_names:
            return
        placeholders = ", ".join(["?"] * len(folder_names))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM access_folders WHERE nome IN ({placeholders})",
                folder_names,
            )
            conn.commit()

    def fetch_user_groups(self) -> list[dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute("SELECT id, nome FROM user_groups ORDER BY LOWER(nome)").fetchall()
            return [dict(row) for row in rows]

    def add_user_group(self, nome: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            exists = cursor.execute(
                "SELECT 1 FROM user_groups WHERE LOWER(nome)=LOWER(?) LIMIT 1",
                (nome,),
            ).fetchone()
            if exists:
                return False
            cursor.execute("INSERT INTO user_groups (nome) VALUES (?)", (nome,))
            conn.commit()
            return True

    def assign_user_to_group(self, group_id: int, user_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            exists = cursor.execute(
                """
                SELECT 1 FROM user_group_members
                WHERE group_id = ? AND user_id = ?
                LIMIT 1
                """,
                (group_id, user_id),
            ).fetchone()
            if exists:
                return False
            cursor.execute(
                "INSERT INTO user_group_members (group_id, user_id) VALUES (?, ?)",
                (group_id, user_id),
            )
            conn.commit()
            return True

    def fetch_group_members(self, group_id: int) -> list[dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(
                """
                SELECT u.id, u.nome, u.departamento, u.perfil
                FROM user_group_members m
                JOIN users u ON u.id = m.user_id
                WHERE m.group_id = ?
                ORDER BY u.nome
                """,
                (group_id,),
            ).fetchall()
            return [dict(row) for row in rows]

    def insert_chamado(
        self,
        titulo: str,
        descricao: str,
        tipo: str,
        urgencia: str,
        arquivo: str,
        status: str,
    ) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chamados (titulo, descricao, tipo, urgencia, arquivo, status)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (titulo, descricao, tipo, urgencia, arquivo, status),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def update_chamado_status(self, chamado_id: int, status: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE chamados SET status = ? WHERE id = ?",
                (status, chamado_id),
            )
            conn.commit()

    def import_legacy_chamados(self, legacy_db_path: str) -> tuple[int, int]:
        imported = 0
        skipped = 0

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            legacy_conn = sqlite3.connect(legacy_db_path)
            legacy_cur = legacy_conn.cursor()

            query = """
                SELECT
                    t.id,
                    t.title,
                    t.description,
                    t.ticket_type,
                    t.urgency,
                    COALESCE(a.files, '')
                FROM tickets_ticket t
                LEFT JOIN (
                    SELECT ticket_id, GROUP_CONCAT(file, '; ') AS files
                    FROM tickets_ticketattachment
                    GROUP BY ticket_id
                ) a ON a.ticket_id = t.id
                ORDER BY t.id
            """
            legacy_rows = legacy_cur.execute(query).fetchall()

            for row in legacy_rows:
                legacy_id, title, description, ticket_type, urgency, files = row
                exists = cursor.execute(
                    """
                    SELECT 1
                    FROM chamados
                    WHERE legacy_source = ? AND legacy_id = ?
                    LIMIT 1
                    """,
                    ("old_tickets", legacy_id),
                ).fetchone()
                if exists:
                    skipped += 1
                    continue

                cursor.execute(
                    """
                    INSERT INTO chamados (
                        titulo, descricao, tipo, urgencia, arquivo, status, legacy_source, legacy_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        title or "",
                        description or "",
                        ticket_type or "",
                        urgency or "",
                        files or "",
                        "pendente",
                        "old_tickets",
                        legacy_id,
                    ),
                )
                imported += 1

            conn.commit()
            legacy_conn.close()

        return imported, skipped
