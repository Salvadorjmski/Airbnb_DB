from mysql.connector import Error
from utils import input_date

def crear_reserva_y_pago(cn):

    print("\n=== Crear reserva y pago ===")
    try:
        id_prop    = int(input("ID Propiedad: ").strip())
        id_huesped = int(input("ID Huésped (Usuario): ").strip())
        check_in   = input_date("Fecha inicio")
        check_out  = input_date("Fecha fin")
        n_huesp    = int(input("N° huéspedes: ").strip())

        cur = cn.cursor(dictionary=True) #devuelve cada fila como diccionario
        cur.execute("SELECT precio FROM Propiedad WHERE id_propiedad=%s", (id_prop,))
        row = cur.fetchone()
        if not row:
            print("Propiedad no existe.")
            return

        nights = (check_out - check_in).days
        if nights <= 0:
            print("Las fechas son inválidas (fin > inicio).")
            return

        total = round(float(row["precio"]) * nights, 2)

        # Reserva
        cur.execute(
            "INSERT INTO Reserva (date_inicio, date_fin, estado, n_huespedes, precio_total, date_creacion, id_huesped, id_propiedad) "
            "VALUES (%s,%s,'confirmada',%s,%s,CURRENT_DATE,%s,%s)",
            (check_in, check_out, n_huesp, total, id_huesped, id_prop)
        )
        id_reserva = cur.lastrowid

        # Pago (opcional)
        metodo = input("Método de pago [TARJETA/EFECTIVO/TRANSFERENCIA] (ENTER para omitir): ").strip().upper()
        if metodo:
            comision = round(total * 0.07, 2)
            cur.execute(
                "INSERT INTO Pago (fecha_pago, monto_total, metodo_pago, comprobante, comision, id_reserva) "
                "VALUES (NOW(), %s, %s, %s, %s, %s)",
                (total, metodo, f"REC-{id_reserva:05d}", comision, id_reserva)
            )

        cn.commit()
        print(f" Reserva {id_reserva} creada por {nights} noche(s), total {total}.")
        if metodo:
            print("Pago registrado.")
    except Error as e:
        cn.rollback()
        print("X Error:", e)
