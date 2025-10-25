import unittest
import models
import payments


class TestApp(unittest.TestCase):
    # simulo crear el pago aqui
    def make_payment(self, amount, method):
        return {
            models.AMOUNT: amount,
            models.PAYMENT_METHOD: method,
        }

    def test_credit_card_rejects_high_amount(self):
        """La tarjeta de credito debe fallar si el pago es mayor a 10000"""
        ok_payment = self.make_payment(9000, models.CREDIT_CARD)
        bad_payment = self.make_payment(15000, models.CREDIT_CARD)
        all_payments = {} 
        self.assertTrue(payments.validate_payment(ok_payment, all_payments))
        self.assertFalse(payments.validate_payment(bad_payment, all_payments))

    def test_paypal_amount_limits(self):
        """Con Paypal solo se aceptan pagos menores a 5000"""
        ok_payment = self.make_payment(4999, models.PAYPAL)
        bad_payment = self.make_payment(5000, models.PAYPAL)
        all_payments = {}
        self.assertTrue(payments.validate_payment(ok_payment, all_payments))
        self.assertFalse(payments.validate_payment(bad_payment, all_payments))

    def test_unknown_method_is_rejected(self):
        """Metodos desconocidos tienen que ser rechazados"""
        payment = self.make_payment(100, "Bitcoin")
        all_payments = {}
        self.assertFalse(payments.validate_payment(payment, all_payments))

    def test_credit_card_only_one_registered_allowed(self):
        """Debe rechazar si ya hay otro pago REGISTRADO con tarjeta."""
        all_payments = {
            "1": {
                models.PAYMENT_METHOD: models.CREDIT_CARD,
                models.STATUS: models.STATUS_REGISTRADO,
                models.AMOUNT: 1000,
            }
        }
        new_payment = self.make_payment(500, models.CREDIT_CARD)
        self.assertFalse(payments.validate_payment(new_payment, all_payments))

    def test_credit_card_accepts_first_valid_payment(self):
        """No rechaza si los payments registrados estan con status PAGADO"""
        all_payments = {
            "1": {
                models.PAYMENT_METHOD: models.CREDIT_CARD,
                models.STATUS: models.STATUS_PAGADO,
                models.AMOUNT: 5000,
            }
        }
        new_payment = self.make_payment(500, models.CREDIT_CARD)
        self.assertTrue(payments.validate_payment(new_payment, all_payments))

if __name__ == '__main__':
    unittest.main()
