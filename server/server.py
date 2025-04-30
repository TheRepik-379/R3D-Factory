from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text, bindparam
connection_string = "mysql+pymysql://admin:123@192.168.0.106:3306/article"
engine = create_engine(connection_string, echo=True)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
@app.route("/")
def index():
    return "Hello world"
@app.route("/api/article/all")
def get_article():
    with engine.connect() as connection:
        raw_article = connection.execute(text("SELECT * FROM article"))
        article = []
        for i in raw_article.all():
            article.append(i._asdict())
        return jsonify(article)
    return Response(jsonify({"status": "500", "message": "Database is down!"}), status=500)

@app.route("/api/article", methods=["POST"])
def add_article():
    if request.method == "POST":
        form = request.form
        with engine.connect() as connection:
            query = text("INSERT INTO article (Heading, description, picture, dfc) VALUES (:Heading, :description, :picture, :dfc) RETURNING *")
            query = query.bindparams(bindparam("Heading", form.get("Heading")))
            query = query.bindparams(bindparam("description", form.get("description")))
            query = query.bindparams(bindparam("picture", form.get("picture")))
            query = query.bindparams(bindparam("dfc", form.get("dfc")))
            result = connection.execute(query)
            connection.commit()
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})
@app.route("/api/article/<id>", methods=["DELETE","GET","PUT"])
def delete_article(id: int):
    if request.method == "DELETE":
        with engine.connect() as connection:
            query = text("DELETE FROM article WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            connection.commit()
            return jsonify({"message": "Success", "id": id})
        return jsonify({"message": "Записи с таким id не существует"})
    if request.method == "GET":
        with engine.connect() as connection:
            query = text("SELECT * FROM article WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})
    if request.method == "PUT":
        form = request.form
        with engine.connect() as connection:
            query = text("UPDATE article SET Heading = :Heading, description = :description, picture = :picture, dfc = :dfc WHERE id = :id")
            query = query.bindparams(bindparam("Heading", form.get("Heading")))
            query = query.bindparams(bindparam("description", form.get("description")))
            query = query.bindparams(bindparam("picture", form.get("picture")))
            query = query.bindparams(bindparam("dfc", form.get("dfc")))
            query = query.bindparams(bindparam("id", id))
            connection.execute(query)
            connection.commit()
            query = text("SELECT * FROM article WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})


@app.route("/api/article_page/<id>", methods=["GET"])
def get_article_page(id: int):
    if request.method == "GET":
        with engine.connect() as connection:
            query = text("SELECT * FROM article WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})

def main():
    app.run("localhost", 8000, True)
if __name__ == "__main__":
    main()