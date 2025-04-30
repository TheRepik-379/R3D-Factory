from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text, bindparam

connection_string = "mysql+pymysql://r3df:12345@192.168.0.4:3306/r3dfactory-admin"
engine = create_engine(connection_string, echo=True)


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/")
def index():
    return "Hello world"

@app.route("/api/product/all")
def get_products():
    with engine.connect() as connection:
        raw_result = connection.execute(text("SELECT * FROM products"))
        result = []
        for r in raw_result.all():
            result.append(r._asdict())
        return jsonify(result)
    return Response(jsonify({"status": "500", "message": "Database is down!"}), status=500)

@app.route("/api/product", methods=["POST"])
def add_product():
    if request.method == "POST":
        form = request.form
        with engine.connect() as connection:
            query = text("INSERT INTO products (name, description, price, image) VALUES (:name, :description, :price, :image) RETURNING *")
            query = query.bindparams(bindparam("name", form.get("name")))
            query = query.bindparams(bindparam("description", form.get("description")))
            query = query.bindparams(bindparam("price", form.get("price")))
            query = query.bindparams(bindparam("image", form.get("image")))
            result = connection.execute(query)
            connection.commit()
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})

@app.route("/api/product/<id>", methods=["GET", "DELETE", "PUT"])
def product(id: int):
    if request.method == "GET":
        with engine.connect() as connection:
            query = text("SELECT * FROM products WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})
    if request.method == "DELETE":
        with engine.connect() as connection:
            query = text("DELETE FROM products WHERE id = :id;")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            connection.commit()
            return jsonify({"message": "Success", "id": id})
        return jsonify({"message": "Error"})
    if request.method == "PUT":
        form = request.form
        with engine.connect() as connection:
            query = text("UPDATE products SET name = :name, description = :description, price = :price, image = :image WHERE id = :id")
            query = query.bindparams(bindparam("name", form.get("name")))
            query = query.bindparams(bindparam("description", form.get("description")))
            query = query.bindparams(bindparam("price", form.get("price")))
            query = query.bindparams(bindparam("image", form.get("image")))
            query = query.bindparams(bindparam("id", id))
            connection.execute(query)
            connection.commit()
            query = text("SELECT * FROM products WHERE id = :id")
            query = query.bindparams(bindparam("id", id))
            result = connection.execute(query)
            return jsonify(result.fetchone()._asdict())
        return jsonify({"message": "Error"})


def main():
    app.run("localhost", 8000, True)

if __name__ == "__main__":
    main()