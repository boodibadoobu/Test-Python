def pertambahan (angka1, angka2):
    return angka1 + angka2

def pengurangan (angka1, angka2):
    return angka1 - angka2   

def perkalian (angka1, angka2):
    return angka1 * angka2

def pembagian (angka1, angka2):
    if angka2 == 0:
        return "Tidak bisa dibagi dengan 0"
    else:
        return angka1 / angka2
        
def menu ():
    while True:
        print ("======== Kalkulator dua angka ========")
        print ("1. Pertambahan")
        print ("2. Pengurangan")
        print ("3. Perkalian")
        print ("4. Pembagian")
        print ("5. Keluar")
        pilihan = (input ("Masukkan Menu yang anda inginkan : "))
        
        if pilihan in ['1', '2', '3', '4']:
            angka1 = int(input("Masukkan angka pertama: "))
            angka2 = int(input("Masukkan angka kedua: "))
        
        if pilihan == '1' :
            hasil = pertambahan (angka1, angka2)
            print (f"Hasil = {hasil}")
        elif pilihan == '2' :
            hasil = pengurangan (angka1, angka2)
            print (f"Hasil = {hasil}")
        elif pilihan == '3' :
            hasil = perkalian (angka1, angka2)
            print (f"Hasil = {hasil}")
        elif pilihan == '4' :
            hasil = pembagian (angka1, angka2)
            print (f"Hasil = {hasil}")
        elif pilihan == '5' : 
            exit()
        else:
            print("Menu tidak ada, silahkan pilih yang tertera")
            
menu()

#Push test