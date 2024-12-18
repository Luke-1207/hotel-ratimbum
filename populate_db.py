from application import create_app, db
from application.models import Usuario, Quarto, Reserva
from werkzeug.security import generate_password_hash

app = create_app()


def populate_database():
    with app.app_context():
        db.session.query(Usuario).delete()
        db.session.query(Quarto).delete()
        db.session.query(Reserva).delete()

        db.session.commit()

        user = Usuario(
            nome="Cliente Teste",
            email="cliente@teste.com",
            senha=generate_password_hash("senhateste"),
            telefone="123456789",
            cpf="12345678901",
            endereco="Rua de Teste, 123"
        )
        db.session.add(user)

        for i in range(1, 51):
            quarto = Quarto(
                tipo='INDIVIDUAL' if i % 3 == 0 else 'DUPLO' if i % 3 == 1 else 'SUITE',
                status='DESOCUPADO'
            )
            db.session.add(quarto)

        db.session.commit()
        print("Banco de dados populado com sucesso!")
