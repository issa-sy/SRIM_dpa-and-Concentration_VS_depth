import numpy as np
import matplotlib.pyplot as plt

# === Paramètres ===
fluence = 1.0e15   # ions/cm2
rho = 10.7      # g/cm3 (exemple UO2)
M = 270.03       # g/mol (masse molaire UO2)
fm = 3          # la fraction massique, égale à 3 pour (U + 2O)
NA = 6.022e23    # le nombre d’Avogadro = 6,022x10^23 /mol

# densité atomique hôte (at/cm3)
da = (rho * NA / M) * fm

# Lecture fichiers SRIM exportés
# Exemple fichier range: 2 colonnes : Depth(A) et Cs ions [(Atoms/cm3) / (Atoms/cm2)] 
# Exemple fichier vacancy: 2 colonnes : Depth(A) et Vacancies/(Angstrom-Ion)
ion_dist = np.loadtxt("IonDistribution.txt")   
vac_prof = np.loadtxt("VacancyProfile.txt")    

depth = ion_dist[:,0] * 0.1   # convert A en nm
cs = ion_dist[:,1]
vac = vac_prof[:,1]

# === Calcul concentration Cs (at.%) ===
Cons_cs = cs * fluence      # at/cm3
Cons_en_pourcent = 100.0 * (Cons_cs / (Cons_cs + da))

# === Calcul dpa ===
dpa = vac * fluence * 1e8 / da

# === Tracé ===
fig, ax1 = plt.subplots()

ax1.plot(depth, Cons_en_pourcent, 'k-', label="[Cs] (at.%)")
ax1.set_xlabel("Depth (nm)")
ax1.set_ylabel("[Cs] (at.%)", color='k')
ax1.tick_params(axis='y', labelcolor='k')

ax2 = ax1.twinx()
ax2.plot(depth, dpa, 'r--', label="dpa profile")
ax2.set_ylabel("Number of dpa", color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Rassembler les légendes des deux axes
lines = []
labels = []
for ax in [ax1, ax2]:
    for line in ax.get_lines():
        lines.append(line)
        labels.append(line.get_label())

# Ajouter la légende dans le graphique
ax1.legend(lines, labels, loc='upper right', bbox_to_anchor=(1.0, 1.0))

plt.title("SRIM calculation for Cs $10^{15}$ at.cm$^{-2}$, 800 keV")
fig.tight_layout()
plt.show()
