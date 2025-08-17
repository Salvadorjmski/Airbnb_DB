# usuarios.py
def listar_anfitriones(cn, limite=50):
    cur = cn.cursor(dictionary=True)
    cur.execute("""
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono,
               COUNT(DISTINCT p.id_propiedad) AS propiedades
        FROM Usuario u
        JOIN usuario_rol ur ON ur.id_usuario = u.id_usuario
        JOIN roles r ON r.id_rol = ur.id_rol AND r.nombre = 'ANFITRION'
        LEFT JOIN Propiedad p ON p.anfitrion_id = u.id_usuario
        GROUP BY u.id_usuario, u.nombre, u.correo, u.telefono
        ORDER BY propiedades DESC, u.nombre
        LIMIT %s
    """, (limite,))
    rows = cur.fetchall()
    if not rows:
        print("No hay anfitriones.")
        return
    print("\n=== Anfitriones ===")
    for x in rows:
        print(f"[{x['id_usuario']}] {x['nombre']:<20} {x['correo']:<25} "
              f"Tel: {x['telefono']:<12} | Propiedades: {x['propiedades']}")

def listar_huespedes(cn, limite=50):
    """Lista usuarios con rol HUESPED y cuántas reservas realizaron."""
    cur = cn.cursor(dictionary=True)
    cur.execute("""
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono,
               COUNT(DISTINCT res.id_reserva) AS reservas
        FROM Usuario u
        JOIN usuario_rol ur ON ur.id_usuario = u.id_usuario
        JOIN roles rl ON rl.id_rol = ur.id_rol AND rl.nombre = 'HUESPED'
        LEFT JOIN Reserva res ON res.id_huesped = u.id_usuario
        GROUP BY u.id_usuario, u.nombre, u.correo, u.telefono
        ORDER BY reservas DESC, u.nombre
        LIMIT %s
    """, (limite,))
    rows = cur.fetchall()
    if not rows:
        print("No hay huéspedes.")
        return
    print("\n=== Huéspedes ===")
    for x in rows:
        print(f"[{x['id_usuario']}] {x['nombre']:<20} {x['correo']:<25} "
              f"Tel: {x['telefono']:<12} | Reservas: {x['reservas']}")

def buscar_usuario_por_correo(cn):
    correo = input("Correo a buscar: ").strip()
    cur = cn.cursor(dictionary=True)
    cur.execute("""
        SELECT u.id_usuario, u.nombre, u.correo,
               GROUP_CONCAT(DISTINCT r.nombre ORDER BY r.nombre SEPARATOR ', ') AS roles
        FROM Usuario u
        LEFT JOIN usuario_rol ur ON ur.id_usuario = u.id_usuario
        LEFT JOIN roles r ON r.id_rol = ur.id_rol
        WHERE u.correo = %s
        GROUP BY u.id_usuario, u.nombre, u.correo
    """, (correo,))
    row = cur.fetchone()
    if not row:
        print("No se encontró ese correo.")
        return
    print(f"\nID: {row['id_usuario']} | Nombre: {row['nombre']} | Roles: {row['roles'] or '-'}")
