# API de Gestión de Pagos (Examen Unidad 1)

Esta es la implementación de una API de pagos usando FastAPI, con CI/CD a través de GitHub Actions.

## URL de la API

**API de Producción:** `http://<TU_IP_O_DOMINIO>:8000/docs`

## Instrucciones de Ejecución

### 1. Ejecución Local

1.  Clonar el repositorio:
    ```bash
    git clone <tu-repo-url>
    cd <tu-repo-dir>
    ```
2.  (Opcional) Crear un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r requirements.txt
    ```
4.  Correr la API en modo desarrollo:
    ```bash
    fastapi dev main.py
    ```
5.  Acceder a la documentación interactiva (Swagger UI):
    [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 2. Ejecución de Tests

Para correr la suite de tests automáticos:

```bash
pytest
