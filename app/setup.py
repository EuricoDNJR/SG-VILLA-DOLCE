from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["asyncio", "uvicorn", "fastapi", "contextlib", "database", "routers", "passlib", "pydantic", "peewee"],
    "include_files": ["app.log"]
}

executables = [
    Executable("main.py", base=None),
]

setup(
    name="Nome do Seu App",
    version="1.0",
    description="Descrição do Seu App",
    options={"build_exe": build_exe_options},
    executables=executables,
)