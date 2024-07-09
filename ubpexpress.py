import csv
import os
import random
from datetime import datetime

FILE_NAME = 'transaksi_ubp_express.csv'
FIELDNAMES = ['nomor_resi', 'nama_pengirim', 'nama_penerima', 'alamat_penerima', 'nomor_hp_penerima', 'deskripsi_paket', 'berat_paket', 'biaya_pengiriman', 'tanggal_transaksi']

TARIF_PER_KM = 200
TARIF_PER_KG = 5000

def buat_file_jika_tidak_ada():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def generate_unique_id():
    existing_ids = set()
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                existing_ids.add(int(row['nomor_resi']))
    
    while True:
        new_id = random.randint(100000, 999999)
        if new_id not in existing_ids:
            return new_id

def hitung_biaya_pengiriman(jarak, berat):
    return int((TARIF_PER_KM * jarak) + (TARIF_PER_KG * berat))

def tambah_transaksi():
    nomor_resi = generate_unique_id()
    nama_pengirim = input("Nama Pengirim         : ")
    nama_penerima = input("Nama Penerima         : ")
    alamat_penerima = input("Alamat Penerima       : ")
    nomor_hp_penerima = int(input("Nomor HP Penerima     : "))
    deskripsi_paket = input("Deskripsi Paket       : ")
    berat_paket = float(input("Berat Paket (kg)      : "))
    jarak_pengiriman = float(input("Jarak Pengiriman (km) : "))
    biaya_pengiriman = hitung_biaya_pengiriman(jarak_pengiriman, berat_paket)
    tanggal_transaksi = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow({
            'nomor_resi': nomor_resi,
            'nama_pengirim': nama_pengirim,
            'nama_penerima': nama_penerima,
            'alamat_penerima': alamat_penerima,
            'nomor_hp_penerima': nomor_hp_penerima,
            'deskripsi_paket': deskripsi_paket,
            'berat_paket': berat_paket,
            'biaya_pengiriman': biaya_pengiriman,
            'tanggal_transaksi': tanggal_transaksi
        })
    print(f"Transaksi berhasil ditambahkan dengan Nomor Resi (ID): {nomor_resi} & Biaya Pengiriman: Rp{biaya_pengiriman}")

def ubah_transaksi():
    nomor_resi = input("Masukkan Nomor Resi (ID) dari transaksi yang akan diubah: ")
    transaksi_ditemukan = False
    transaksi_baru = []

    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['nomor_resi'] == nomor_resi:
                transaksi_ditemukan = True
                print("Masukkan data baru (kosongkan jika tidak ingin mengubah):")
                nama_pengirim = input(f"Nama Pengirim ({row['nama_pengirim']}): ") or row['nama_pengirim']
                nama_penerima = input(f"Nama Penerima ({row['nama_penerima']}): ") or row['nama_penerima']
                alamat_penerima = input(f"Alamat Penerima ({row['alamat_penerima']}): ") or row['alamat_penerima']
                nomor_hp_penerima = input(f"Nomor HP Penerima ({row['nomor_hp_penerima']}): ") or row['nomor_hp_penerima']
                deskripsi_paket = input(f"Deskripsi Paket ({row['deskripsi_paket']}): ") or row['deskripsi_paket']
                berat_paket = input(f"Berat Paket ({row['berat_paket']}): ") or row['berat_paket']
                biaya_pengiriman = input(f"Biaya Pengiriman ({row['biaya_pengiriman']}): ") or row['biaya_pengiriman']
                tanggal_transaksi = input(f"Tanggal Transaksi ({row['tanggal_transaksi']}): ") or row['tanggal_transaksi']
                row = {
                    'nomor_resi': nomor_resi,
                    'nama_pengirim': nama_pengirim,
                    'nama_penerima': nama_penerima,
                    'alamat_penerima': alamat_penerima,
                    'nomor_hp_penerima': nomor_hp_penerima,
                    'deskripsi_paket': deskripsi_paket,
                    'berat_paket': berat_paket,
                    'biaya_pengiriman': biaya_pengiriman,
                    'tanggal_transaksi': tanggal_transaksi
                }
            transaksi_baru.append(row)

    if transaksi_ditemukan:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(transaksi_baru)
        print("Transaksi berhasil diubah.")
    else:
        print("Transaksi tidak ditemukan.")

def hapus_transaksi():
    nomor_resi = input("Masukkan Nomor Resi (ID) dari transaksi yang akan dihapus: ")
    transaksi_ditemukan = False
    transaksi_baru = []

    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['nomor_resi'] == nomor_resi:
                transaksi_ditemukan = True
            else:
                transaksi_baru.append(row)

    if transaksi_ditemukan:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(transaksi_baru)
        print("Transaksi berhasil dihapus.")
    else:
        print("Transaksi tidak ditemukan.")

def lihat_transaksi():
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print("-" * 40)
            print(f"Nomor Resi          : {row['nomor_resi']}")
            print(f"Nama Pengirim       : {row['nama_pengirim']}")
            print(f"Nama Penerima       : {row['nama_penerima']}")
            print(f"Alamat Penerima     : {row['alamat_penerima']}")
            print(f"Nomor HP Penerima   : {row['nomor_hp_penerima']}")
            print(f"Deskripsi Paket     : {row['deskripsi_paket']}")
            print(f"Berat Paket         : {row['berat_paket']} kg")
            print(f"Biaya Pengiriman    : Rp{int(row['biaya_pengiriman'])}")
            print(f"Tanggal Transaksi   : {row['tanggal_transaksi']}")

def menu():
    buat_file_jika_tidak_ada()
    while True:
        print("\n========== UBP Express ==========")
        print("[1] Tambah Transaksi Pengiriman")
        print("[2] Ubah Transaksi Pengiriman")
        print("[3] Hapus Transaksi Pengiriman")
        print("[4] Lihat Transaksi Pengiriman")
        print("[5] Keluar")
        pilihan = input("Pilih menu (1-5): ")
        
        if pilihan == '1':
            tambah_transaksi()
        elif pilihan == '2':
            ubah_transaksi()
        elif pilihan == '3':
            hapus_transaksi()
        elif pilihan == '4':
            lihat_transaksi()
        elif pilihan == '5':
            print("Terima kasih telah menggunakan UBP Express.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")
            continue

        while True:
            kembali = input("Kembali ke menu awal? (y/n): ").lower()
            if kembali == 'y':
                break
            elif kembali == 'n':
                print("Terima kasih telah menggunakan UBP Express.")
                return
            else:
                print("Pilihan tidak valid, silakan masukkan 'y' atau 'n'.")

if __name__ == "__main__":
    menu()
