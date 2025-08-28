# POS Radiocity

Este proyecto es una aplicación web basada en **Django** y **SQLAlchemy** para la gestión de ventas y análisis de datos.

## 📦 Requisitos

- Python 3.10+
- pip (administrador de paquetes de Python)
- [MySQL](https://dev.mysql.com/downloads/) o [MariaDB](https://mariadb.org/download/) (para la carga inicial de datos)
- (Opcional) SQLite para pruebas locales (ya incluido en el repo con `db.sqlite3`)

Instala las dependencias del proyecto con:

```bash
pip install -r requirements.txt
```

---

## 🚀 Ejecución del proyecto

### 1. Poblar la base de datos (opcional si usas MySQL)
Desde la raíz del proyecto:

```bash
python datapp/populate_db.py
```

Esto:
- Limpia datos existentes.
- Inserta datos iniciales desde `datos.json`.

---

### 2. Migraciones de Django

Entra en la carpeta `webapp` y corre:

```bash
cd webapp
python manage.py migrate
```

Esto aplica todas las migraciones necesarias para las apps (`gestion`, `auth`, etc.).

---

### 3. Levantar el servidor de desarrollo

Desde la carpeta `webapp`:

```bash
python manage.py runserver
```

El servidor quedará disponible en:

👉 http://127.0.0.1:8000/

---

## 🛠️ Comandos útiles

- Poblar datos con SQLAlchemy:

  ```bash
  python datapp/populate_db.py
  ```

- Borrar datos manualmente:

  ```bash
  python datapp/clear_db.py
  ```

- Migraciones Django:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

- Crear superusuario para el admin de Django:

  ```bash
  python manage.py createsuperuser
  ```

- Correr servidor:

  ```bash
  python manage.py runserver
  ```



## 📝 Notas

- Si usas **WSL (Ubuntu en Windows)**, recuerda ejecutar los scripts desde la **raíz del proyecto**, por ejemplo:

  ```bash
  python datapp/populate_db.py
  ```

- No ejecutes `python datapp/populate_db.py` dentro de la carpeta `webapp/`, ya que esa ruta no existe allí.

---