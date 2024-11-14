from application import create_app, db
from flask_cors import CORS
from populate_db import populate_database

app = create_app()
CORS(app)

# Cria as tabelas no banco de dados
with app.app_context():
    db.create_all()
    populate_database()

if __name__ == '__main__':
    app.run(debug=True)


