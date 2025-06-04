
import psycopg2
import webbrowser
import os
from datetime import date
from tabulate import tabulate
import time

# file_path = os.path.abspath("peta.html")
# webbrowser.open(f"file://{file_path}")
def connect_db():
    conn = psycopg2.connect(
    host="localhost",
    database="Algo2",
    user="postgres",
    password="",
    port=5432
    )     
    return conn

def clear_terminal():
    os.system('cls')
    
def kembali ():
    
    inputan_kembali = input("Tekan Enter untuk kembali ke menu utama...")
    if inputan_kembali == "":
        clear_terminal()
    else:
        kembali()
        
def main():
    while True:
        print("\n=== MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == "1":
            os.system('cls')
            nama = input("Nama: ")
            no_hp = input("No HP: ")
            password = input("Password (max 8 karakter): ")
            # status_akun = input("Status akun (misalnya A): ")
            # latitude = float(input("Latitude: "))
            # longitude = float(input("Longitude: "))
            register(nama, no_hp, password)
            os.system('cls')

        elif pilihan == "2":
            no_hp = input("No HP: ")
            password = input("Password: ")
            login(no_hp, password)
            os.system('cls')

        elif pilihan == "3":
            print("Keluar dari program.")
            os.system('cls')
            break

        else:
            print("Pilihan tidak valid.")


def register(nama, no_hp, password):
    print("Memuat Peta", end="")
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.5) 
    file_path = os.path.abspath("peta.html")
    webbrowser.open(f"file://{file_path}")
    lokasi=input("Masukkan Lokasi Anda : ")
    latitude,longitude=lokasi.split(',')
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Insert ke tabel akun
        cur.execute("""
            INSERT INTO akun (nama, no_hp, password, status_akun)
            VALUES (%s, %s, %s, %s) RETURNING id_akun;
        """, (nama, no_hp, password, "1"))
        id_akun = cur.fetchone()[0]

        # Insert ke tabel lokasi
        cur.execute("""
            INSERT INTO lokasi (latitude, longitude, id_akun)
            VALUES (%s, %s, %s);
        """, (latitude, longitude, id_akun))

        conn.commit()
        print("Registrasi berhasil!")
        inputan_kembali = input("Tekan Enter untuk kembali ke menu utama...")

    except psycopg2.IntegrityError:
        conn.rollback()
        inputan_kembali = input("Registrasi gagal: Nomor HP sudah digunakan atau data tidak valid.")
    except Exception as e:
        conn.rollback()
        inputan_kembali = input("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
        
def login(no_hp, password):
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_akun, nama, status_akun FROM akun
            WHERE no_hp = %s AND password = %s;
        """, (no_hp, password))
        user = cur.fetchone()
        id_akun= user[0]
        nama= user[1]
        status = user[2]

        if user:
            if status == "0":
                menu_owner(nama)
            else : 
                menu_pembeli(id_akun,nama)
            clear_terminal()
        else:
            print("Login gagal: Nomor HP atau password salah.")
            kembali()

    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
    finally:
        cur.close()
        conn.close()

def menu_owner(nama):
    while True :
        clear_terminal()
        print(f"halo {nama} selamat datang di aplikasi petani")
        print("=========================menu utama=========================")
        print("1. penjualan hasil tani")
        print("2. Rute pengiriman ")
        print("3.pencatatan transaksi")
        print("4. pengelolaan stock")
        print("5. Keluar")
        pilihan = input("Masukkan pilihan anda: ")
        if pilihan == "1":
            penjualan_hasil_tani()
        elif pilihan == "2":
            rute_pengiriman()
        elif pilihan == "3":
            pencatatan_transaksi()
        elif pilihan == "4":
            pengelolaan_stock()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi ini.")
            clear_terminal()
            break
        else:
            print("Pilihan tidak valid.")
        
def menu_pembeli(id_akun, nama):
    while True :
        clear_terminal()
        print(f"halo {nama} selamat datang di aplikasi petani")
        print("=========================menu utama=========================")
        print("1. Beli Hasil Tani")
        print("2. Keluar")
        pilihan = input("Masukkan pilihan anda: ")
        if pilihan == "1":
            beli_hasil_tani(id_akun)
        elif pilihan == "2":
            print("Terima kasih telah menggunakan aplikasi ini.")
            clear_terminal()
            break
        else:
            print("Pilihan tidak valid.")

def beli_hasil_tani (id_akun):
    print("Menu Beli Hasil Tani")
    nama_sayur = input("Masukkan nama sayur: ").strip()
    jumlah_beli = int(input("Masukkan jumlah beli: "))
    
    conn = connect_db()
    cur = conn.cursor()
    query = f"""
        SELECT id_sayur, harga_satuan
        FROM sayur
        WHERE nama_sayur ilike '{nama_sayur}'
    """
    cur.execute(query)

    data_sayur = cur.fetchone()

    if data_sayur is None:
        input("❌ Sayur tidak ditemukan dalam database.")
    else:
        id_sayur, harga_satuan = data_sayur
        total_harga = harga_satuan * jumlah_beli
        status = 'P'

        insert_query = f"""
            INSERT INTO request_pembelian (id_akun, id_sayur, nama_sayur, jumlah_beli, total_harga, status)
            VALUES ({id_akun}, {id_sayur}, '{nama_sayur}', {jumlah_beli}, {total_harga}, '{status}')
        """
        cur.execute(insert_query)
        conn.commit()
        input("✅ Request pembelian berhasil disimpan!")

    # max_budget = int(input("Masukkan budget maksimal: "))

 
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
    
    
main()
