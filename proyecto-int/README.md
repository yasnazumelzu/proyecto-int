# Sistema Hospital Clínico Herminda Martín

Sistema de gestión hospitalaria desarrollado con Django para el Hospital Clínico Herminda Martín de Chillán.

## Características

- **Módulo de Matrona**: Registro de nacimientos y seguimiento materno
- **Módulo Médico**: Gestión de reportes clínicos y fichas de pacientes
- **Módulo de Enfermería**: Controles y seguimiento de pacientes
- **Módulo Administrativo**: Admisiones, pagos, altas y egresos
- **Módulo de Pediatra**: Gestión de recién nacidos y altas pediátricas
- **Módulo TI**: Administración de usuarios, permisos y auditoría del sistema

## Tecnologías

- Django 5.x
- Python 3.12
- Bootstrap 5
- SQLite (base de datos)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd proyecto-int
```

2. Crear un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Aplicar migraciones:
```bash
python manage.py migrate
```

5. Crear superusuario:
```bash
python manage.py createsuperuser
```

6. Ejecutar el servidor:
```bash
python manage.py runserver
```

## Usuarios por defecto

- **Matrona**: `matrona` / `1234`
- **Médico**: `medico` / `1234`
- **Enfermero**: `enfermero` / `1234`
- **Administrativo**: `administrativo` / `1234`
- **Pediatra**: `pediatra` / `1234`
- **TI**: Usar el comando `python manage.py crear_usuario_ti` o `python manage.py crear_pediatra`

## Estructura del Proyecto

```
proyecto-int/
├── administrativos/    # Módulo administrativo
├── auditoria/          # Sistema de auditoría
├── enfermero/          # Módulo de enfermería
├── medico/             # Módulo médico
├── matrona/            # Módulo de matrona
├── pacientes/          # Gestión de pacientes
├── pediatra/           # Módulo de pediatra
├── usuarios/           # Gestión de usuarios
└── templates/          # Plantillas HTML
```

## Licencia

Proyecto desarrollado para el Hospital Clínico Herminda Martín - Chillán
