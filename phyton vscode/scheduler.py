from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from database import cursor, conn
from services.whatsapp import enviar

scheduler = BackgroundScheduler()

def lembretes():
    agora = datetime.now().strftime("%H:%M")

    cursor.execute(
        "SELECT usuario, tarefa FROM tarefas WHERE horario=? AND concluido=0",
        (agora,)
    )

    for user, tarefa in cursor.fetchall():
        enviar(user, f"⏰ Lembrete: {tarefa}")

def reset():
    cursor.execute("UPDATE tarefas SET concluido=0")
    conn.commit()

def iniciar_scheduler():
    scheduler.add_job(lembretes, 'interval', minutes=1)
    scheduler.add_job(reset, 'cron', hour=0, minute=0)
    scheduler.start()