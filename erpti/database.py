import sqlite3
import hashlib
import hmac
import os
from base64 import urlsafe_b64decode, urlsafe_b64encode
from pathlib import Path


class DatabaseManager:
    PASSWORD_PEPPER = "Sidertec01"
    PASSWORD_ITERATIONS = 200_000

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
                    username TEXT NOT NULL DEFAULT '',
                    senha TEXT NOT NULL DEFAULT '',
                    telefone TEXT NOT NULL,
                    ramal TEXT NOT NULL,
                    email TEXT NOT NULL
                )
                """
            )
            user_columns = {row[1] for row in cursor.execute("PRAGMA table_info(users)").fetchall()}
            if "perfil" not in user_columns:
                cursor.execute("ALTER TABLE users ADD COLUMN perfil TEXT NOT NULL DEFAULT ''")
            if "username" not in user_columns:
                cursor.execute("ALTER TABLE users ADD COLUMN username TEXT NOT NULL DEFAULT ''")
            if "senha" not in user_columns:
                cursor.execute("ALTER TABLE users ADD COLUMN senha TEXT NOT NULL DEFAULT ''")
            if "senha_hash" not in user_columns:
                cursor.execute("ALTER TABLE users ADD COLUMN senha_hash TEXT NOT NULL DEFAULT ''")
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
                    autor TEXT NOT NULL DEFAULT '',
                    tipo TEXT NOT NULL DEFAULT '',
                    urgencia TEXT NOT NULL DEFAULT '',
                    arquivo TEXT NOT NULL DEFAULT '',
                    responsavel TEXT NOT NULL DEFAULT '',
                    status TEXT NOT NULL
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS chamado_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chamado_id INTEGER NOT NULL,
                    canal TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    mensagem TEXT NOT NULL,
                    arquivo TEXT NOT NULL DEFAULT '',
                    criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(chamado_id) REFERENCES chamados(id)
                )
                """
            )
            chamado_columns = {
                row[1] for row in cursor.execute("PRAGMA table_info(chamados)").fetchall()
            }
            if "autor" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN autor TEXT NOT NULL DEFAULT ''")
            if "tipo" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN tipo TEXT NOT NULL DEFAULT ''")
            if "urgencia" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN urgencia TEXT NOT NULL DEFAULT ''")
            if "arquivo" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN arquivo TEXT NOT NULL DEFAULT ''")
            if "responsavel" not in chamado_columns:
                cursor.execute("ALTER TABLE chamados ADD COLUMN responsavel TEXT NOT NULL DEFAULT ''")
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
            self._migrate_plaintext_passwords(conn)

    def _hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        derived = hashlib.pbkdf2_hmac(
            "sha256",
            (password + self.PASSWORD_PEPPER).encode("utf-8"),
            salt,
            self.PASSWORD_ITERATIONS,
        )
        salt_b64 = urlsafe_b64encode(salt).decode("ascii")
        hash_b64 = urlsafe_b64encode(derived).decode("ascii")
        return f"pbkdf2_sha256${self.PASSWORD_ITERATIONS}${salt_b64}${hash_b64}"

    def _verify_password(self, password: str, encoded_hash: str) -> bool:
        try:
            algorithm, rounds, salt_b64, hash_b64 = encoded_hash.split("$", 3)
        except ValueError:
            return False
        if algorithm != "pbkdf2_sha256":
            return False
        try:
            salt = urlsafe_b64decode(salt_b64.encode("ascii"))
            stored_hash = urlsafe_b64decode(hash_b64.encode("ascii"))
            iterations = int(rounds)
        except Exception:
            return False
        candidate = hashlib.pbkdf2_hmac(
            "sha256",
            (password + self.PASSWORD_PEPPER).encode("utf-8"),
            salt,
            iterations,
        )
        return hmac.compare_digest(candidate, stored_hash)

    def _migrate_plaintext_passwords(self, conn: sqlite3.Connection) -> None:
        cursor = conn.cursor()
        rows = cursor.execute(
            """
            SELECT id, senha, senha_hash
            FROM users
            WHERE TRIM(COALESCE(senha, '')) <> ''
            """
        ).fetchall()
        changed = False
        for user_id, plain_password, stored_hash in rows:
            if stored_hash:
                continue
            password_hash = self._hash_password(plain_password)
            cursor.execute(
                "UPDATE users SET senha_hash = ?, senha = '' WHERE id = ?",
                (password_hash, user_id),
            )
            changed = True
        if changed:
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

    def fetch_user_group_map(self) -> dict[int, str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            rows = cursor.execute(
                """
                SELECT
                    m.user_id,
                    GROUP_CONCAT(g.nome, ', ')
                FROM user_group_members m
                JOIN user_groups g ON g.id = m.group_id
                GROUP BY m.user_id
                """
            ).fetchall()
            return {int(user_id): groups for user_id, groups in rows}

    def set_user_credentials(self, user_id: int, username: str, senha: str) -> bool:
        password_hash = self._hash_password(senha)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            exists = cursor.execute(
                """
                SELECT 1 FROM users
                WHERE LOWER(username) = LOWER(?) AND id <> ?
                LIMIT 1
                """,
                (username, user_id),
            ).fetchone()
            if exists:
                return False
            cursor.execute(
                "UPDATE users SET username = ?, senha_hash = ?, senha = '' WHERE id = ?",
                (username, password_hash, user_id),
            )
            conn.commit()
            return True

    def authenticate_user(self, username: str, senha: str) -> dict[str, str] | None:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            row = cursor.execute(
                """
                SELECT id, nome, username, senha, senha_hash
                FROM users
                WHERE LOWER(username) = LOWER(?)
                LIMIT 1
                """,
                (username,),
            ).fetchone()
            if not row:
                return None

            user = dict(row)
            stored_hash = (user.get("senha_hash") or "").strip()
            stored_plain = (user.get("senha") or "").strip()

            if stored_hash and self._verify_password(senha, stored_hash):
                return {"id": user["id"], "nome": user["nome"], "username": user["username"]}

            if stored_plain and hmac.compare_digest(stored_plain, senha):
                password_hash = self._hash_password(senha)
                cursor.execute(
                    "UPDATE users SET senha_hash = ?, senha = '' WHERE id = ?",
                    (password_hash, user["id"]),
                )
                conn.commit()
                return {"id": user["id"], "nome": user["nome"], "username": user["username"]}

            return None

    def insert_chamado(
        self,
        titulo: str,
        descricao: str,
        autor: str,
        tipo: str,
        urgencia: str,
        arquivo: str,
        status: str,
        responsavel: str = "",
    ) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chamados (titulo, descricao, autor, tipo, urgencia, arquivo, responsavel, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (titulo, descricao, autor, tipo, urgencia, arquivo, responsavel, status),
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

    def update_chamado_flow(self, chamado_id: int, status: str, responsavel: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE chamados SET status = ?, responsavel = ? WHERE id = ?",
                (status, responsavel, chamado_id),
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
                    COALESCE(NULLIF(TRIM(u.first_name || ' ' || u.last_name), ''), u.username, ''),
                    COALESCE(NULLIF(TRIM(au.first_name || ' ' || au.last_name), ''), au.username, ''),
                    t.ticket_type,
                    t.urgency,
                    t.status,
                    COALESCE(a.files, '')
                FROM tickets_ticket t
                LEFT JOIN auth_user u ON u.id = t.created_by_id
                LEFT JOIN auth_user au ON au.id = t.assigned_to_id
                LEFT JOIN (
                    SELECT ticket_id, GROUP_CONCAT(file, '; ') AS files
                    FROM tickets_ticketattachment
                    GROUP BY ticket_id
                ) a ON a.ticket_id = t.id
                ORDER BY t.id
            """
            legacy_rows = legacy_cur.execute(query).fetchall()

            for row in legacy_rows:
                legacy_id, title, description, autor, assigned_to, ticket_type, urgency, old_status, files = row
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

                mapped_status = "pendente"
                mapped_responsavel = ""
                old_status = (old_status or "").strip().lower()
                if old_status in {"resolved", "fechado", "finalizado"}:
                    mapped_status = "fechado"
                elif old_status in {"in_progress", "em_atendimento"}:
                    mapped_status = "em_atendimento"
                    mapped_responsavel = assigned_to or ""

                cursor.execute(
                    """
                    INSERT INTO chamados (
                        titulo, descricao, autor, tipo, urgencia, arquivo, responsavel, status, legacy_source, legacy_id
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        title or "",
                        description or "",
                        autor or "Solicitante",
                        ticket_type or "",
                        urgency or "",
                        files or "",
                        mapped_responsavel,
                        mapped_status,
                        "old_tickets",
                        legacy_id,
                    ),
                )
                imported += 1

            conn.commit()
            legacy_conn.close()

        return imported, skipped

    def fetch_chamado_messages(self, chamado_id: int, canal: str) -> list[dict[str, str]]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(
                """
                SELECT id, autor, mensagem, arquivo, criado_em
                FROM chamado_messages
                WHERE chamado_id = ? AND canal = ?
                ORDER BY id
                """,
                (chamado_id, canal),
            ).fetchall()
            return [dict(row) for row in rows]

    def add_chamado_message(
        self,
        chamado_id: int,
        canal: str,
        autor: str,
        mensagem: str,
        arquivo: str,
    ) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO chamado_messages (chamado_id, canal, autor, mensagem, arquivo)
                VALUES (?, ?, ?, ?, ?)
                """,
                (chamado_id, canal, autor, mensagem, arquivo),
            )
            conn.commit()
