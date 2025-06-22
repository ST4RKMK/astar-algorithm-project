import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Imposta le directory
input_dir = "multiexperiments_2000"
output_dir = os.path.join(input_dir, "comparison_astar")
os.makedirs(output_dir, exist_ok=True)

# Raccoglie tutti i CSV dai sottodirectory
all_files = [
    os.path.join(input_dir, graph_dir, f)
    for graph_dir in os.listdir(input_dir)
    if os.path.isdir(os.path.join(input_dir, graph_dir))
    for f in os.listdir(os.path.join(input_dir, graph_dir))
    if f.endswith("_results.csv")
]

# Unisce i file in un unico DataFrame
df_list = [pd.read_csv(f) for f in all_files]
df = pd.concat(df_list, ignore_index=True)

# Estrai il tipo di grafo dal nome
df["graph_type"] = df["graph"].apply(lambda x: x.split("_")[0])
df["time_ms"] = df["time_sec"] * 1000

# Seleziona solo gli algoritmi A*
astar_algos = ["astar_null", "astar_euclidean", "astar_manhattan"]
df_astar = df[df["algo"].isin(astar_algos)]

# Genera un grafico per ogni variante A*
for algo in astar_algos:
    subset = df_astar[df_astar["algo"] == algo]
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=subset,
        x="n_nodes",
        y="time_ms",
        hue="graph_type",
        marker="o",
        errorbar="sd",
        linewidth=2.5
    )
    plt.title(f"Tempo medio vs numero di nodi – {algo}")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo medio (ms)")
    plt.grid(True)
    plt.tight_layout()
    output_path = os.path.join(output_dir, f"time_vs_n_graphs_{algo}.png")
    plt.savefig(output_path)
    plt.close()

print(f"Grafici salvati in: {output_dir}")
