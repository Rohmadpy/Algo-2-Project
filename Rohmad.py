import webbrowser
import os
import psycopg2

# file_path = os.path.abspath("peta.html")
# webbrowser.open(f"file://{file_path}")

def clear_terminal():
    os.system('cls')
    
def kembali ():
    
    inputan_kembali = input("Tekan Enter untuk kembali ke menu utama...")
    if inputan_kembali == "":
        clear_terminal()
    else:
        kembali()

# Fungsi koneksi ke database
def connect_db():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="dtbase",
        user="postgres",
        password="Rohmad_25"
    )

# Fungsi registrasi dengan lokasi
 
def register(nama, no_hp, password, status_akun, latitude, longitude):
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Insert ke tabel akun
        cur.execute("""
            INSERT INTO akun (nama, no_hp, password, status_akun)
            VALUES (%s, %s, %s, %s) RETURNING id_akun;
        """, (nama, no_hp, password, status_akun))
        id_akun = cur.fetchone()[0]

        # Insert ke tabel lokasi
        cur.execute("""
            INSERT INTO lokasi (latitude, longitude, id_akun)
            VALUES (%s, %s, %s);
        """, (latitude, longitude, id_akun))

        conn.commit()
        print("Registrasi berhasil!")
        kembali()

    except psycopg2.IntegrityError:
        conn.rollback()
        print("Registrasi gagal: Nomor HP sudah digunakan atau data tidak valid.")
    except Exception as e:
        conn.rollback()
        print("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()

# LOGIN USER (cek dari tabel akun)
def login(no_hp, password):
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_akun, nama, status_akun FROM akun
            WHERE no_hp = %s AND password = %s;
        """, (no_hp, password))
        user = cur.fetchone()

        if user:
            menu_owner(no_hp)
            clear_terminal()
        else:
            print("Login gagal: Nomor HP atau password salah.")
            kembali()

    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
    finally:
        cur.close()
        conn.close()

# MENU UTAMA

def menu_owner(no_hp):
    clear_terminal()
    print(f"halo {no_hp} selamat datang di aplikasi petani")
    print("=========================menu utama=========================")
    print("1. penjualan hasil tani")
    print("2. Rute pengiriman ")
    print("3.pencatatan transaksi")
    print("4. pengelolaan stock")
    print("5. Keluar")
    pilihan = input("Masukkan pilihan anda: ")
    if pilihan == "1":
        penjualan_hasil_tani(no_hp)
    elif pilihan == "2":
        rute_pengiriman()
    elif pilihan == "3":
        pencatatan_transaksi()
    elif pilihan == "4":
        pengelolaan_stock()
    elif pilihan == "5":
        print("Terima kasih telah menggunakan aplikasi ini.")
        clear_terminal()
        exit()
    else:
        print("Pilihan tidak valid.")
        
def penjualan_hasil_tani():
    print("Menu Penjualan Hasil Tani")
    # Tambahkan logika untuk penjualan hasil tani

def rute_pengiriman():
    print("Menu Rute Pengiriman")
    # Tambahkan logika untuk rute pengiriman
def pengelolaan_stock():
    print("Menu Pengelolaan Stock")
    # Tambahkan logika untuk pengelolaan stock
def pencatatan_transaksi():
    print("Menu Pencatatan Transaksi")
    # Tambahkan logika untuk pencatatan transaksi

