# H1D024072-PraktikumKB-Pertemuan3
Yustinus Ergi Owen Sinaga - Shift C

Program kedua ini adalah implementasi sistem kontrol fuzzy untuk mengevaluasi tingkat kepuasan pelayanan. Pengambilan keputusan didasarkan pada empat variabel input: kejelasan informasi, kejelasan persyaratan, kemampuan petugas, dan ketersediaan sarana prasarana. Program ini juga menunjukkan efisiensi penulisan kode dengan menggunakan perulangan (for loop) untuk mendefinisikan kurva keanggotaan yang identik

PENJELASAN PROGRAM :

info = ctrl.Antecedent(np.arange(0, 101, 1), 'kejelasan_informasi')
syarat = ctrl.Antecedent(np.arange(0, 101, 1), 'kejelasan_persyaratan')
petugas = ctrl.Antecedent(np.arange(0, 101, 1), 'kemampuan_petugas')
sarpras = ctrl.Antecedent(np.arange(0, 101, 1), 'ketersediaan_sarpras')
kepuasan = ctrl.Consequent(np.arange(0, 401, 1), 'kepuasan_pelayanan')
*Bagian ini mendefinisikan 4 variabel input dengan rentang nilai 0-100, dan 1 variabel output dengan rentang nilai yang lebih besar yaitu 0-400*

for var in [info, syarat, petugas, sarpras]:
    var['tidak_memuaskan'] = fuzzy.trimf(var.universe, [0, 0, 75])
    var['cukup_memuaskan'] = fuzzy.trimf(var.universe, [60, 75, 90])
    var['memuaskan'] = fuzzy.trimf(var.universe, [75, 100, 100])
*Berbeda dengan program sebelumnya, bagian ini memanfaatkan perulangan for dalam Python untuk secara otomatis memberikan kurva segitiga (fuzzy.trimf) dengan rentang yang persis sama kepada 4 variabel input sekaligus, sehingga kode menjadi lebih ringkas*

kepuasan['tidak_memuaskan'] = fuzzy.trimf(kepuasan.universe, [0, 0, 100])
# ... (sampai 'sangat_memuaskan')
*Variabel output dibagi menjadi 5 tingkatan linguistik (dari tidak memuaskan hingga sangat memuaskan) dengan rentangnya masing-masing*

rules = [
    # Rule dasar
    ctrl.Rule(info['tidak_memuaskan'] & syarat['tidak_memuaskan'] & petugas['tidak_memuaskan'] & sarpras['tidak_memuaskan'], kepuasan['tidak_memuaskan']),
    # ...
    # RULE TAMBAHAN PENYELAMAT
    ctrl.Rule(info['cukup_memuaskan'] & syarat['tidak_memuaskan'] & petugas['tidak_memuaskan'] & sarpras['memuaskan'], kepuasan['kurang_memuaskan'])
]
kepuasan_ctrl = ctrl.ControlSystem(rules)
*Aturan dikelompokkan ke dalam sebuah struktur data List Python (rules = [...]), yang kemudian dimasukkan sekaligus ke dalam ctrl.ControlSystem. Terdapat satu rule spesifik (rule penyelamat) yang dirancang untuk menangani kondisi input unik yang tidak ter-cover oleh rule dasar*

simulasi = ctrl.ControlSystemSimulation(kepuasan_ctrl)
simulasi.input['kejelasan_informasi'] = 80
simulasi.input['kejelasan_persyaratan'] = 60
simulasi.input['kemampuan_petugas'] = 50
simulasi.input['ketersediaan_sarpras'] = 90
simulasi.compute()
print(f"Nilai Tingkat Kepuasan Pelayanan: {simulasi.output['kepuasan_pelayanan']:.2f}")
kepuasan.view(sim=simulasi)
plt.show()
*Input diberikan sesuai studi kasus (80, 60, 50, 90). Kemudian program memproses nilai tersebut menggunakan .compute() dan menampilkan outputnya ke konsol dan grafik menggunakan .view() dan plt.show()*
