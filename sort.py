import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="Algo2",
    user="postgres",
    password="syadid1306",
    port=5432)
cur = conn.cursor()

def selection_sort_by_stok(data, ascending=True):
    n = len(data)
    for i in range(n):
        idx_extreme = i
        for j in range(i + 1, n):
            if ascending:
                if data[j][2] < data[idx_extreme][2]:  
                    idx_extreme = j
            else:
                if data[j][2] > data[idx_extreme][2]:
                    idx_extreme = j
        data[i], data[idx_extreme] = data[idx_extreme], data[i]
    return data

def selection_sort_by_nama(data, ascending=True):
    n = len(data)
    for i in range(n):
        idx_extreme = i
        for j in range(i + 1, n):
            nama_j = data[j][1].lower()
            nama_extreme = data[idx_extreme][1].lower()
            if ascending:
                if nama_j < nama_extreme:
                    idx_extreme = j
            else:
                if nama_j > nama_extreme:
                    idx_extreme = j
        data[i], data[idx_extreme] = data[idx_extreme], data[i]
    return data

def ambil_semua_data():
    cur.execute("SELECT * FROM sayur") 
    return cur.fetchall()

def tampilkan_data(data):
    print("\nData Sayur:")
    for row in data:
        print(f"ID: {row[0]}, Nama: {row[1]}, Stok: {row[2]}, Harga: {row[3]}")

def menu():
    while True:
        print("\n==== Menu Pengelolaan Stok Sayur ====")
        print("1. Tampilkan sayur dengan stok paling sedikit (Selection Sort)")
        print("2. Tampilkan sayur urut nama (A-Z) (Selection Sort)")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == '1':
            data = ambil_semua_data()
            data_sorted = selection_sort_by_stok(data, ascending=True)
            tampilkan_data(data_sorted)
        elif pilihan == '2':
            data = ambil_semua_data()
            data_sorted = selection_sort_by_nama(data, ascending=True)
            tampilkan_data(data_sorted)
        elif pilihan == '3':
            break
        else:
            print("Pilihan tidak valid.")

# menu()

# cur.close()
# conn.close()
