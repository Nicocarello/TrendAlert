import os
import smtplib
from email.message import EmailMessage
from apify_client import ApifyClient

# 🔐 Cargar credenciales desde variables de entorno (secrets)
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")

DESTINATARIOS_ML = [email.strip() for email in os.getenv("DESTINATARIOS_ML", "").split(",")]
DESTINATARIOS_MP = [email.strip() for email in os.getenv("DESTINATARIOS_MP", "").split(",")]

# Inicializa el cliente de Apify
apify_client = ApifyClient(APIFY_API_TOKEN)

ACTOR_ID = "karamelo/twitter-trends-scraper"

run_inputs = {
    "country": "29",  # Argentina
    "day2": False,
    "day3": False,
    "hour1": False,
    "hour12": False,
    "hour24": False,
    "hour3": False,
    "hour6": False,
    "live": True,
    "proxyOptions": {
        "useApifyProxy": True
    }
}

# Ejecutar actor
run = apify_client.actor(ACTOR_ID).call(run_input=run_inputs)

# Obtener resultados del dataset
dataset_id = run.get("defaultDatasetId")
items = apify_client.dataset(dataset_id).list_items().items or []

# Palabras clave divididas por categoría
keywords_ml = ['mercado libre', 'mercadolibre']
keywords_mp = ['mercado pago', 'mercadopago']

norm_ml = [k.replace(' ', '').lower() for k in keywords_ml]
norm_mp = [k.replace(' ', '').lower() for k in keywords_mp]

def _normalize(s):
    return (s or '').lower().replace(' ', '')

# Buscar coincidencias
matches_ml = []
matches_mp = []

for idx, it in enumerate(items):
    trend = it.get('trend', '')
    volume = it.get('volume', 'N/A')
    norm_trend = _normalize(trend)

    found_ml = [kw for kw in norm_ml if kw in norm_trend]
    found_mp = [kw for kw in norm_mp if kw in norm_trend]

    if found_ml:
        matches_ml.append({
            'index': idx + 1,
            'trend': trend,
            'volume': volume,
            'matches': found_ml
        })

    if found_mp:
        matches_mp.append({
            'index': idx + 1,
            'trend': trend,
            'volume': volume,
            'matches': found_mp
        })

# Función para enviar correos
def enviar_correo(asunto, destinatarios, coincidencias):
    html_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; color: #333;">
        <h2 style="color: #d9534f;">🚨 {asunto}</h2>
        <p>Se detectaron las siguientes <strong>tendencias</strong> relacionadas:</p>
    """

    for m in coincidencias:
        volumen_texto = f"{m['volume']} tweets" if m['volume'] != 'N/A' else "volumen no disponible"
        html_body += f"""
        <div style="margin-bottom: 15px; font-size: 16px;">
            <strong>{m['trend']}</strong> es tendencia N° <strong>{m['index']}</strong> en Argentina con <strong>{volumen_texto}</strong>.<br>
            <span style="font-size: 13px; color: #555;">(Coincidencias: {', '.join(m['matches'])})</span>
        </div>
        """

    html_body += """
        <p style="margin-top: 30px; font-size: 13px; color: #888;">
            Este mensaje fue generado automáticamente por el sistema de monitoreo de tendencias en Twitter.
        </p>
    </body>
    </html>
    """

    msg = EmailMessage()
    msg['Subject'] = asunto
    msg['From'] = EMAIL_SENDER
    msg['To'] = ', '.join(destinatarios)
    msg.set_content("Se detectaron nuevas tendencias relevantes en Twitter.")  # Fallback de texto plano
    msg.add_alternative(html_body, subtype='html')

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f'✅ Correo enviado a: {msg["To"]}')
    except Exception as e:
        print(f'❌ Error al enviar correo a {msg["To"]}:', e)

# Enviar correos según coincidencias
if matches_ml:
    enviar_correo("🚨 Alerta Tendencia: Mercado Libre", DESTINATARIOS_ML, matches_ml)

if matches_mp:
    enviar_correo("🚨 Alerta Tendencia: Mercado Pago", DESTINATARIOS_MP, matches_mp)

if not matches_ml and not matches_mp:
    print("🔍 No hay tendencias de Mercadolibre o Mercado Pago.")
