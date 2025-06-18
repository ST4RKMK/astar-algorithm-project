Analisi e Implementazione dell'Algoritmo A*

Questo progetto affronta lo studio approfondito dell'algoritmo A*, con implementazione in Python e analisi sperimentale. Sono stati condotti test su **griglie bidimensionali** e **grafi generati automaticamente**, al fine di confrontare diverse euristiche e valutare le prestazioni computazionali dell’algoritmo.

Struttura del progetto

PythonProject3/
├── 2D/                         # Esperimenti su griglie bidimensionali
│   ├── main2d.py               # Entry point per test su griglie
│   ├── astar2D.py              # Implementazione A* su griglia
│   ├── multipletest.py         # Test multipli su varie dimensioni
│   ├── plot_grid.py            # Visualizzazione dei percorsi su griglia
│   ├── risultati_astar.csv     # Risultati dei test
│
├── Grafi/                      # Esperimenti principali su grafi
│   ├── main.py                 # Entry point
│   ├── astar_graph.py          # A* su grafi generici
│   ├── generate_graph.py       # Costruzione grafi (geo, gnk, gnp, grid)
│   ├── scaling_experiment.py   # Esperimenti di scalabilità
│
├── Prove vecchie/              # Codici precedenti non più attivi
│   └── [vecchi script per grafi]
│
├── results_*.csv               # File di output con risultati
├── plots/, multiexperiments/  # Cartelle con grafici
└── README.md                   # Questo file


Requisiti

Assicurati di avere Python 3.7+ con:
```bash
pip install matplotlib networkx pandas
```

Esecuzione

#Griglie 2D

Dalla cartella `2D/`, puoi eseguire:

```bash
python main2d.py
```

Per lanciare test multipli (dimensioni diverse):

```bash
python multipletest.py
```

I risultati vengono salvati in `.csv` e possono essere visualizzati con `plot_grid.py`.

#Grafi generati

Dalla cartella `Grafi/`:

```bash
python main.py
```

Per test su grafi di diverse dimensioni o strutture:

- `generate_graph.py`: genera i grafi
- `scaling_experiment.py`: misura prestazioni in scaling

Euristiche testate

- `zero_heuristic`: ritorna 0 → equivale a Dijkstra
- `manhattan_heuristic`: somma delle distanze orizzontali e verticali
- `euclidean_heuristic`: distanza geometrica
- `aggressive_manhattan`: Manhattan * 2.5 

Obiettivo del progetto

- Valutare l’impatto dell’euristica su performance e correttezza
- Confrontare A* con BFS e DFS
- Studiare la scalabilità su grafi e griglie

Autore

Giorgio Susanna  
Matricola: 283714  
Università degli studi di L'Aquila
