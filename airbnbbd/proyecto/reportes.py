def reporte_reservas_detallado(cn):
    print("\n=== Reporte: Reservas detalladas ===")
    estado = input("Filtrar estado (pendiente/confirmada/cancelada/completada o ENTER): ").strip().lower()
    ciudad = input("Filtrar ciudad (ENTER = todas): ").strip()

    params, where = [], []
    if estado:
        where.append("r.estado = %s")
        params.append(estado)
    if ciudad:
        where.append("ub.ciudad = %s")
        params.append(ciudad)
    where_clause = "WHERE " + " AND ".join(where) if where else ""

    sql = f"""
    SELECT r.id_reserva, r.date_inicio, r.date_fin, r.estado, r.precio_total,
           hu.nombre AS huesped,
           pr.id_propiedad, pr.tipo, pr.precio,
           ub.ciudad, ub.pais
    FROM Reserva r
    JOIN Usuario hu ON hu.id_usuario = r.id_huesped
    JOIN Propiedad pr ON pr.id_propiedad = r.id_propiedad
    JOIN Ubicacion ub ON ub.id_ubicacion = pr.id_ubicacion
    {where_clause}
    ORDER BY r.date_inicio DESC, r.id_reserva DESC
    """
    cur = cn.cursor(dictionary=True)
    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    if not rows:
        print("Sin resultados.")
        return
    for x in rows:
        print(f"[{x['id_reserva']}] {x['date_inicio']}→{x['date_fin']}  {x['estado']:>10} | "
              f"H: {x['huesped']} | Prop {x['id_propiedad']} {x['tipo']} "
              f"{x['ciudad']} ({x['pais']}) | Total: {x['precio_total']}")

def reporte_ingresos_por_anfitrion(cn):
    """JOIN + GROUP BY: ingresos sumados por anfitrión."""
    print("\n=== Reporte: Ingresos por anfitrión ===")
    cur = cn.cursor(dictionary=True)
    cur.execute("""
        SELECT a.id_usuario AS id_anfitrion, a.nombre AS anfitrion,
               COUNT(DISTINCT r.id_reserva) AS reservas,
               COALESCE(SUM(pg.monto_total),0) AS ingresos
        FROM Propiedad pr
        JOIN Usuario a ON a.id_usuario = pr.anfitrion_id
        LEFT JOIN Reserva r ON r.id_propiedad = pr.id_propiedad
        LEFT JOIN Pago pg ON pg.id_reserva = r.id_reserva
        GROUP BY a.id_usuario, a.nombre
        ORDER BY ingresos DESC, reservas DESC
    """)
    for x in cur.fetchall():
        print(f"{x['anfitrion']:<20} | reservas: {x['reservas']:<3} | ingresos: {x['ingresos']:.2f}")
