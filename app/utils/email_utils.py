import resend
from app.core.config import settings

resend.api_key = settings.RESEND_API_KEY

def send_password_reset_email(to_email: str, reset_token: str) -> None:
    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
    resend.Emails.send({
        "from": "Aznaoure Art <onboarding@resend.dev>",
        "to": [to_email],
        "subject": "Reset your Aznaoure Art password",
        "html": f"""
            <p>We received a request to reset your password.</p>
            <p><a href="{reset_link}">Click here to reset your password</a></p>
            <p>This link expires in {settings.RESET_TOKEN_EXPIRE_MINUTES} minutes.
            If you didn't request this, you can ignore this email.</p>
        """,
    })