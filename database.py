import json
import models

def load_all_payments():
    """Carga todos los pagos desde el archivo JSON."""
    try:
        with open(models.DATA_PATH, "r") as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        # Si el archivo no existe, retorna un dict vacío
        return {}

def save_all_payments(data):
    """Guarda el dict completo de pagos en el archivo JSON."""
    with open(models.DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)

def load_payment(payment_id: str):
    """
    Carga un pago específico.
    Lanza KeyError si el payment_id no existe.
    """
    all_data = load_all_payments()
    return all_data[payment_id]

def save_payment_data(payment_id: str, data: dict):
    """Guarda (crea o actualiza) los datos de un pago específico."""
    all_data = load_all_payments()
    all_data[str(payment_id)] = data
    save_all_payments(all_data)