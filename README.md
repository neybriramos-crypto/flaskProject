# Sistema de Gestión de Usuarios con Flask

Proyecto Flask simple de autenticación y administración de usuarios.

## Descripción

Aplicación web que permite registrar usuarios, iniciar sesión y acceder a un panel de control. Los usuarios normales ven su propio dashboard, mientras que los administradores pueden ver la lista de usuarios y eliminar cuentas.

## Características

- Registro de usuarios
- Inicio de sesión
- Panel de usuario y panel de admin
- Cambio de rol entre `user` y `admin`
- Eliminación de usuarios (solo admin)
- Persistencia con base de datos SQL usando SQLAlchemy

## Estructura principal

- `app.py`: aplicación Flask y rutas.
- `config.py`: configuración de Flask y SQLAlchemy.
- `models.py`: modelo `User` y configuración de la base de datos.
- `templates/`: vistas HTML.
- `static/`: recursos estáticos.

## Requisitos

- Python 3.9+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- PyMySQL

## Instalación

1. Crea y activa un entorno virtual:

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

2. Instala las dependencias:

```powershell
pip install flask flask-login flask-sqlalchemy pymysql
```

3. Configura la base de datos opcionalmente con variables de entorno:

```powershell
$env:SECRET_KEY = "tu_llave_secreta"
$env:DATABASE_URL = "mysql+pymysql://usuario:contraseña@localhost/sistema_usuarios"
```

> Si no se define `DATABASE_URL`, se usa por defecto:
> `mysql+pymysql://root:@localhost/sistema_usuarios`

4. Crea la base de datos en MySQL si aún no existe.

## Uso

Ejecuta la aplicación:

```powershell
python app.py
```

Abre el navegador en:

```
http://127.0.0.1:5000
```

## Notas

- La aplicación crea las tablas automáticamente al iniciar.
- El cambio de rol y la eliminación de usuarios solo están disponibles para usuarios con rol `admin`.
- Ajusta `SECRET_KEY` y la conexión de base de datos en producción.

## Licencia

Proyecto de ejemplo sin licencia específica.
