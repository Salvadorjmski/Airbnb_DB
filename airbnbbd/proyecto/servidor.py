
from propiedades import listar_propiedades, crear_propiedad_con_ubicacion, eliminar_propiedad
from reservas import crear_reserva_y_pago
from reportes import reporte_reservas_detallado, reporte_ingresos_por_anfitrion
from bd_conections import get_conn
from usuarios import listar_anfitriones, listar_huespedes, buscar_usuario_por_correo

        
def menu(cn):
    while True:
        print("""
================ MENÚ ================
1) Listar propiedades
2) Crear propiedad + ubicación
3) Crear reserva y/o pago 
4) Reporte reservas detalladas
5) Reporte ingresos por anfitrión
6) Eliminar propiedad
7) Listar ANFITRIONES
8) Listar HUÉSPEDES
9) Buscar usuario por CORREO
0) Salir
""")
        op = input("Opción: ").strip()
        if   op == "1": listar_propiedades(cn)
        elif op == "2": crear_propiedad_con_ubicacion(cn)
        elif op == "3": crear_reserva_y_pago(cn)
        elif op == "4": reporte_reservas_detallado(cn)
        elif op == "5": reporte_ingresos_por_anfitrion(cn)
        elif op == "6": eliminar_propiedad(cn)
        elif op == "7": listar_anfitriones(cn)
        elif op == "8": listar_huespedes(cn)
        elif op == "9": buscar_usuario_por_correo(cn)
        elif op == "0": break
        else: print("Opción inválida.")


def main():                       
    cn = get_conn()
    if not cn:
        print("No se pudo abrir la conexión. Revise firewall Azure.")
        return
    try:
        print("Conectado:", cn.is_connected())
        menu(cn)
    finally:
        try:
            cn.close()
        except Exception:
            pass
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
