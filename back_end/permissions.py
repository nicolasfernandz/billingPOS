'''
Created on 21 set. 2017

@author: Juan
'''
from rolepermissions.permissions import register_object_checker
from Bar7a.roles import *

@register_object_checker()
def access_clinic(role, user, clinic):
    if role == Encargado:
        return True

    if user.clinic == clinic:
        return True

    return False

@register_object_checker()
def access_informe_x(role, user):
    if role == Encargado:
        return True

    return False

