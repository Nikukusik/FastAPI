from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from config.general import MAIL_FROM, MAIL_USERNAME, MAIL_PORT, MAIL_SERVER, MAIL_PASSWORD

mail_conf = ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_PORT=MAIL_PORT,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_verification(email: str, body: str):
    message = MessageSchema(
        subject="Email verification",
        recipients=[email],
        body=body,
        subtype="html"
    )
    fm = FastMail(mail_conf)
    await fm.send_message(message)