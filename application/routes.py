from datetime import datetime

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, logout_user, login_required
from application.functions import (
    atualizar_reserva,
    realizar_login,
    listar_quartos_disponiveis,
    reservar_quarto,
    obter_minhas_reservas,
    pagar_reserva,
    excluir_reserva
)

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/booking')
def booking():
    return render_template('booking.html')


@main.route('/mybooking')
def mybooking():
    return render_template('mybooking.html')


@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    response, status = realizar_login(email, senha)
    if status == 200:
        login_user(response['user'])
    return jsonify({"message": response['message']}), status


@main.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout realizado com sucesso!"}), 200


@main.route('/quartos-disponiveis', methods=['GET'])
def listar_quartos_disponiveis_route():
    return jsonify(listar_quartos_disponiveis()), 200


@main.route('/reservar-quarto', methods=['POST'])
@login_required
def reservar_quarto_route():
    data = request.get_json()
    id_quarto = data.get('id_quarto')
    data_entrada = datetime.strptime(data.get('data_entrada'), '%Y-%m-%d')
    data_saida = datetime.strptime(data.get('data_saida'), '%Y-%m-%d')
    preco = data.get('preco', 0.0)

    response, status = reservar_quarto(id_quarto, data_entrada, data_saida, preco)
    return jsonify({"message": response}), status


@main.route('/minhas_reservas', methods=['GET'])
def minhas_reservas():
    reservas = obter_minhas_reservas()
    return jsonify({'reservas': reservas})


@main.route('/pagar-reserva/<int:id_reserva>', methods=['PUT'])
@login_required
def pagar_reserva_route(id_reserva):
    response, status = pagar_reserva(id_reserva)
    return jsonify({"message": response['message']}), status


@main.route('/editar-reserva/<int:id_reserva>', methods=['PUT'])
@login_required
def editar_reserva_route(id_reserva):
    data = request.get_json()
    return atualizar_reserva(id_reserva, data['data_entrada'], data['data_saida'])


@main.route('/excluir-reserva/<int:id_reserva>', methods=['DELETE'])
@login_required
def excluir_reserva_route(id_reserva):
    response, status = excluir_reserva(id_reserva)
    return jsonify({"message": response['message']}), status
