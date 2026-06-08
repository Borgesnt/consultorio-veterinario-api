import json
import pika
from datetime import datetime

from server.utils.database import carregar, salvar


def registrar_evento(db, mensagem):
    db["eventos"].append({
        "hora": datetime.now().strftime("%H:%M:%S"),
        "evento": mensagem
    })


def callback(ch, method, properties, body):

    try:

        data = json.loads(body)

        db = carregar()

        acao = data["acao"]

        if acao == "cadastrar_animal":

            animal = data["dados"]

            db["animais"].append(animal)

            registrar_evento(
                db,
                f"Animal '{animal['nome']}' cadastrado"
            )

            print(
                f"[OK] Animal cadastrado: {animal['nome']}"
            )

        elif acao == "registrar_consulta":

            consulta = data["dados"]

            db["consultas"].append(consulta)

            registrar_evento(
                db,
                f"Consulta registrada para {consulta['animal']}"
            )

            print(
                f"[OK] Consulta registrada para {consulta['animal']}"
            )

        else:

            registrar_evento(
                db,
                f"Ação desconhecida: {acao}"
            )

            print(
                f"[ERRO] Ação desconhecida: {acao}"
            )

        db["mensagens_processadas"] += 1

        salvar(db)

        ch.basic_ack(
            delivery_tag=method.delivery_tag
        )

    except Exception as e:

        print(f"[ERRO] {e}")

        ch.basic_nack(
            delivery_tag=method.delivery_tag,
            requeue=True
        )


connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

channel.queue_declare(
    queue="clinica_queue",
    durable=True
)

channel.basic_qos(
    prefetch_count=1
)

channel.basic_consume(
    queue="clinica_queue",
    on_message_callback=callback
)

print("=" * 50)
print(" CONSUMIDOR CLÍNICA VETERINÁRIA")
print("Aguardando mensagens...")
print("=" * 50)

channel.start_consuming()