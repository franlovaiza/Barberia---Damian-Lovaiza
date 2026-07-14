import resend
from config import settings

resend.api_key = settings.RESEND_API_KEY


def _formatear_fecha(fecha) -> str:
    """Convierte la fecha (date o datetime) a un formato lindo en español, ej: '10 de agosto de 2026'."""
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
    ]
    try:
        return f"{fecha.day} de {meses[fecha.month - 1]} de {fecha.year}"
    except Exception:
        return str(fecha)


def enviar_confirmacion_turno(turno) -> None:
    """
    Envía un mail de confirmación al cliente cuando reserva un turno.
    Si falta la API key de Resend (por ejemplo, en desarrollo local sin configurar),
    no rompe la creación del turno: solo avisa por consola y sigue.
    """
    if not settings.RESEND_API_KEY:
        print("⚠️  RESEND_API_KEY no configurada. No se envió el mail de confirmación.")
        return

    fecha_legible = _formatear_fecha(turno.fecha)
    hora_legible = str(turno.hora)[:5]  # "10:00:00" -> "10:00"

    metodo_pago = getattr(turno, "metodo_pago", "Efectivo") or "Efectivo"
    bloque_pago = f"""
                <tr>
                    <td style="padding: 8px 0; color: #666;">Pago:</td>
                    <td style="padding: 8px 0; font-weight: bold;">{metodo_pago}</td>
                </tr>
    """
    aviso_transferencia = ""
    if metodo_pago.lower() == "transferencia":
        aviso_transferencia = """
            <div style="background: #fff8e6; border: 1px solid #e0d3b8; border-radius: 8px; padding: 12px 16px; margin: 16px 0;">
                <p style="margin: 0; font-size: 14px;">💳 Transferí a <strong>Naranja X, alias: LOVAIZADL</strong></p>
            </div>
        """

    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 480px; margin: auto; border: 1px solid #e0d3b8; border-radius: 12px; overflow: hidden;">
        <div style="background: #1a1a1a; padding: 24px; text-align: center;">
            <h1 style="color: #d9b25f; margin: 0; font-size: 22px;">¡Turno confirmado!</h1>
        </div>
        <div style="padding: 24px; color: #222;">
            <p>Hola <strong>{turno.nombre}</strong>,</p>
            <p>Tu turno en <strong>Barbería Damián Lovaiza</strong> quedó reservado con éxito. Estos son los detalles:</p>
            <table style="width: 100%; border-collapse: collapse; margin: 16px 0;">
                <tr>
                    <td style="padding: 8px 0; color: #666;">Servicio:</td>
                    <td style="padding: 8px 0; font-weight: bold;">{turno.tipo_turno}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;">Fecha:</td>
                    <td style="padding: 8px 0; font-weight: bold;">{fecha_legible}</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #666;">Hora:</td>
                    <td style="padding: 8px 0; font-weight: bold;">{hora_legible} hs</td>
                </tr>
                {bloque_pago}
            </table>
            {aviso_transferencia}
            <p>Si necesitás cancelar o cambiar el turno, contactanos con anticipación al
                <a href="https://wa.me/5493534264629" style="color: #a97c2f; font-weight: bold; text-decoration: none;">+54 9 3534264629</a>
                (WhatsApp Damian Lovaiza).
            </p>
            <p style="margin-top: 24px; color: #999; font-size: 13px;">¡Te esperamos!</p>
        </div>
    </div>
    """

    try:
        resend.Emails.send({
            "from": settings.MAIL_FROM or "Barbería Damián Lovaiza <turnos@barberialovaiza.com>",
            "to": [turno.email],
            "subject": "Confirmación de tu turno - Barbería Damián Lovaiza",
            "html": html,
        })
    except Exception as e:
        # No queremos que un error de mail rompa la reserva del turno.
        print(f"⚠️  Error al enviar mail de confirmación: {e}")