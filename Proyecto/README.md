# POS Radiocity

Este proyecto es una aplicación web basada en **Django** y **SQLAlchemy** para la gestión de ventas y análisis de datos.

## 📂 Organización del backend

El código del proyecto vive en la carpeta `backend/`:

- `backend/datapp`: scripts de carga de datos y dashboard de Streamlit.
- `backend/webapp`: aplicación Django.

El archivo `main.py` en la raíz ofrece una pequeña CLI para levantar cualquiera de estos servicios.

## 📦 Requisitos

- Python 3.10+
- pip (administrador de paquetes de Python)
- [MySQL](https://dev.mysql.com/downloads/) o [MariaDB](https://mariadb.org/download/) (para la carga inicial de datos)
- (Opcional) SQLite para pruebas locales (ya incluido en el repo con `db.sqlite3`)

### Configuración del entorno

1. Crea y activa un entorno virtual:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

2. Instala las dependencias del proyecto:

   ```bash
   pip install -r requirements.txt
   ```

3. Ejecuta el backend (servidor Django):

   ```bash
   python main.py --app server
   ```

   Para lanzar el dashboard de Streamlit utiliza:

   ```bash
   python main.py --app dashboard
   ```

---

### 1. Poblar la base de datos (opcional si usas MySQL)
Desde la raíz del proyecto:

```bash
python backend/datapp/populate_db.py
```

Esto:
- Limpia datos existentes.
- Inserta datos iniciales desde `datos.json`.

---

### 2. Migraciones de Django

Aplica las migraciones necesarias para las apps (`gestion`, `auth`, etc.) con:

```bash
python backend/webapp/manage.py migrate
```

---

### 3. Levantar el servidor de desarrollo

```bash
python main.py --app server
```

El servidor quedará disponible en:

👉 http://127.0.0.1:8000/

---

## 🛠️ Comandos útiles

- Poblar datos con SQLAlchemy:

  ```bash
  python backend/datapp/populate_db.py
  ```

- Borrar datos manualmente:

  ```bash
  python backend/datapp/clear_db.py
  ```

- Migraciones Django:

  ```bash
  python backend/webapp/manage.py makemigrations
  python backend/webapp/manage.py migrate
  ```

- Crear superusuario para el admin de Django:

  ```bash
  python backend/webapp/manage.py createsuperuser
  ```

- Correr servidor:

  ```bash
  python main.py --app server
  ```



## 📝 Notas

- Si usas **WSL (Ubuntu en Windows)**, recuerda ejecutar los scripts desde la **raíz del proyecto**, por ejemplo:

  ```bash
  python backend/datapp/populate_db.py
  ```

- No ejecutes `python backend/datapp/populate_db.py` dentro de la carpeta `webapp/`, ya que esa ruta no existe allí.

---