import base64
import ctypes
import os
from ctypes import wintypes


def _is_windows() -> bool:
    return os.name == "nt"


def _resolve_default_key_file() -> str:
    app_data_root = os.getenv("LOCALAPPDATA") or os.getenv("APPDATA") or os.getcwd()
    data_dir = os.path.join(app_data_root, "SG-VILLA-DOLCE", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "sqlite_key.bin")


def _get_key_file_path() -> str:
    return os.getenv("DB_SQLITE_KEY_FILE", "").strip() or _resolve_default_key_file()


def _generate_key() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode("ascii")


if _is_windows():
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


    crypt32 = ctypes.windll.crypt32
    kernel32 = ctypes.windll.kernel32


def _dpapi_protect(data: bytes) -> bytes:
    if not _is_windows():
        return data

    in_buffer = ctypes.create_string_buffer(data)
    in_blob = DATA_BLOB(
        len(data),
        ctypes.cast(in_buffer, ctypes.POINTER(ctypes.c_byte)),
    )
    out_blob = DATA_BLOB()
    if not crypt32.CryptProtectData(
        ctypes.byref(in_blob),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise OSError("Falha ao proteger chave com DPAPI")

    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        kernel32.LocalFree(out_blob.pbData)


def _dpapi_unprotect(data: bytes) -> bytes:
    if not _is_windows():
        return data

    in_buffer = ctypes.create_string_buffer(data)
    in_blob = DATA_BLOB(
        len(data),
        ctypes.cast(in_buffer, ctypes.POINTER(ctypes.c_byte)),
    )
    out_blob = DATA_BLOB()
    if not crypt32.CryptUnprotectData(
        ctypes.byref(in_blob),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob),
    ):
        raise OSError("Falha ao descriptografar chave com DPAPI")

    try:
        return ctypes.string_at(out_blob.pbData, out_blob.cbData)
    finally:
        kernel32.LocalFree(out_blob.pbData)


def _write_key_file(path: str, key: str) -> None:
    key_bytes = key.encode("utf-8")
    protected = _dpapi_protect(key_bytes)
    with open(path, "wb") as key_file:
        key_file.write(protected)


def _read_key_file(path: str) -> str:
    with open(path, "rb") as key_file:
        raw = key_file.read()
    return _dpapi_unprotect(raw).decode("utf-8")


def get_sqlite_cipher_key() -> str:
    env_key = os.getenv("DB_SQLITE_KEY", "").strip()
    if env_key:
        return env_key

    key_file_path = _get_key_file_path()
    if os.path.exists(key_file_path):
        return _read_key_file(key_file_path)

    generated_key = _generate_key()
    _write_key_file(key_file_path, generated_key)
    return generated_key
