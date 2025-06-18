import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caricamento file
base_dir = "experiments"
csv_files = []

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith("_results.csv"):
            csv_files.append(os.path.join(root, file))

#  tipo grafo
def infer_graph_type(name):
    name = name.lower()
    if "grid" in name:
        return "grid"
    elif "geo" in name:
        return "geometric"
    elif "gnp" in name:
        return "gnp"
    elif "gnk" in name:
        return "gnk"
    else:
        return "custom"

frames = []
for f in csv_files:
    df = pd.read_csv(f)
    df["graph_type"] = df["graph"].apply(infer_graph_type)
    df["time_ms"] = df["time_sec"] * 1000  # Converti in millisecondi
    frames.append(df)

df_all = pd.concat(frames, ignore_index=True)

# Filtra solo algoritmi desiderati
algos = ["astar_null", "astar_manhattan", "astar_euclidean", "bfs", "dfs"]
df_plot = df_all[df_all["algo"].isin(algos)]

# Crea cartella output
output_dir = "grafici_analisi_avanzata"
os.makedirs(output_dir, exist_ok=True)

#  Barplot con media e std (tempo in ms)
plt.figure(figsize=(10, 6))
sns.barplot(data=df_plot, x="algo", y="time_ms", hue="graph_type", estimator="mean", errorbar="sd")
plt.title("Tempo medio (ms) per algoritmo e tipo di grafo")
plt.xlabel("Algoritmo")
plt.ylabel("Tempo (millisecondi)")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "barplot_tempo_ms_per_algoritmo.png"))
plt.close()

# : Barplot nodi espansi
plt.figure(figsize=(10, 6))
sns.barplot(data=df_plot, x="algo", y="nodes_expanded", hue="graph_type", estimator="mean", errorbar="sd")
plt.title("Nodi espansi medi per algoritmo e tipo di grafo")
plt.xlabel("Algoritmo")
plt.ylabel("Nodi espansi")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "barplot_nodi_espansi_per_algoritmo.png"))
plt.close()

# Scatter separati per tipo di grafo
for gtype in df_plot["graph_type"].unique():
    df_g = df_plot[df_plot["graph_type"] == gtype]
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_g, x="path_cost", y="nodes_expanded", hue="algo", style="algo", s=100)
    plt.title(f"Scatter: Costo vs Nodi Espansi – {gtype.capitalize()}")
    plt.xlabel("Costo del cammino")
    plt.ylabel("Nodi espansi")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"scatter_pathcost_nodiexp_{gtype}.png"))
    plt.close()

print(f" Grafici salvati nella cartella: {output_dir}")
