from sqlalchemy.orm import Session
from db.models.turno_model import Turno
from schemas.turno_schema import TurnoCreate, TurnoSchema, TurnoOut
from fastapi import HTTPException
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from typing import List, Optional
from config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Para usar variables de entorno (recomendado):

fm = FastMail(conf)

def get_all_turnos_paginated(db: Session, skip: int = 0, limit: int = 15) -> List[TurnoOut]:
    turnos = db.query(Turno).offset(skip).limit(limit).all()
    return [TurnoOut(**t.__dict__) for t in turnos]

def get_turnos(db: Session) -> List[TurnoOut]:
    turnos = db.query(Turno).all()
    return [TurnoOut(**t.__dict__) for t in turnos]

def get_turno(db: Session, turno_id: int) -> Optional[TurnoSchema]:
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if turno:
        return TurnoSchema(**turno.__dict__)
    return None

async def create_turno(db: Session, turno: TurnoCreate) -> TurnoSchema:
    # Convertir el objeto time a string antes de guardar
    turno_data = turno.dict()
    turno_data['hora'] = turno.hora.strftime("%H:%M:%S")  # ✅ Convertir time a string
    
    db_turno = Turno(**turno_data)
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)

    try:
        message = MessageSchema(
                subject="✅ Confirmación de tu Reserva - Peluquería",
                recipients=[turno.email],
                body=crear_email_html(turno=TurnoSchema(**db_turno.__dict__)),
                subtype=MessageType.html
            )
        
        # Enviar el email
        await fm.send_message(message)

    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la reserva. Por favor intenta nuevamente."
        )
    
    return TurnoSchema(**db_turno.__dict__)

def update_turno(db: Session, turno_id: int, turno_update: TurnoCreate) -> Optional[TurnoSchema]:
    db_turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not db_turno:
        return None
    
    # Convertir el objeto time a string antes de actualizar
    turno_data = turno_update.dict()
    turno_data['hora'] = turno_update.hora.strftime("%H:%M:%S")  # ✅ Convertir time a string
    
    for field, value in turno_data.items():
        setattr(db_turno, field, value)
    
    db.commit()
    db.refresh(db_turno)
    return TurnoSchema(**db_turno.__dict__)

def delete_turno(db: Session, turno_id: int) -> bool:
    db_turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not db_turno:
        return False
    db.delete(db_turno)
    db.commit()
    return True

def crear_email_html(turno: TurnoSchema) -> str:
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: #ffffff;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
                border-radius: 10px 10px 0 0;
            }}
            .header h1 {{
                margin: 0;
                font-size: 28px;
            }}
            .content {{
                padding: 30px 20px;
                background: #f9f9f9;
            }}
            .detalle-box {{
                background: white;
                padding: 25px;
                margin: 20px 0;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            .detalle-item {{
                margin: 15px 0;
                display: flex;
                align-items: center;
            }}
            .icon {{
                font-size: 24px;
                margin-right: 10px;
                width: 30px;
            }}
            .label {{
                font-weight: bold;
                color: #667eea;
                margin-right: 8px;
            }}
            .value {{
                color: #333;
            }}
            .importante {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 14px;
                background: #f9f9f9;
                border-radius: 0 0 10px 10px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 15px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>✂️ ¡Reserva Confirmada!</h1>
                <p style="margin: 10px 0 0 0;">Tu cita ha sido agendada exitosamente</p>
            </div>
            
            <div class="content">
                <p>Hola <strong>{turno.nombre}</strong>,</p>
                <p>Nos complace confirmar tu reserva. Aquí están los detalles de tu cita:</p>
                
                <div class="detalle-box">
                    <div class="detalle-item">
                        <span class="icon">📅</span>
                        <span class="label">Fecha:</span>
                        <span class="value">{turno.fecha}</span>
                    </div>
                    <div class="detalle-item">
                        <span class="icon">🕐</span>
                        <span class="label">Hora:</span>
                        <span class="value">{turno.hora}</span>
                    </div>
                    <div class="detalle-item">
                        <span class="icon">💇</span>
                        <span class="label">Servicio:</span>
                        <span class="value">{turno.tipo_turno}</span>
                    </div>
                    <div class="detalle-item">
                        <span class="icon">📞</span>
                        <span class="label">Teléfono:</span>
                        <span class="value">{turno.telefono}</span>
                    </div>
                </div>
                
                <div class="importante">
                    <strong>⚠️ Importante:</strong>
                    <ul style="margin: 10px 0;">
                        <li>Por favor, llega 5 minutos antes de tu hora reservada</li>
                        <li>Si necesitas cancelar, avísanos con al menos 24hs de anticipación</li>
                        <li>Recuerda traer una toalla si lo prefieres</li>
                    </ul>
                </div>
                
                <p>Si necesitas modificar tu reserva, no dudes en contactarnos.</p>
            </div>
            
            <div class="footer">
                <p style="font-size: 16px; margin-bottom: 10px;">¡Te esperamos! 💜</p>
                <p style="font-size: 12px; color: #999;">
                    Este es un email automático. Por favor no respondas a este mensaje.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
