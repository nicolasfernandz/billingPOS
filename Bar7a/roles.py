'''
Created on 21 set. 2017

1. http://django-role-permissions.readthedocs.io/en/stable/
2. pip install django-role-permissions
3. python manage.py shell (Para despues poder asignar roles a usuarios)
4. from rolepermissions.roles import assign_role
5. Crear usuarios en django admin
6. user = User.objects.get(username='[NombreDeUsuarioEnAdmin]')
7. assign_role(user, '[role]') el rol con minuscula
-> https://www.youtube.com/watch?v=f6Doj2LOIlo
@author: Juan
'''
from rolepermissions.roles import AbstractUserRole

class Barman(AbstractUserRole):
    available_permissions = {
        'access_informe_x': False,
        'access_informe_y': False,
    }

class Encargado(AbstractUserRole):
    available_permissions = {
        'access_informe_x': True,
        'access_informe_y': True,
    }    
    
class Contador(AbstractUserRole):
    available_permissions = {
        'access_informe_x': True,
        'access_informe_y': True,
        'access_reportes': True,
    }  