from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuring a mysql connection
db_config = {
    'host': 'esaqrio.mysql.pythonanywhere-services.com',
    'port': 3306,
    'user': 'esaqrio',
    'password': 'umbreon99',
    'database': 'esaqrio$default'
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loomians/delete", methods=["POST"])
def delete_loomian():
    loomian_id = request.form["loomian_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Deleting the loomian
    cursor.execute("DELETE FROM Loomian_attack WHERE loomian_id = %s", (loomian_id,))
    cursor.execute("DELETE FROM Loomian_party WHERE loomian_id = %s", (loomian_id,))
    cursor.execute("DELETE FROM Loomian WHERE id = %s", (loomian_id,))

    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("loomians"))

@app.route("/loomians")
def loomians():
    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)

    # Fetching loomians from the database
    cursor.execute("SELECT * FROM Loomian")
    loomians = cursor.fetchall()

    # Ending the connection
    cursor.close()
    con.close()

    return render_template("loomians.html", loomians=loomians)

@app.route("/loomians/add", methods=["POST"])
def add_loomian():
    id = request.form["id"]
    name = request.form["name"]
    main_type = request.form["main_type"]
    secondary_type = request.form["secondary_type"]
    ability = request.form["ability"]
    melee_attack = request.form["melee_attack"]
    melee_defense = request.form["melee_defense"]
    ranged_attack = request.form["ranged_attack"]
    ranged_defense = request.form["ranged_defense"]
    speed = request.form["speed"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Adding loomian to the database
    cursor.execute("INSERT INTO Loomian (id, name, main_type, secondary_type, ability, melee_attack, melee_defense, ranged_attack, ranged_defense, speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (id, name, main_type, secondary_type, ability, melee_attack, melee_defense, ranged_attack, ranged_defense, speed))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("loomians"))

@app.route("/delete_party", methods=["POST"])
def delete_party():
    party_id = request.form["party_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Deleting the party
    cursor.execute("DELETE FROM Loomian_party WHERE party_id = %s", (party_id,))
    cursor.execute("DELETE FROM Party WHERE id = %s", (party_id,))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("show_parties"))

@app.route("/parties")
def show_parties():
    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)

    # Fetching parties from the database
    cursor.execute("SELECT * FROM Party")
    parties = cursor.fetchall()

    # Ending the connection
    cursor.close()
    con.close()

    return render_template("manage_parties.html", parties=parties)

@app.route("/parties/create", methods=["POST"])
def create_party():
    name = request.form["name"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Creating a new party
    cursor.execute("INSERT INTO Party (name) VALUES (%s)", (name,))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("show_parties"))

@app.route("/parties/<int:party_id>")
def view_party(party_id):
    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)

    # Fetching party id
    cursor.execute("SELECT * FROM Party WHERE id = %s", (party_id,))
    party = cursor.fetchone()

    # Fetching loomians in the party
    cursor.execute(""" SELECT l.* FROM Loomian l JOIN Loomian_party lp ON l.id = lp.loomian_id
        WHERE lp.party_id = %s""", (party_id,))
    loomians = cursor.fetchall()

    #Adding more loomians
    cursor.execute("SELECT * FROM Loomian")
    all_loomians = cursor.fetchall()

    # Ending the connection
    cursor.close()
    con.close()

    return render_template("view_party.html", party=party, loomians=loomians, all_loomians=all_loomians)

@app.route("/parties/<int:party_id>/add", methods=["POST"])
def add_loomian_to_party(party_id):
    loomian_id = request.form["loomian_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Adding loomian to the party
    cursor.execute("INSERT IGNORE INTO Loomian_party (party_id, loomian_id) VALUES (%s, %s)", (party_id, loomian_id))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("view_party", party_id=party_id))

@app.route("/remove_loomian_from_party", methods=["POST"])
def remove_loomian_from_party():
    party_id = request.form["party_id"]
    loomian_id = request.form["loomian_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Removing loomian from the party
    cursor.execute("DELETE FROM Loomian_party WHERE party_id = %s AND loomian_id = %s", (party_id, loomian_id))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("view_party", party_id=party_id, loomian_id=loomian_id))

@app.route("/loomian/<int:loomian_id>/remove_attack", methods=["POST"])
def remove_attack(loomian_id):
    attack_id = request.form["attack_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Removing attack from the loomian
    cursor.execute("DELETE FROM Loomian_attack WHERE loomian_id = %s AND attack_id = %s", (loomian_id, attack_id))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("manage_attacks", loomian_id=loomian_id))

@app.route("/attacks/delete", methods=["POST"])
def delete_attack():
    attack_id = request.form["attack_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Deleting the attack
    cursor.execute("DELETE FROM Loomian_attack WHERE attack_id = %s", (attack_id,))
    cursor.execute("DELETE FROM Attack WHERE id = %s", (attack_id,))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("show_attacks"))

@app.route("/attacks")
def show_attacks():
    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)

    # Fetching attacks from the database
    cursor.execute("SELECT * FROM Attack")
    attacks = cursor.fetchall()

    # Ending the connection
    cursor.close()
    con.close()

    return render_template("attacks.html", attacks=attacks)

@app.route("/attacks/create", methods=["POST"])
def create_attack():
    id = request.form["id"]
    name = request.form["name"]
    type = request.form["type"]
    power = request.form["power"]
    accuracy = request.form["accuracy"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Creating attack in the database
    cursor.execute("INSERT INTO Attack (id, name, type, power, accuracy) VALUES (%s, %s, %s, %s, %s)", (id, name, type, power, accuracy))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("show_attacks"))

@app.route("/loomian/<int:loomian_id>/attacks", methods=["GET","POST"])
def manage_attacks(loomian_id):
    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor(dictionary=True)

    # Fetching loomian id
    cursor.execute("SELECT * FROM Loomian WHERE id = %s", (loomian_id,))
    loomian = cursor.fetchone()

    # Fetching assigned attacks
    cursor.execute(""" SELECT a.* FROM Attack a JOIN Loomian_attack la ON a.id = la.attack_id
        WHERE la.loomian_id = %s""", (loomian_id,))
    attacks = cursor.fetchall()

    #Adding more attacks
    cursor.execute("SELECT * FROM Attack")
    all_attacks = cursor.fetchall()

    #Filtering out already assigned attacks
    assigned_attack_ids = {attack['id'] for attack in attacks}
    available_attacks = [attack for attack in all_attacks if attack['id'] not in assigned_attack_ids]

    # Ending the connection
    cursor.close()
    con.close()

    return render_template("manage_attacks.html", loomian_id=loomian_id, loomian=loomian, attacks=attacks, available_attacks=available_attacks)

@app.route("/loomian/<int:loomian_id>/add_attack", methods=["POST"])
def add_attack(loomian_id):
    attack_id = request.form["attack_id"]

    # Connecting to database
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Adding attack to the loomian
    cursor.execute("INSERT IGNORE INTO Loomian_attack (loomian_id, attack_id) VALUES (%s, %s)", (loomian_id, attack_id))
    con.commit()

    # Ending the connection
    cursor.close()
    con.close()

    return redirect(url_for("manage_attacks", loomian_id=loomian_id))

if __name__ == "__main__":
    app.run(debug=True)
