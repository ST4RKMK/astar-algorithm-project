import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Percorso della cartella di output
output_dir = "non_heuristic_analysis300x300"
os.makedirs(output_dir, exist_ok=True)  # Crea la cartella se non esiste

# Caricamento del dataset
df = pd.read_csv("results_non_heuristic_300x300.csv")  # Modifica il path se necessario

# Filtro solo i test andati a buon fine
df = df[df["success"] == "yes"]

# Imposto lo stile grafico
sns.set(style="whitegrid")

# Funzione per aggiungere etichette sopra le barre
def add_value_labels(ax):
    for bar in ax.patches:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f'{height:.1f}',
            ha='center',
            va='bottom',
            fontsize=9
        )

# Grafico 1: Nodi espansi
plt.figure(figsize=(8, 5))
ax1 = sns.barplot(data=df, x="heuristic", y="nodes_expanded", ci=None)
add_value_labels(ax1)
plt.title("Nodi espansi medi per euristica (300x300)")
plt.ylabel("Nodi Espansi")
plt.xlabel("Euristica")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "grafico_nodi_espansi.png"))
plt.close()

# Grafico 2: Tempo medio
plt.figure(figsize=(8, 5))
ax2 = sns.barplot(data=df, x="heuristic", y="time_sec", ci=None)
add_value_labels(ax2)
plt.title("Tempo medio di esecuzione per euristica (300x300)")
plt.ylabel("Tempo (s)")
plt.xlabel("Euristica")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "grafico_tempo_medio.png"))
plt.close()

# Grafico 3: Lunghezza del percorso
plt.figure(figsize=(8, 5))
ax3 = sns.barplot(data=df, x="heuristic", y="path_len", ci=None)
add_value_labels(ax3)
plt.title("Lunghezza media del percorso per euristica (300x300)")
plt.ylabel("Path Length")
plt.xlabel("Euristica")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "grafico_path_length.png"))
plt.close()
