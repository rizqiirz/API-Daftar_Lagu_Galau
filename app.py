from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


# Muhammad Rizqi
# 2211102016
# IF10K


def koneksi_database():
    conn = None
    try:
        conn = pymysql.connect(
            host="127.0.0.1",
            database="daftar_lagu_galau",
            user="root",
            # password="",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.Error as e:
        print(e)
    return conn


@app.route("/lagu-galau", methods=["GET", "POST", "PUT", "DELETE"])
def kelola_lagu_galau():
    conn = koneksi_database()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM lagu_galau")
        lagu_galau = [
            dict(id=row["id"], judul=row["judul"], durasi=str(row["durasi"]), artis=row["artis"], album=row["album"], genre=row["genre"], tahun=row["tahun"])
            for row in cursor.fetchall()
        ]
        if lagu_galau:
            return jsonify(lagu_galau)
        else:
            return "Daftar Lagu Galau Masih Kosong!"

    if request.method == "POST":
        tambah_judul = request.form["judul"]
        tambah_durasi = request.form["durasi"]
        tambah_artis = request.form["artis"]
        tambah_album = request.form["album"]
        tambah_genre = request.form["genre"]
        tambah_tahun = request.form["tahun"]

        query_insert = (
            """INSERT INTO lagu_galau (judul, durasi, artis, album, genre, tahun) VALUES (%s, %s, %s, %s, %s, %s)"""
        )

        cursor.execute(query_insert, (tambah_judul, tambah_durasi, tambah_artis, tambah_album, tambah_genre, tambah_tahun))
        conn.commit()
        return "Berhasil Menambahkan Lagu Galau!"

    if request.method == "PUT":
        update_id = request.form["id"]
        update_judul = request.form["judul"]
        update_durasi = request.form["durasi"]
        update_artis = request.form["artis"]
        update_album = request.form["album"]
        update_genre = request.form["genre"]
        update_tahun = request.form["tahun"]

        query_update = """
            UPDATE lagu_galau
            SET judul=%s, durasi=%s, artis=%s, album=%s, genre=%s, tahun=%s
            WHERE id=%s
        """

        cursor.execute(query_update, (update_judul, update_durasi, update_artis, update_album, update_genre, update_tahun, update_id))
        conn.commit()
        return "Berhasil Memperbarui Informasi Lagu Galau!"

    if request.method == "DELETE":
        hapus_id = request.form["id"]

        query_delete = """DELETE FROM lagu_galau WHERE id=%s"""

        cursor.execute(query_delete, (hapus_id,))
        conn.commit()
        return "Berhasil Menghapus Lagu Galau!"


if __name__ == "__main__":
    app.run()
