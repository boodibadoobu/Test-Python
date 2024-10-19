import pandas as pd
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import webbrowser

path = 'D:\\Data Akang\\Telkom University\\Matkul\\Praktikum Pemrograman\\Tugas Besar Semester 2\\Data Negara - Negara Ekspor dan Impor beras Indonesia - Original.csv'
try:
    df = pd.read_csv(path)
except FileNotFoundError:
    print(f"File not found: {path}")
    df = pd.DataFrame(columns=['No', 'Ekspor/Impor', 'Negara', 'Tahun', 'Kuartal', 'Total Beras (Ton)'])

def syarat_input (pesan, validasi_opsi = None, opsi_valid = str, batasKarakter = None ) :
    while True :
        data = input (pesan)
        if not data :
            print("Data tidak boleh kosong")
            continue
        if opsi_valid == str :
            if not all(char.isalpha() or char.isspace() for char in data):
                print("Tidak ada negara dengan angka")
                continue
            if validasi_opsi and data.capitalize () not in validasi_opsi:
                print(f"Pilihan tidak valid, Pilih salah satu dari: {', '.join(validasi_opsi)}")
            if data.capitalize() == 'Indonesia' :
                print ('Ini adalah tabel Ekspor Impor untuk Indonesia')
                continue
            return data.capitalize()
        elif opsi_valid == int:
            if not data.isdigit():
                print("Input harus angka, coba lagi")
                continue
            if batasKarakter and len(data) > batasKarakter:
                print(f"Terlalu banyak, batas adalah {batasKarakter} digit. Silakan coba lagi")
                continue
            data = int(data)
            if validasi_opsi and data not in validasi_opsi:
                print(f"Pilihan tidak valid, Pilih salah satu dari: {', '.join(map(str, validasi_opsi))}")
                continue
            return data

