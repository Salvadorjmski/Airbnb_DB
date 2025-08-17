# propiedades.py
from mysql.connector import Error

def listar_propiedades(cn):
    cur = cn.cursor(dictionary=True)
    cur.execute("""
        SELECT pr.id_propiedad, pr.tipo, pr.precio, pr.disponible,
               ub.ciudad, ub.pais, anfi.nombre AS anfitrion
        FROM Propiedad pr
        JOIN Ubicacion ub ON ub.id_ubicacion = pr.id_ubicacion
        JOIN Usuario   anfi ON anfi.id_usuario = pr.anfitrion_id
        ORDER BY pr.id_propiedad DESC
    """)
    rows = cur.fetchall()
    if not rows:
        print("No hay propiedades todavía.")
        return
    for x in rows:
        disp = "Sí" if x["disponible"] else "No"
        print(f"[{x['id_propiedad']}] {x['tipo']} ${x['precio']} {x['ciudad']} ({x['pais']}) "
              f"| anfitrión: {x['anfitrion']} | disponible: {disp}")

def crear_propiedad_con_ubicacion(cn):
    print("\n=== Crear propiedad + ubicación ===")
    try:
        anfitrion_id   = int(input("ID usuario ANFITRION: ").strip())
        tipo           = input("Tipo [CASA/DEPARTAMENTO/HABITACION/CABANA/OTRO]: ").strip().upper()
        n_habitaciones = int(input("N° habitaciones: ").strip())
        n_banos        = int(input("N° baños: ").strip())
        capacidad      = int(input("Capacidad huéspedes: ").strip())
        precio         = float(input("Precio por noche: ").strip())
        descripcion    = input("Descripción (opcional): ").strip() or None
        reglas         = input("Reglas (opcional): ").strip() or None

        print("Ubicación")
        pais       = input("País: ").strip()
        ciudad     = input("Ciudad: ").strip()
        direccion1 = input("Dirección 1: ").strip()
        direccion2 = input("Dirección 2 (opcional): ").strip() or None
        referencia = input("Referencia (opcional): ").strip() or None

        cur = cn.cursor()
        cur.execute(
            "INSERT INTO Ubicacion (pais, ciudad, direccion1, direccion2, referencia) "
            "VALUES (%s,%s,%s,%s,%s)",
            (pais, ciudad, direccion1, direccion2, referencia)
        )
        id_ubicacion = cur.lastrowid

        cur.execute(
            "INSERT INTO Propiedad (anfitrion_id, tipo, n_habitaciones, `n_baños`, capacidad, precio, "
            "descripcion, reglas, disponible, estado_aprobacion, id_arrendador, id_admin_aprobador, id_ubicacion) "
            "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,1,'pendiente',NULL,NULL,%s)",
            (anfitrion_id, tipo, n_habitaciones, n_banos, capacidad, precio,
             descripcion, reglas, id_ubicacion)
        )
        id_propiedad = cur.lastrowid
        cn.commit()
        print(f"✅ Propiedad {id_propiedad} creada con ubicación {id_ubicacion}.")
    except Error as e:
        cn.rollback()
        print("❌ Error:", e)

def eliminar_propiedad(cn):
    print("\n=== Eliminar propiedad ===")
    try:
        id_prop = int(input("ID Propiedad a eliminar: ").strip())
        cur = cn.cursor()
        cur.execute("DELETE FROM Propiedad WHERE id_propiedad=%s", (id_prop,))
        cn.commit()
        if cur.rowcount == 0:
            print("No se eliminó (no existe o tiene reservas).")
        else:
            print("🗑️ Propiedad eliminada.")
    except Error as e:
        cn.rollback()
        print("❌ Error:", e)

