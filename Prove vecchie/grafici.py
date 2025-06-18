import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os


sns.set_theme(style="whitegrid")
output_dir = "grafici"
os.makedirs(output_dir, exist_ok=True)


df = pd.read_csv("results_astar_comparison.csv")

# Pre-elabora: aggiungi colonna binaria di successo
df["success_bin"] = df["success"].map({"yes": 1, "no": 0})

# 1. Success Rate per modello
plt.figure(figsize=(6, 4))
success_rate = df.groupby("model")["success_bin"].mean().reset_index()
sns.barplot(data=success_rate, x="model", y="success_bin", hue="model", palette="crest", legend=False)
plt.title("Success Rate per Modello di Grafo")
plt.ylabel("Percentuale di Successo")
plt.xlabel("Modello")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(f"{output_dir}/success_rate.png", dpi=300)
plt.close()

# 2. Tempo medio di esecuzione
plt.figure(figsize=(6, 4))
avg_time = df.groupby("model")["time_sec"].mean().reset_index()
sns.barplot(data=avg_time, x="model", y="time_sec", hue="model", palette="flare", legend=False)
plt.title("Tempo Medio di Esecuzione (secondi)")
plt.ylabel("Tempo (s)")
plt.xlabel("Modello")
plt.tight_layout()
plt.savefig(f"{output_dir}/avg_time.png", dpi=300)
plt.close()

# 3. Nodi espansi in media
plt.figure(figsize=(6, 4))
avg_nodes = df.groupby("model")["nodes_expanded"].mean().reset_index()
sns.barplot(data=avg_nodes, x="model", y="nodes_expanded", hue="model", palette="mako", legend=False)
plt.title("Nodi Espansi in Media")
plt.ylabel("Numero di Nodi")
plt.xlabel("Modello")
plt.tight_layout()
plt.savefig(f"{output_dir}/avg_nodes_expanded.png", dpi=300)
plt.close()

print(f"[✓] Grafici salvati in: {output_dir}/")
