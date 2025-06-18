
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


input_dir = "multiexperiments"
output_dir = os.path.join(input_dir, "scaling_plots")
os.makedirs(output_dir, exist_ok=True)


all_files = [f for f in os.listdir(input_dir) if f.endswith("_results.csv")]
frames = []

for f in all_files:
    df = pd.read_csv(os.path.join(input_dir, f))
    df["n_nodes"] = df["n_nodes"].astype(int)
    frames.append(df)

df_all = pd.concat(frames, ignore_index=True)

# conversione tempo
df_all["time_ms"] = df_all["time_sec"] * 1000

# plot tempo
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_all, x="n_nodes", y="time_ms", hue="algo", marker="o")
plt.title("Tempo di esecuzione vs Numero di nodi")
plt.xlabel("Numero di nodi")
plt.ylabel("Tempo (ms)")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "scaling_tempo.png"))
plt.close()

# plot nodi espansi
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_all, x="n_nodes", y="nodes_expanded", hue="algo", marker="o")
plt.title("Nodi espansi vs Numero di nodi")
plt.xlabel("Numero di nodi")
plt.ylabel("Nodi espansi")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "scaling_nodi_espansi.png"))
plt.close()

# plot path cost
plt.figure(figsize=(10, 6))
sns.lineplot(data=df_all, x="n_nodes", y="path_cost", hue="algo", marker="o")
plt.title("Costo del cammino vs Numero di nodi")
plt.xlabel("Numero di nodi")
plt.ylabel("Costo del cammino")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "scaling_path_cost.png"))
plt.close()

print(f"✅ Grafici salvati in: {output_dir}")
