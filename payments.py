import models

def validate_payment(payment: dict, all_payments: dict) -> bool:
    """
    Valida un pago basado en su método y las reglas de negocio.
    Retorna True si es válido, False si falla.
    """
    method = payment[models.PAYMENT_METHOD]
    amount = payment[models.AMOUNT]

    if method == models.CREDIT_CARD:
        # [cite_start]Condición 1: Monto [cite: 42]
        if amount >= 10000:
            return False
        
        # [cite_start]Condición 2: No más de 1 pago REGISTRADO con este método [cite: 43-44]
        registered_cc_payments = 0
        for p_data in all_payments.values():
            if (p_data[models.PAYMENT_METHOD] == models.CREDIT_CARD and
                p_data[models.STATUS] == models.STATUS_REGISTRADO):
                registered_cc_payments += 1
        
        # Si hay más de 1 (incluyendo el actual), falla.
        if registered_cc_payments > 1:
            return False
            
        return True

    elif method == models.PAYPAL:
        # [cite_start]Condición 1: Monto [cite: 47]
        if amount >= 5000:
            return False
        return True

    # Si el método de pago no es conocido, falla la validación
    return False