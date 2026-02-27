DB = csv

Reserva :

- ID
- Nombre del cliente
- Typo de reserva
- Fecha y hora de la reserva (YYYY-MM-DD HH:MM)
- Duración de la reserva (en horas)
- Coste total de la reserva (auto : typo.coste \* duración)
- estado de la reserva (confirmada, pendiente, cancelada o finalizada)

Typo de reserva :

- Nombre del typo de reserva
- tipo ('Grupo', 'Individual' o 'Acceso libre')
- precio por hora o por sesion

new_reserva:

- estado : default = 'pendiente'

func :

- create_reservation
- change_reservation_status
  Getters :
- get_reservation_from_status
- get_all_profit

# Unit tests :

- Change reservation status to unknow status
