"""数据库引擎、会话与声明基类。"""
from sqlalchemy import inspect, text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

# SQLite 在多线程下需要关闭同一线程检查
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 依赖：为每个请求提供数据库会话。"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _server_default_literal(column):
    """取出列上的字面量服务端默认值（仅支持常量，如 'expense'）。"""
    server_default = column.server_default
    if server_default is None:
        return None
    arg = getattr(server_default, "arg", None)
    if isinstance(arg, str):
        return arg
    text = getattr(arg, "text", None)
    return text if isinstance(text, str) else None


def ensure_columns(base):
    """SQLite 轻量迁移：create_all 不会改已存在的表，这里补上新增的列。

    - 带 server_default 的列会写成 `DEFAULT <值>`，SQLite 会用该默认值回填历史行；
    - 非空列只有在能取到默认值时才会加 NOT NULL（SQLite 不允许无默认值的 NOT NULL 列）。
    若将来需要更复杂的迁移（改类型、重命名、回填计算值），应改用 Alembic。
    """
    if not engine.url.get_backend_name().startswith("sqlite"):
        return
    inspector = inspect(engine)
    added = []
    with engine.begin() as conn:
        for table in base.metadata.sorted_tables:
            if not inspector.has_table(table.name):
                continue
            existing = {col["name"] for col in inspector.get_columns(table.name)}
            for col in table.columns:
                if col.name in existing:
                    continue
                segments = [col.name, col.type.compile(engine.dialect)]
                default = _server_default_literal(col)
                if default is not None:
                    segments.append(f"DEFAULT '{default}'")
                if col.nullable is False and default is not None:
                    segments.append("NOT NULL")
                conn.execute(text(f"ALTER TABLE {table.name} ADD COLUMN {' '.join(segments)}"))
                added.append(f"{table.name}.{col.name}")
    return added


def _python_default_literal(column):
    """取出列上的 Python 侧默认值（标量或零参 callable），转成 SQL 字面量。"""
    default = column.default
    if default is None:
        return None
    arg = getattr(default, "arg", None)
    if callable(arg):
        try:
            arg = arg(None)
        except TypeError:
            return None
    if isinstance(arg, bool):
        return 1 if arg else 0
    if isinstance(arg, (int, float)):
        return arg
    if isinstance(arg, str):
        return f"'{arg}'"
    return None


def backfill_nulls(base):
    """把历史行中的 NULL 回填成模型默认值。

    迁移加列时若该列还没写 server_default，SQLite 会把老行的值留成 NULL，
    读取时会被 Pydantic 判为类型错误（例如 bool 字段收到 None）。这里按模型
    声明的 Python 默认值补一遍，保证升级后老数据仍然可读。
    """
    inspector = inspect(engine)
    filled = []
    with engine.begin() as conn:
        for table in base.metadata.sorted_tables:
            if not inspector.has_table(table.name):
                continue
            existing = {col["name"] for col in inspector.get_columns(table.name)}
            for col in table.columns:
                if col.name == "id" or col.name not in existing:
                    continue
                literal = _python_default_literal(col)
                if literal is None:
                    continue
                result = conn.execute(
                    text(f"UPDATE {table.name} SET {col.name} = :val WHERE {col.name} IS NULL"),
                    {"val": literal},
                )
                if result.rowcount:
                    filled.append(f"{table.name}.{col.name}({result.rowcount})")
    return filled
