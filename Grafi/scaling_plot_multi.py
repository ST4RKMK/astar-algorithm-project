
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


base_dir = "multiexperiments"
graph_types = ["geo", "grid", "gnp", "gnk"]

# analisi per grafo
for gtype in graph_types:
    input_dir = os.path.join(base_dir, gtype)
    output_dir = os.path.join(input_dir, "scaling_plots")
    os.makedirs(output_dir, exist_ok=True)

    # Carica tutti i CSV nella sottocartella
    csv_files = [f for f in os.listdir(input_dir) if f.endswith("_results.csv")]
    frames = []

    for f in csv_files:
        df = pd.read_csv(os.path.join(input_dir, f))
        df["n_nodes"] = df["n_nodes"].astype(int)
        frames.append(df)

    if not frames:
        print(f"Nessun file trovato per {gtype}")
        continue

    df_all = pd.concat(frames, ignore_index=True)
    df_all["time_ms"] = df_all["time_sec"] * 1000

    # grafo tempo
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_all, x="n_nodes", y="time_ms", hue="algo", marker="o")
    plt.title(f"Tempo di esecuzione vs N nodi – {gtype}")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Tempo (ms)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{gtype}_scaling_tempo.png"))
    plt.close()

    # grafo nodi
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_all, x="n_nodes", y="nodes_expanded", hue="algo", marker="o")
    plt.title(f"Nodi espansi vs N nodi – {gtype}")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Nodi espansi")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{gtype}_scaling_nodi_espansi.png"))
    plt.close()

    # grafo path cost
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df_all, x="n_nodes", y="path_cost", hue="algo", marker="o")
    plt.title(f"Costo del cammino vs N nodi – {gtype}")
    plt.xlabel("Numero di nodi")
    plt.ylabel("Costo cammino")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{gtype}_scaling_path_cost.png"))
    plt.close()

    print(f"Grafici salvati in: {output_dir}")
