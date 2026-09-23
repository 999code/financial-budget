"""密码哈希与登录令牌。

仅用标准库实现，避免为演示项目引入 passlib / PyJWT 等依赖：

- 口令存储：PBKDF2-HMAC-SHA256（20 万次迭代）+ 随机盐，格式
  `pbkdf2_sha256$<iterations>$<salt_hex>$<hash_hex>`；
- 登录令牌：JSON 载荷 base64url 编码后接 HMAC-SHA256 签名（密钥来自
  settings.SECRET_KEY），载荷里带过期时间。

生产环境建议换成 passlib + PyJWT/OAuth2 标准方案。
"""
import base64
import hashlib
import hmac
import json
import os
import time
from datetime import timedelta

from app.config import settings

PBKDF2_ITERATIONS = 200_000
SALT_BYTES = 16
TOKEN_EXPIRE_HOURS = 24


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def hash_password(password: str) -> str:
    """生成可存储的口令摘要（每次随机盐，相同口令两次结果不同）。"""
    salt = os.urandom(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str | None) -> bool:
    """校验口令，同时兼容旧数据和非法格式（一律返回 False）。"""
    if not stored:
        return False
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(digest.hex(), digest_hex)


def create_token(user_id: int, expire_hours: int = TOKEN_EXPIRE_HOURS) -> str:
    payload = {
        "uid": user_id,
        "exp": int(time.time()) + int(timedelta(hours=expire_hours).total_seconds()),
    }
    body = _b64encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    return f"{body}.{_sign(body)}"


def _sign(body: str) -> str:
    secret = (settings.SECRET_KEY or "dev-secret").encode("utf-8")
    return hmac.new(secret, body.encode("utf-8"), hashlib.sha256).hexdigest()


def decode_token(token: str) -> int | None:
    """解析令牌，返回用户 id；签名错误或已过期返回 None。"""
    if not token or "." not in token:
        return None
    body, _, signature = token.rpartition(".")
    if not hmac.compare_digest(_sign(body), signature):
        return None
    try:
        payload = json.loads(_b64decode(body))
        user_id = int(payload["uid"])
        expired = int(payload.get("exp", 0)) <= int(time.time())
    except (ValueError, KeyError, TypeError):
        return None
    return None if expired else user_id
