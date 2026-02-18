# Sistema de Control de Horas de Servicio Social: BitBunker

Este proyecto es una aplicación web desarrollada con *Django* cuyo objetivo es llevar el **control y seguimiento de horas de servicio social para estudiantes**.

Permite:

* Registro de usuarios
* Inicio de sesión mediante matrícula
* Registro de horas diarias
* Visualización del progreso acumulado
* Generación de reportes en PDF

El sistema está diseñado para automatizar el seguimiento de horas de manera clara y sencilla.

---

##  Stack Tecnológico

### Backend

* **Python 3.10.10**
* **Django 5.2.11**

### Frontend

* HTML5
* CSS3
* JavaScript

---
## Usuarios de Prueba

Puedes usar los siguientes usuarios para probar la aplicación:

| Matrícula | Contraseña |
| --------- | ---------- |
| 211064018 | 211064018  |
| 1         | 1234       |
| 2         | 2345       |

---
###  Descripción de Endpoints

| Ruta         | Método   | Descripción                             |
| ------------ | -------- | --------------------------------------- |
| `/profile/`  | GET      | Visualización del perfil del estudiante |
| `/home/`     | GET      | Página principal tras iniciar sesión    |
| `/inicio/`   | GET      | Página principal antes iniciar sesión   |
| `/register/` | GET/POST | Registro de nuevos usuarios             |
| `/login/`    | GET/POST | Inicio de sesión                        |
| `/setup/`    | GET/POST | Configuración inicial                   |
| `/index/`    | GET      | Página principal del sistema            |
| `/save_pdf/` | POST     | Generación de reporte en PDF            |
| `/contador/` | GET/POST | Registro y conteo de horas              |
| `/logout/`   | GET      | Cierre de sesión                        |

---
## Flujo General del Sistema

1️. El estudiante se registra o inicia sesión con su matrícula.

2️. Accede al panel principal donde puede:

* Registrar horas diarias
* Consultar su acumulado
* Visualizar progreso

3️. El sistema contabiliza automáticamente las horas ingresadas.

4️. El usuario puede generar un **reporte en PDF** con su progreso.

---

## Ejecución local

### Requisitos

* Python **3.10.10**

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Para ejecuctar el sistema es con este comando:

```bash
python manage.py runserver
```

Acceso en:

```
http://127.0.0.1:8000/
```

---

## Ejecución con Docker (Recomendado)

### 1. Construir la imagen (Build)

Este comando lee el `Dockerfile` y empaqueta todo tu código y dependencias en una imagen.

```bash
docker build -t BitBunker .

```

### 2. Ejecutar el contenedor (Run)

Una vez creada la imagen, la pones en marcha con este comando:

```bash
docker run -p 8000:8000 BitBunker

```

---

## Estructura General del Proyecto

* `Services/` → Logica extensa del sistema
* `Views/` → Control principal de las vistas sistema
* `urls.py` → Definición de rutas
* `templates/` → Vistas HTML
* `static/` → Archivos CSS y JS
* `manage.py` → Punto de entrada del proyecto Django

---

##  Nota Importante sobre Persistencia

Actualmente **la persistencia de datos NO está habilitada**, ni del lado del servidor ni en la lógica del sistema.

Esto significa que:

* Los datos no se guardan permanentemente.
* Al reiniciar el servidor, la información puede perderse.
* El proyecto funciona como prototipo funcional.

