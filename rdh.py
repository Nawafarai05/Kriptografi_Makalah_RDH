import argparse
import sys
import numpy as np
from PIL import Image
import math
import matplotlib.pyplot as plt

# menghitung nilai PSNR antara gambar original dan hasil steganografi
def calculate_psnr(original, stego) :
    mse = np.mean((original - stego) ** 2)
    if mse == 0 : return float('inf')
    max_pixel = 255.0
    psnr = 10 * math.log10((max_pixel ** 2) / mse)
    return psnr

# konversi teks input menjadi kode biner
def text_to_bin(char) :
    return ''.join(format(ord(c), '08b') for c in char)

# konversi teks dalam kode biner menjadi karakter readable
def bin_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars if int(c, 2) != 0)

# membuat grafik historgram dan citra rekam medis
def generate_histogram(image_path, output_path):
    print(f"=== Membaca citra untuk histogram: {image_path} ===")
    img = Image.open(image_path).convert('L')
    data = np.array(img)
    hist, bins = np.histogram(data.flatten(), bins = 256, range=[0, 256])
    
    # abaikan area hitam pekat agar peak berada di area medis
    hist[0] = 0
    
    peak_point = np.argmax(hist)
    zero_point = np.argmin(hist)

    # membuat citra grafik
    plt.figure(figsize= (8, 5))
    plt.bar(range(256), hist, color = 'gray', alpha = 0.7, label = 'Frekuensi Pixel')
    plt.axvline(peak_point, color = 'red', linestyle = 'dashed', linewidth = 2, label = f'Peak Point ({peak_point})')
    plt.axvline(zero_point, color = 'blue', linestyle = 'dashed', linewidth = 2, label = f'Zero Point ({zero_point})')
    plt.title(f'Histogram Analisis Citra Medis', fontsize = 14)
    plt.xlabel('Intensitas Pixel (Grayscale)', fontsize = 12)
    plt.ylabel('Frekuensi', fontsize = 12)
    plt.legend()
    plt.grid(axis = 'y', alpha = 0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi = 300)
    print(f"Grafik histogram berhasil disimpan di: {output_path}")

# menyisipkan teks rahasia ke dalam gambar rekam medis
def embed_data(image_path, message, output_path):
    print(f"=== Membaca citra asli: {image_path} ===")
    img = Image.open(image_path).convert('L')
    data = np.array(img, dtype = int)
    hist, bins = np.histogram(data.flatten(), bins = 256, range = [0, 256])
    hist[0] = 0
    
    peak_point = np.argmax(hist)
    zero_point = np.argmin(hist)

    print(f"Peak Point: {peak_point}")
    print(f"Zero Point: {zero_point}")

    binary_msg = text_to_bin(message)
    binary_msg += '1111111111111110'

    if len(binary_msg) > hist[peak_point]:
        print("!!! Kapasitas citra tidak cukup untuk pesan ini") 
        return

    stego_data = np.copy(data)
    msg_index = 0

    for i in range(stego_data.shape[0]):
        for j in range(stego_data.shape[1]):
            pixel = stego_data[i, j]

            # logika 2 arah
            if peak_point < zero_point:
                if peak_point < pixel < zero_point:
                    stego_data[i, j] += 1
                elif pixel == peak_point:
                    if msg_index < len(binary_msg):
                        stego_data[i, j] += int(binary_msg[msg_index])
                        msg_index += 1
            else:
                if zero_point < pixel < peak_point:
                    stego_data[i, j] -= 1
                elif pixel == peak_point:
                    if msg_index < len(binary_msg):
                        stego_data[i, j] -= int(binary_msg[msg_index])
                        msg_index += 1

    stego_img = Image.fromarray(np.uint8(stego_data))
    stego_img.save(output_path)
    psnr_val = calculate_psnr(data, stego_data)
    print("Pesan berhasil disisipkan!")
    print(f"Citra Stego disimpan di: {output_path}")
    print(f"Nilai PSNR: {psnr_val:.2f} dB")

# mengekstrak pesan rahasia dari citra medis
def extract_data(stego_path, peak_point, zero_point, output_recovered_path):
    print(f"Membaca citra stego: {stego_path}")
    img = Image.open(stego_path).convert('L')
    stego_data = np.array(img, dtype = int)
    recovered_data = np.copy(stego_data)
    extracted_bin = ""

    for i in range(recovered_data.shape[0]):
        for j in range(recovered_data.shape[1]):
            pixel = recovered_data[i, j]

            # LOGIKA DUA ARAH (BIDIRECTIONAL)
            if peak_point < zero_point:
                if pixel == peak_point:
                    extracted_bin += "0"
                elif pixel == peak_point + 1:
                    extracted_bin += "1"
                    recovered_data[i, j] -= 1
                elif peak_point + 1 < pixel <= zero_point:
                    recovered_data[i, j] -= 1
            else:
                if pixel == peak_point:
                    extracted_bin += "0"
                elif pixel == peak_point - 1:
                    extracted_bin += "1"
                    recovered_data[i, j] += 1
                elif zero_point <= pixel < peak_point - 1:
                    recovered_data[i, j] += 1

    delimiter = '1111111111111110'
    msg_end = extracted_bin.find(delimiter)
    if msg_end != -1:
        extracted_bin = extracted_bin[:msg_end]

    message = bin_to_text(extracted_bin)
    rec_img = Image.fromarray(np.uint8(recovered_data))
    rec_img.save(output_recovered_path)

    print("+" + "-" * (27 + len(message)) + "+")
    print(f"| Pesan rahasia diekstrak: {message} |")
    print("+" + "-" * (27 + len(message)) + "+")
    print(f"Citra asli berhasil dipulihkan di: {output_recovered_path}")

# fungsi utama
def main():
    while True:
        print("\n" + "=" * 50)
        print(" PROGRAM REVERSIBLE DATA HIDING (HISTOGRAM SHIFTING)")
        print("="*50)
        print("1. Embed Pesan (Sisipkan data ke gambar)")
        print("2. Extract Pesan (Ambil data & pulihkan gambar)")
        print("3. Buat Grafik Histogram")
        print("4. Keluar")
        print("="*50)
        
        pilihan = input("Pilih menu (1/2/3/4): ")

        if pilihan == '1':
            img_path = input("Masukkan path gambar asli (contoh: xray.png): ")
            msg = input("Masukkan teks rekam medis: ")
            out_path = input("Masukkan nama file stego (contoh: stego.png): ")
            embed_data(img_path, msg, out_path)
            
        elif pilihan == '2':
            stego_path = input("Masukkan path gambar stego (contoh: stego.png): ")
            try:
                peak = int(input("Masukkan nilai Peak Point: "))
                zero = int(input("Masukkan nilai Zero Point: "))
            except ValueError:
                print("!!! Input harus berupa angka bulat.")
                continue
            rec_path = input("Masukkan nama file gambar pulih (contoh: recover.png): ")
            extract_data(stego_path, peak, zero, rec_path)
            
        elif pilihan == '3':
            img_path = input("Masukkan path gambar (contoh: xray.png): ")
            out_path = input("Masukkan nama file grafik (contoh: hist.png): ")
            generate_histogram(img_path, out_path)
            
        elif pilihan == '4':
            print("Keluar dari program. Semoga eksperimen makalahnya sukses!")
            sys.exit()
            
        else:
            print("!!! Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()