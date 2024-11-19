from application.models import Usuario, Quarto, Reserva, db
from flask_login import current_user
from werkzeug.security import check_password_hash


def atualizar_reserva(id_reserva, data_entrada, data_saida):
    reserva = Reserva.query.get(id_reserva)
    if not reserva:
        return {"message": "Reserva não encontrada!"}

    reserva.data_entrada = data_entrada
    reserva.data_saida = data_saida
    db.session.commit()

    return {"message": "Reserva atualizada com sucesso!"}


def realizar_login(email, senha):
    user = Usuario.query.filter_by(email=email).first()
    if user and check_password_hash(user.senha, senha):
        return {"message": "Login realizado com sucesso!", "user": user}, 200
    else:
        return {"message": "Email ou senha inválidos!"}, 401


def listar_quartos_disponiveis():
    quartos = Quarto.query.filter_by(status='DESOCUPADO').all()
    return [{"id": q.id_quarto, "tipo": q.tipo, "status": q.status} for q in quartos]


def reservar_quarto(id_quarto, data_entrada, data_saida, preco):
    quarto = Quarto.query.get(id_quarto)
    if quarto and quarto.status == 'DESOCUPADO':
        reserva = Reserva(
            id_usuario=current_user.id_usuario,
            id_quarto=id_quarto,
            data_entrada=data_entrada,
            data_saida=data_saida,
            preco=preco,
            status_pagamento=False
        )
        quarto.status = 'RESERVADO'
        db.session.add(reserva)
        db.session.commit()
        return {"message": "Quarto reservado com sucesso!"}, 201
    else:
        return {"message": "Quarto não disponível para reserva."}, 400


def obter_minhas_reservas():
    reservas = Reserva.query.filter_by(id_usuario=current_user.id_usuario).all()
    reservas_info = []

    for reserva in reservas:
        quarto = Quarto.query.get(reserva.id_quarto)
        reservas_info.append({
            "id_reserva": reserva.id_reserva,
            "id_quarto": reserva.id_quarto,
            "tipo_quarto": quarto.tipo,
            "status_quarto": quarto.status,
            "data_entrada": reserva.data_entrada.strftime('%Y-%m-%d'),
            "data_saida": reserva.data_saida.strftime('%Y-%m-%d'),
            "preco": reserva.preco,
            "status_pagamento": reserva.status_pagamento
        })

    if reservas_info:
        return reservas_info
    else:
        return {"message": "Você não tem reservas no momento."}


def pagar_reserva(id_reserva):
    reserva = Reserva.query.get(id_reserva)
    if reserva and reserva.id_usuario == current_user.id_usuario:
        reserva.status_pagamento = True
        db.session.commit()
        return {"message": "Pagamento realizado com sucesso!"}, 200
    else:
        return {"message": "Reserva não encontrada ou acesso negado."}, 404


def excluir_reserva(id_reserva):
    reserva = Reserva.query.get(id_reserva)
    if reserva and reserva.id_usuario == current_user.id_usuario:
        quarto = Quarto.query.get(reserva.id_quarto)
        quarto.status = 'DESOCUPADO'
        db.session.delete(reserva)
        db.session.commit()
        return {"message": "Reserva excluída com sucesso!"}, 200
    else:
        return {"message": "Reserva não encontrada ou acesso negado."}, 404
