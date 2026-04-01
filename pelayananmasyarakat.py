import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

info = ctrl.Antecedent(np.arange(0, 101, 1), 'kejelasan_informasi')
syarat = ctrl.Antecedent(np.arange(0, 101, 1), 'kejelasan_persyaratan')
petugas = ctrl.Antecedent(np.arange(0, 101, 1), 'kemampuan_petugas')
sarpras = ctrl.Antecedent(np.arange(0, 101, 1), 'ketersediaan_sarpras')
kepuasan = ctrl.Consequent(np.arange(0, 401, 1), 'kepuasan_pelayanan')

for var in [info, syarat, petugas, sarpras]:
    var['tidak_memuaskan'] = fuzzy.trimf(var.universe, [0, 0, 75])
    var['cukup_memuaskan'] = fuzzy.trimf(var.universe, [60, 75, 90])
    var['memuaskan'] = fuzzy.trimf(var.universe, [75, 100, 100])

kepuasan['tidak_memuaskan'] = fuzzy.trimf(kepuasan.universe, [0, 0, 100])
kepuasan['kurang_memuaskan'] = fuzzy.trimf(kepuasan.universe, [50, 100, 150])
kepuasan['cukup_memuaskan'] = fuzzy.trimf(kepuasan.universe, [125, 200, 275])
kepuasan['memuaskan'] = fuzzy.trimf(kepuasan.universe, [250, 325, 400])
kepuasan['sangat_memuaskan'] = fuzzy.trimf(kepuasan.universe, [325, 400, 400])

rules = [
    # Rule dasar
    ctrl.Rule(info['tidak_memuaskan'] & syarat['tidak_memuaskan'] & petugas['tidak_memuaskan'] & sarpras['tidak_memuaskan'], kepuasan['tidak_memuaskan']),
    ctrl.Rule(info['cukup_memuaskan'] & syarat['cukup_memuaskan'] & petugas['cukup_memuaskan'] & sarpras['memuaskan'], kepuasan['memuaskan']),
    ctrl.Rule(info['memuaskan'] & syarat['memuaskan'] & petugas['memuaskan'] & sarpras['memuaskan'], kepuasan['sangat_memuaskan']),
    
    # RULE TAMBAHAN PENYELAMAT: Menangkap kondisi input Info=80 (Cukup), Syarat=60 (Tidak), Petugas=50 (Tidak), Sarpras=90 (Memuaskan)
    ctrl.Rule(info['cukup_memuaskan'] & syarat['tidak_memuaskan'] & petugas['tidak_memuaskan'] & sarpras['memuaskan'], kepuasan['kurang_memuaskan'])
]
kepuasan_ctrl = ctrl.ControlSystem(rules)
simulasi = ctrl.ControlSystemSimulation(kepuasan_ctrl)

simulasi.input['kejelasan_informasi'] = 80
simulasi.input['kejelasan_persyaratan'] = 60
simulasi.input['kemampuan_petugas'] = 50
simulasi.input['ketersediaan_sarpras'] = 90

simulasi.compute()
print(f"Nilai Tingkat Kepuasan Pelayanan: {simulasi.output['kepuasan_pelayanan']:.2f}")

kepuasan.view(sim=simulasi)
plt.show()