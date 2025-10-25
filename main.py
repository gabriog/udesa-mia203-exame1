from fastapi import FastAPI, HTTPException
import database as db
import models
import payments as p

app = FastAPI()

def get_payment_or_404(payment_id: str):
    """Función helper para obtener un pago o lanzar un 404."""
    try:
        return db.load_payment(payment_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Payment not found")

@app.get("/payments")
async def get_all_payments():
    """Obtiene todos los pagos del sistema."""
    return db.load_all_payments()

@app.post("/payments/{payment_id}")
async def register_payment(payment_id: str, amount: float, payment_method: str):
    """Registra un pago con su información."""
    all_payments = db.load_all_payments()
    if payment_id in all_payments:
        raise HTTPException(status_code=409, detail="Payment ID already exists")

    new_payment = {
        models.AMOUNT: amount,
        models.PAYMENT_METHOD: payment_method,
        models.STATUS: models.STATUS_REGISTRADO
    }
    
    db.save_payment_data(payment_id, new_payment)
    return new_payment

@app.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float, payment_method: str):
    """Actualiza la información de un pago existente."""
    payment = get_payment_or_404(payment_id)
    
    # Solo se puede updatear si está en estado REGISTRADO 
    if payment[models.STATUS] != models.STATUS_REGISTRADO:
        raise HTTPException(
            status_code=409, 
            detail=f"Payment cannot be updated in status {payment[models.STATUS]}"
        )
        
    payment[models.AMOUNT] = amount
    payment[models.PAYMENT_METHOD] = payment_method
    db.save_payment_data(payment_id, payment)
    return payment

@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str):
    """Marca un pago como pagado o fallido tras la validación."""
    payment = get_payment_or_404(payment_id)

    if payment[models.STATUS] != models.STATUS_REGISTRADO:
        raise HTTPException(
            status_code=409, 
            detail=f"Payment cannot be paid in status {payment[models.STATUS]}"
        )

    all_payments = db.load_all_payments()
    
    # Delegamos la lógica de validación
    is_valid = p.validate_payment(payment, all_payments)
    
    if is_valid:
        payment[models.STATUS] = models.STATUS_PAGADO
    else:
        payment[models.STATUS] = models.STATUS_FALLIDO
        
    db.save_payment_data(payment_id, payment)
    return payment

@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    """Revierte un pago del estado FALLIDO a REGISTRADO."""
    payment = get_payment_or_404(payment_id)
    
    # Solo se puede revertir si está en estado FALLIDO
    if payment[models.STATUS] != models.STATUS_FALLIDO:
        raise HTTPException(
            status_code=409, 
            detail=f"Payment cannot be reverted in status {payment[models.STATUS]}"
        )

    payment[models.STATUS] = models.STATUS_REGISTRADO
    db.save_payment_data(payment_id, payment)
    return payment