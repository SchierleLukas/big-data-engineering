from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

@app.route("/anomalies", methods=["GET"])
def get_anomalies():
    conn = mysql.connector.connect(user="root", password="password", host="mariadb", database="logs")
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM anomalies")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