def tambah_data () :
    global df
    jenis = syarat_input ('Masukkan Jenis (Ekspor/Impor) : ', validasi_opsi = ['Ekspor', 'Impor'])
    negara = syarat_input ('Masukkan Nama Negara : ', opsi_valid = str, batasKarakter=40)
    tahun = syarat_input ('Masukkan Tahun : ', opsi_valid = int, batasKarakter=4)
    kuartal = syarat_input ('Masukkan Kuartal (1, 2, 3, 4) : ', validasi_opsi = [1, 2, 3, 4], opsi_valid=int)
    total_beras = syarat_input ('Masukkan total beras (Ton): ', opsi_valid = int)
    
    if not df.empty and 'No' in df.columns:
        next_number = df['No'].max() + 1
    else:
        next_number = 1
    if not df[(df['Negara'] == negara) & (df['Tahun'] == tahun) & (df['Kuartal'] == kuartal)].empty:
        print(f"Data untuk {negara} tahun {tahun} kuartal {kuartal} sudah ada")
    
    dataBaru = pd.DataFrame ({'No': [next_number], 'Ekspor/Impor' : [jenis], 'Negara': [negara], 'Tahun': [tahun], 'Kuartal': [kuartal], 'Total Beras (Ton)': [total_beras]})
    df = pd.concat([df, dataBaru], ignore_index=True)
    
    df.sort_values(by=['Ekspor/Impor', 'No', 'Tahun', 'Negara'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    
    df['No'] = range(1, len(df) + 1)
    
    df.to_csv(path, index=False)

    print("Data telah dimasukkan kedalam CSV")
    
def edit_data () :
    global df
    table = PrettyTable()
    for col in df.columns:
        table.add_column(col, df[col])
    print(table)
    
    try:
        indeks = int(input("Masukkan indeks data yang ingin diedit : "))
        if indeks < 1 or indeks > len(df):
            print(indeks, 'Tidak ada dalam Tabel')
            return
        
        total_beras = df.at[indeks-1, 'Total Beras (Ton)']
        total_beras_input = input(f"Total Beras saat ini: {total_beras}\nMasukkan total beras baru (Ton) atau biarkan kosong jika tidak ingin mengubah: ")
        if total_beras_input.strip():
            total_beras = syarat_input('Masukkan total beras baru (Ton): ', opsi_valid=int)
        elif total_beras_input != df.at[indeks-1, 'Total Beras (Ton)']:
            jenis = syarat_input ('Masukkan Jenis (Ekspor/Impor) : ', validasi_opsi = ['Ekspor', 'Impor'])
            negara = syarat_input ('Masukkan Nama Negara : ', opsi_valid = str, batasKarakter=40)
            tahun = syarat_input ('Masukkan Tahun : ', opsi_valid = int, batasKarakter=4)
            kuartal = syarat_input ('Masukkan Kuartal (1, 2, 3, 4) : ', validasi_opsi = [1, 2, 3, 4], opsi_valid=int)
            total_beras = syarat_input ('Masukkan total beras (Ton): ', opsi_valid = int)
                
            if not df[(df['Negara'] == negara) & (df['Tahun'] == tahun) & (df['Kuartal'] == kuartal)].empty:
                print(f"Data untuk {negara} tahun {tahun} kuartal {kuartal} sudah ada, data gagal diubah")
                return
            
            df.at[indeks-1, 'Ekspor/Impor'] = jenis
            df.at[indeks-1, 'Negara'] = negara
            df.at[indeks-1, 'Tahun'] = tahun
            df.at[indeks-1, 'Kuartal'] = kuartal
        else:
            total_beras_input = total_beras
        df.at[indeks-1, 'Total Beras (Ton)'] = total_beras
        
        data_sebelum = df.iloc[indeks-1].copy()
        
        df.to_csv(path, index=False)
        
        
        print("Data sebelum diubah:")
        print(data_sebelum)
        print("\nData telah diperbarui:")
        print(df.iloc[indeks-1])
        
    except ValueError:
        print("Input harus berupa angka")
        
def hapus_data () :
    global df
    table = PrettyTable()
    for col in df.columns:
        table.add_column(col, df[col])
    print(table)
          
    try:
        indeks = int(input("Masukkan indeks data yang ingin dihapus: "))
        if indeks < 1 or indeks > len(df):
            print(indeks, 'Tidak ada dalam Tabel')
            return
        df.drop(index=indeks-1, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df['No'] = range(1, len(df) + 1)
        df.to_csv(path, index=False)
        print("Data telah dihapus dari CSV")
        
    except ValueError:
        print("Input harus berupa angka")

def tampilkan_tabel() :
    table = PrettyTable()
    for col in df.columns:
        table.add_column(col, df[col])
    print(table)

def tampilkan_grafik_bar_negara(jenis_data, negara) :
    if jenis_data.lower() not in ['ekspor', 'impor']:
        print("Jenis data harus 'Ekspor' atau 'Impor'")
        return
    
    if negara not in df['Negara'].values:
        print("Negara tidak ada, coba lagi yang lain")
        return
    
    filter_data = df[(df['Ekspor/Impor'] == jenis_data) & (df['Negara'] == negara)]
    filter_data.plot(kind='bar', x='Tahun', y='Total Beras (Ton)')
    plt.title(f'Grafik {jenis_data} {negara}')
    plt.xlabel('Tahun')
    plt.ylabel('Total Beras (Ton)')
    plt.show()

def plot_ekspor_impor(df) :
    # Mengubah kolom Tahun menjadi tipe data string
    df['Tahun'] = df['Tahun'].astype(str)

    # Mengelompokkan data berdasarkan 'Ekspor/Impor', 'Tahun', dan 'Negara' untuk mendapatkan total ton ekspor dan impor per tahun per negara
    grouped = df.groupby(['Ekspor/Impor', 'Tahun', 'Negara'])['Total Beras (Ton)'].sum().reset_index()

    # Mengambil data ekspor dan impor
    ekspor = grouped[grouped['Ekspor/Impor'] == 'Ekspor']
    impor = grouped[grouped['Ekspor/Impor'] == 'Impor']

    # Mengelompokkan data ekspor dan impor berdasarkan 'Tahun' untuk mendapatkan total ton ekspor dan impor per tahun
    total_ekspor_per_tahun = ekspor.groupby('Tahun')['Total Beras (Ton)'].sum()
    total_impor_per_tahun = impor.groupby('Tahun')['Total Beras (Ton)'].sum()

    # Plotting data total ton ekspor dan impor per tahun
    plt.figure(figsize=(12, 6))
    plt.plot(total_ekspor_per_tahun.index, total_ekspor_per_tahun.values, marker='o', color='blue', label='Ekspor')
    plt.plot(total_impor_per_tahun.index, total_impor_per_tahun.values, marker='o', color='yellow', label='Impor')
    plt.title('Total Ekspor dan Impor Beras per Tahun')
    plt.xlabel('Tahun')
    plt.ylabel('Total Beras (Ton)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def search_data():
    global df  # Declare df as global to use it within this function
    while True:
        print("\nMenu Pencarian:")
        print("1. Negara dengan Ekspor/Impor tertinggi")
        print("2. Negara dengan Ekspor/Impor terendah")
        print("3. Mencari nama negara")
        print("4. Mencari berdasarkan tahun")
        print("5. Mencari berdasarkan kuartal")
        print("6. Mencari berdasarkan berat")
        print("7. Kembali ke menu utama")

        choice = input("Pilih opsi (1/2/3/4/5/6/7): ")
        if choice == '1':
            highest_export = df[df['Ekspor/Impor'] == 'Ekspor'].nlargest(1, 'Total Beras (Ton)')
            highest_import = df[df['Ekspor/Impor'] == 'Impor'].nlargest(1, 'Total Beras (Ton)')
            print("\nNegara dengan Ekspor Tertinggi:")
            print(highest_export[['Negara', 'Total Beras (Ton)']].to_string(index=False))
            print("\nNegara dengan Impor Tertinggi:")
            print(highest_import[['Negara', 'Total Beras (Ton)']].to_string(index=False))
        elif choice == '2':
            lowest_export = df[df['Ekspor/Impor'] == 'Ekspor'].nsmallest(1, 'Total Beras (Ton)')
            lowest_import = df[df['Ekspor/Impor'] == 'Impor'].nsmallest(1, 'Total Beras (Ton)')
            print("\nNegara dengan Ekspor Terendah:")
            print(lowest_export[['Negara', 'Total Beras (Ton)']].to_string(index=False))
            print("\nNegara dengan Impor Terendah:")
            print(lowest_import[['Negara', 'Total Beras (Ton)']].to_string(index=False))
        elif choice == '3':
            negara = syarat_input("Masukkan nama negara yang ingin dicari: ")
            kategori = syarat_input("Masukkan kategori (Ekspor/Impor): ", valid_options=["Ekspor", "Impor"])
            filtered_df = df[(df['Negara'] == negara) & (df['Ekspor/Impor'] == kategori)].sort_values(by=['Tahun', 'Kuartal'])

            if not filtered_df.empty:
                print(filtered_df.to_string(index=False))
            else:
                print("Negara tidak ditemukan. Membuka link...")
                webbrowser.open('https://www.youtube.com/watch?v=b3rNUhDqciM')
        elif choice == '4':
            tahun = syarat_input("Masukkan tahun yang ingin dicari: ", validation_type=int, length_limit=4)
            filtered_df = df[df['Tahun'] == tahun].sort_values(by=['Ekspor/Impor', 'Kuartal', 'Total Beras (Ton)'])

            if not filtered_df.empty:
                print(filtered_df.to_string(index=False))
            else:
                print("Data tidak ditemukan untuk tahun tersebut.")
        elif choice == '5':
            kuartal = syarat_input("Masukkan kuartal yang ingin dicari (1, 2, 3, 4): ", valid_options=[1, 2, 3, 4], validation_type=int)
            filtered_df = df[df['Kuartal'] == kuartal].sort_values(by=['Ekspor/Impor', 'Tahun', 'Total Beras (Ton)'])

            if not filtered_df.empty:
                print(filtered_df.to_string(index=False))
            else:
                print("Data tidak ditemukan untuk kuartal tersebut.")
        elif choice == '6':
            berat = syarat_input("Masukkan berat yang ingin dicari (Ton): ", validation_type=int)
            filtered_df = df[df['Total Beras (Ton)'] == berat].sort_values(by=['Ekspor/Impor', 'Tahun', 'Kuartal'])

            if not filtered_df.empty:
                print(filtered_df.to_string(index=False))
            else:
                print("Data tidak ditemukan untuk berat tersebut.")
        elif choice == '7':
            break
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

def tampilkan_tipe_grafik() :
    while True:
        try:
            print ('1. Grafik garis (Perbandingan antara Ekspor dan Impor)')
            print ('2. Grafik Batang (Melihat Ekspor/Impor suatu negara)')
            print ('3. Diagram pie (Melihat kontribusi semua negara dalam Ekspor/Impor)')
            milihGrafik = int(input("Pilih grafik yang diinginkan : "))
            if milihGrafik == 1:
                plot_ekspor_impor (df)
                break
            elif milihGrafik == 2:
                jenis_data = input('Masukkan jenis (Ekspor/Impor) : ')
                negara = input("Masukkan nama negara : ")
                tampilkan_grafik_bar_negara(jenis_data, negara)
                break
            elif milihGrafik == 3:
                jenis_data = input('Masukkan jenis (Ekspor/Impor) : ')
                negara = input("Masukkan nama negara : ")
                tampilkan_grafik_bar_negara(jenis_data, negara)
                break
            else:
                print("Gaada")
        except ValueError:
            print("Angka ya pls.")

def statika():
    global df

    # Mengubah kolom Tahun menjadi tipe data string
    df['Tahun'] = df['Tahun'].astype(str)

    # Mengelompokkan data berdasarkan 'Ekspor/Impor' dan 'Tahun' untuk mendapatkan total ton ekspor dan impor per tahun
    grouped = df.groupby(['Ekspor/Impor', 'Tahun'])['Total Beras (Ton)']

    # Menghitung mean, median, dan sum untuk setiap grup (Ekspor dan Impor per Tahun)
    stats = grouped.agg(['mean', 'median', 'sum']).reset_index()

    # Memisahkan data ekspor dan impor
    ekspor_stats = stats[stats['Ekspor/Impor'] == 'Ekspor']
    impor_stats = stats[stats['Ekspor/Impor'] == 'Impor']

    # Menampilkan hasil statistik per tahun
    print("\nStatistik Ekspor per Tahun:")
    print(ekspor_stats.to_string(index=False))

    print("\nStatistik Impor per Tahun:")
    print(impor_stats.to_string(index=False))

    # Menghitung statistik untuk semua tahun
    total_stats = df.groupby('Ekspor/Impor')['Total Beras (Ton)'].agg(['mean', 'median', 'sum']).reset_index()

    # Menampilkan hasil statistik untuk semua tahun
    print("\nStatistik Total untuk Semua Tahun:")
    print(total_stats.to_string(index=False))

def menu_utama() :
    while True:
        print("\nMenu:")
        print("1. Tambah Data")
        print("2. Edit Data")
        print("3. Hapus Data")
        print("4. Tampilkan data (Tabel)")
        print("5. Tampilkan data (Grafik)")
        print("6. Pencarian data")
        print("7. Tampilkan Statistik")
        print("8. Keluar")
        
        try:
            pilihan = int(input("Masukkan menu yang diinginkan (angka) : "))
            
            if pilihan == 1:
                tambah_data()
            elif pilihan == 2:
                edit_data()
            elif pilihan == 3:
                hapus_data()
            elif pilihan == 4:
                print("\nTabel CSV Ekspor Impor Indonesia\n")
                tampilkan_tabel()
            elif pilihan == 5:
                tampilkan_tipe_grafik()
            elif pilihan == 6:
                search_data()
            elif pilihan == 7:
                statika()
            elif pilihan == 8:
                exit()
            else:
                print('Gaada Menunya')
                
        except ValueError:
            print('Gaada')

menu_utama()
