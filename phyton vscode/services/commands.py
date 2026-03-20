from database import cursor, conn
from services.whatsapp import enviar

def processar(numero, texto):

    if texto.startswith("add"):
        try:
            partes = texto.split(" ", 2)
            tarefa_hora = partes[2]
            tarefa, horario = tarefa_hora.rsplit(" ", 1)

            cursor.execute(
                "INSERT INTO tarefas (usuario, tarefa, horario) VALUES (?, ?, ?)",
                (numero, tarefa, horario)
            )
            conn.commit()

            enviar(numero, f"✅ '{tarefa}' às {horario}")

        except:
            enviar(numero, "Formato: add tarefa HH:MM")

    elif texto.startswith("done"):
        tarefa = texto.replace("done ", "")

        cursor.execute(
            "UPDATE tarefas SET concluido=1 WHERE usuario=? AND tarefa=?",
            (numero, tarefa)
        )
        conn.commit()

        enviar(numero, f"✔ Concluído: {tarefa}")

    elif texto == "lista":
        cursor.execute(
            "SELECT tarefa, horario, concluido FROM tarefas WHERE usuario=?",
            (numero,)
        )

        dados = cursor.fetchall()

        if not dados:
            enviar(numero, "📭 Lista vazia")
            return

        msg = "📋 Checklist:\n"
        for t in dados:
            status = "✅" if t[2] else "❌"
            msg += f"{status} {t[0]} - {t[1]}\n"

        enviar(numero, msg)

    else:
        enviar(numero,
        "Comandos:\n"
        "add tarefa HH:MM\n"
        "done tarefa\n"
        "lista")