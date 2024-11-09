from app import create_app, db
from app.models import Usuario, Quarto, Reserva

app = create_app()

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
