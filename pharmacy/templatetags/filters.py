from django import template
from pharmacy.models import Prescription

register = template.Library()

@register.filter
def get_prescription_for_order(prescriptions, order):
    return prescriptions.filter(order=order).first()
