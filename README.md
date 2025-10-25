# Examen API de Gestión de Pagos

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
python -m unittest test_app.py
```


## Decisiones de Diseño y Trade-offs

Persistencia (JSON): Usamos el data.json que venia en el codigo de referencia. Es simple pero no es apto para producción ya que el problema es que no maneja concurrencia. Por ejemplo, si dos pagos con tarjeta se validan al mismo tiempo, ambos podrían aprobarse incorrectamente, ya que el archivo no tiene locks. La solución real sería usar una base de datos transaccional (como Postgres) para manejar esto. 

API (Query vs. Body): Seguimos la consigna usando query parameters para enviar datos en los POST (como amount y payment_method). Lo estándar en API REST es mandar estos datos dentro de un JSON body, ya que es mas limpio y fácil de validar.

Logica de Estados: El flujo de estados se implemento con chequeos simples dentro de cada endpoint. Si el flujo fuera mucho más complejo, habria que usar una libreria de maquina de estados para formalizar las transiciones.