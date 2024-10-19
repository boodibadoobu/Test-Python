import datetime

def masuk_parkir(daftar_masuk):
    plat_nomor = input('Masukkan Plat Nomor Kendaraan Anda: ')
    
    for kendaraan in daftar_masuk:
        if plat_nomor == kendaraan[0]:
            print('Maaf, kendaraan dengan plat nomor tersebut sudah masuk parkir.')
            return None

    masuk = (plat_nomor, datetime.datetime.now())
    print('Anda masuk pukul', masuk[1].strftime('%H:%M:%S'))
    return masuk

def keluar_parkir(daftar_masuk):
    plat_nomor = input('Masukkan Plat Nomor Kendaraan Anda: ')
    for idx, kendaraan in enumerate(daftar_masuk):
        if plat_nomor == kendaraan[0]:
            waktu_masuk = kendaraan[1]
            keluar = datetime.datetime.now()
            
            def hitung_biaya_parkir(waktu):
                detik = waktu.total_seconds()
                if detik <= 60:
                    return 10000
                elif detik <= 120:
                    return 10000
                elif detik <= 180:
                    return 20000
                elif detik <= 240:
                    return 30000
                elif detik <= 360:
                    print("Anda terkena denda 10%")
                    return (30000 * 0.1) + 30000
                elif detik > 360:
                    print("Anda terkena denda 25%")
                    return (30000 * 0.25) + 30000

            waktu_parkir = keluar - waktu_masuk
            biaya_parkir = hitung_biaya_parkir(waktu_parkir)
            total_biaya = biaya_parkir
            daftar_masuk[idx] = (plat_nomor, waktu_masuk, keluar, total_biaya)

            print(f"Biaya Parkir: Rp. {biaya_parkir}")
            print(f"Total yang harus dibayar: Rp. {total_biaya}")

            while True:
                try:
                    bayar = float(input("Masukkan Nominal pembayaran anda : "))
                    if bayar >= total_biaya:
                        kembali = bayar - total_biaya
                        print(f'Kembalian anda : Rp {kembali}')
                        print("Silahkan keluar")
                        break
                    else:
                        print(f"Masukkan uang yang sesuai dengan tarif yang ditentukan !!!")
                except ValueError:
                    print("Masukkan angka yang valid.")

            return kendaraan
    print('Plat Kendaraan tidak ada')

def cetak_semua_transaksi(daftar_masuk):
    print("\nDaftar Seluruh Transaksi:")
    for transaksi in daftar_masuk:
        plat_nomor = transaksi[0]
        waktu_masuk = transaksi[1].strftime('%H:%M:%S')
        waktu_keluar = transaksi[2].strftime('%H:%M:%S') if len(transaksi) > 2 else "Belum Keluar"
        total_biaya = transaksi[3] if len(transaksi) > 3 else "Belum Dihitung"

        print(f"Plat Nomor: {plat_nomor}, Waktu Masuk: {waktu_masuk}, Waktu Keluar: {waktu_keluar}, Total Biaya: Rp {total_biaya}")

def cetak_kendaraan_belum_keluar(daftar_masuk):
    belum_keluar = [kendaraan for kendaraan in daftar_masuk if len(kendaraan) <= 2]

    if belum_keluar:
        print("\nDaftar Kendaraan Belum Keluar:")
        for kendaraan in belum_keluar:
            print(f"Plat Nomor: {kendaraan[0]}")
    else:
        print("Semua kendaraan telah keluar.")

def admin_parkir(daftar_masuk):
    attempts = 0
    while attempts < 3:
        pin = input('Masukkan PIN: ')
        if pin != '123456':
            print("Maaf, PIN yang Anda masukkan salah.")
            attempts += 1
        else:
            while True:
                print("\nMenu Admin Parkir:")
                print("1. Cetak Seluruh Transaksi")
                print("2. Kendaraan Belum Keluar")
                print("3. Kembali ke Menu Utama")
                opsi = input("Pilih menu (1/2/3): ")

                if opsi in ("1", "2", "3"):
                    if opsi == "1":
                        cetak_semua_transaksi(daftar_masuk)
                    elif opsi == "2":
                        cetak_kendaraan_belum_keluar(daftar_masuk)
                    else:
                        break
                else:
                    print("Pilihan tidak valid. Silakan coba lagi.")
            break
    else:
        print("Anda telah mencapai batas percobaan PIN. Aplikasi akan keluar.")

def aplikasi_parkir():
    daftar_masuk = []
    kapasitas_parkir = 10

    while True:
        print('\n======== Menu Utama ========')
        print('1. Masuk Parkir')
        print('2. Keluar Parkir')
        print('3. Admin Parkir')
        print('4. Keluar dari aplikasi')
        pilihan = input('Pilih menu: ')

        if pilihan == '1':
            if len(daftar_masuk) < kapasitas_parkir:
                masuk_data = masuk_parkir(daftar_masuk)
                if masuk_data:
                    daftar_masuk.append(masuk_data)
            else:
                print("Maaf, kapasitas parkir telah mencapai batas maksimal.")
        elif pilihan == '2':
            keluar_parkir(daftar_masuk)
        elif pilihan == '3':
            admin_parkir(daftar_masuk)
        elif pilihan == '4':
            print("Terima kasih telah menggunakan layanan kami :)")
            break
        else:
            print('Pilihan tidak valid')

aplikasi_parkir()

#Fixed Folder name