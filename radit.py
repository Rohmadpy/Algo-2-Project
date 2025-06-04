import psycopg2
from datetime import date

DB = psycopg2.connect(
    host='localhost',
    database='DBAlgo2',
    user='postgres',
    password='@Raditya14'
)
curs = DB.cursor()

curs.execute("SELECT id_akun FROM akun WHERE status_akun = '0' LIMIT 1")
akun_data = curs.fetchone()

if akun_data is None:
    print("❌ Tidak ada akun dengan status_akun = 0")
    DB.close()
    exit()

id_akun = akun_data[0]

print(f"✅ ID akun otomatis terisi: {id_akun}")

#########################
nama_sayur = input("Masukkan nama sayur: ").strip()
jumlah_beli = int(input("Masukkan jumlah beli: "))

query = f"""
    SELECT id_sayur, harga_satuan
    FROM sayur
    WHERE nama_sayur = '{nama_sayur}'
"""
curs.execute(query)

data_sayur = curs.fetchone()

if data_sayur is None:
    print("❌ Sayur tidak ditemukan dalam database.")
else:
    id_sayur, harga_satuan = data_sayur
    total_harga = harga_satuan * jumlah_beli
    status = 'P'

    insert_query = f"""
        INSERT INTO request_pembelian (id_akun, id_sayur, nama_sayur, jumlah_beli, total_harga, status)
        VALUES ({id_akun}, {id_sayur}, '{nama_sayur}', {jumlah_beli}, {total_harga}, '{status}')
    """
    curs.execute(insert_query)
    DB.commit()
    print("✅ Request pembelian berhasil disimpan!")

max_budget = int(input("Masukkan budget maksimal: "))

curs.execute("""
    SELECT rp.id_request, rp.id_sayur, rp.jumlah_beli, rp.total_harga, s.stok
    FROM request_pembelian rp
    JOIN sayur s ON rp.id_sayur = s.id_sayur
    WHERE rp.status = 'P'
""")
requests = curs.fetchall()

if not requests:
    print("Tidak ada request dengan status 'P'")
    exit()

values, weights, stok_list, id_list, sayur_ids = [], [], [], [], []

for row in requests:
    id_req, id_sayur, jumlah, total, stok = row
    values.append(jumlah)
    weights.append(total)
    stok_list.append(stok)
    id_list.append(id_req)
    sayur_ids.append(id_sayur)

def knapsack(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w])
            else:
                dp[i][w] = dp[i - 1][w]
    w = capacity
    picked = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            picked.append(i - 1)
            w -= weights[i - 1]
    return picked

picked_indices = knapsack(values, weights, max_budget)

if not picked_indices:
    print("Tidak ada request yang cocok dengan budget.")
    exit()

for i in picked_indices:
    id_request = id_list[i]
    id_sayur = sayur_ids[i]
    jumlah_beli = values[i]
    total_harga = weights[i]
    stok_tersedia = stok_list[i]

    if stok_tersedia < jumlah_beli:
        print(f"Stok tidak cukup untuk request ID {id_request}. Melewati...")
        continue

    try:
        update_stok_query = f"""
            UPDATE sayur
            SET stok = stok - {jumlah_beli}
            WHERE id_sayur = {id_sayur}
        """
        curs.execute(update_stok_query)

        insert_transaksi = f"""
            INSERT INTO transaksi (id_request, tanggal)
            VALUES ({id_request}, '{date.today()}')
        """
        curs.execute(insert_transaksi)

        update_status = f"""
            UPDATE request_pembelian
            SET status = 'S'
            WHERE id_request = {id_request}
        """
        curs.execute(update_status)

        print(f"✅ Transaksi berhasil untuk request ID {id_request}.")

    except Exception as e:
        DB.rollback()
        print(f"❌ Gagal memproses request ID {id_request}: {e}")

DB.commit()
curs.close()
DB.close()
print("✅ Semua transaksi yang sesuai Knapsack telah diproses.")