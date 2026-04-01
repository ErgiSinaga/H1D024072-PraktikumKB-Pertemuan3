import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

barang_terjual = ctrl.Antecedent(np.arange(0, 101, 1), 'barang_terjual')
permintaan = ctrl.Antecedent(np.arange(0, 301, 1), 'permintaan')
harga_item = ctrl.Antecedent(np.arange(0, 100001, 1), 'harga_item')
profit = ctrl.Antecedent(np.arange(0, 4000001, 1), 'profit')
stok_makanan = ctrl.Consequent(np.arange(0, 1001, 1), 'stok_makanan')

barang_terjual['rendah'] = fuzzy.trimf(barang_terjual.universe, [0, 0, 50])
barang_terjual['sedang'] = fuzzy.trimf(barang_terjual.universe, [30, 50, 70])
barang_terjual['tinggi'] = fuzzy.trimf(barang_terjual.universe, [50, 100, 100])

permintaan['rendah'] = fuzzy.trimf(permintaan.universe, [0, 0, 150])
permintaan['sedang'] = fuzzy.trimf(permintaan.universe, [100, 150, 200])
permintaan['tinggi'] = fuzzy.trimf(permintaan.universe, [150, 300, 300])

harga_item['murah'] = fuzzy.trimf(harga_item.universe, [0, 0, 50000])
harga_item['sedang'] = fuzzy.trimf(harga_item.universe, [30000, 50000, 70000])
harga_item['mahal'] = fuzzy.trimf(harga_item.universe, [50000, 100000, 100000])

profit['rendah'] = fuzzy.trimf(profit.universe, [0, 0, 2000000])
profit['sedang'] = fuzzy.trimf(profit.universe, [1500000, 2500000, 3500000])
profit['tinggi'] = fuzzy.trimf(profit.universe, [2500000, 4000000, 4000000])

stok_makanan['sedang'] = fuzzy.trimf(stok_makanan.universe, [0, 500, 1000])
stok_makanan['banyak'] = fuzzy.trimf(stok_makanan.universe, [500, 1000, 1000])

rule1 = ctrl.Rule(barang_terjual['tinggi'] & permintaan['tinggi'] & harga_item['murah'] & profit['tinggi'], stok_makanan['banyak'])
rule2 = ctrl.Rule(barang_terjual['tinggi'] & permintaan['tinggi'] & harga_item['murah'] & profit['sedang'], stok_makanan['sedang'])
rule3 = ctrl.Rule(barang_terjual['tinggi'] & permintaan['sedang'] & harga_item['murah'] & profit['sedang'], stok_makanan['sedang'])
rule4 = ctrl.Rule(barang_terjual['sedang'] & permintaan['tinggi'] & harga_item['murah'] & profit['sedang'], stok_makanan['sedang'])
rule5 = ctrl.Rule(barang_terjual['sedang'] & permintaan['tinggi'] & harga_item['murah'] & profit['tinggi'], stok_makanan['banyak'])
rule6 = ctrl.Rule(barang_terjual['rendah'] & permintaan['rendah'] & harga_item['sedang'] & profit['sedang'], stok_makanan['sedang'])

stok_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
stok_simulasi = ctrl.ControlSystemSimulation(stok_ctrl)

stok_simulasi.input['barang_terjual'] = 80
stok_simulasi.input['permintaan'] = 255
stok_simulasi.input['harga_item'] = 25000
stok_simulasi.input['profit'] = 3500000

stok_simulasi.compute()
print(f"Jumlah Persediaan Stok Makanan: {stok_simulasi.output['stok_makanan']:.2f} unit")

stok_makanan.view(sim=stok_simulasi)
plt.show()