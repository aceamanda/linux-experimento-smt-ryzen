#!/usr/bin/env python3
"""
Análise estatística do experimento SMT - AMD Ryzen 7 4800H
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

# ===== CARREGA OS DADOS =====
df = pd.read_csv('data/results.csv')
threads = sorted(df['threads'].unique())
baseline = df[df['threads'] == 1]['events_per_second'].values

print("=" * 60)
print("ANÁLISE ESTATÍSTICA — SMT AMD Ryzen 7 4800H")
print("=" * 60)
print(f"\n{'Threads':<10}{'Média':>12}{'Desvio-P':>12}{'IC 95% inf':>12}{'IC 95% sup':>12}{'Speedup':>10}{'Efic.(%)':>10}{'p-valor':>12}")
print("-" * 100)

resultados = []

for t in threads:
    dados = df[df['threads'] == t]['events_per_second'].values
    media = np.mean(dados)
    desvio = np.std(dados, ddof=1)
    n = len(dados)
    ic = stats.t.interval(0.95, df=n-1, loc=media, scale=stats.sem(dados))
    speedup = media / np.mean(baseline)
    eficiencia = (speedup / t) * 100

    # Teste t contra baseline (exceto baseline em si)
    if t == 1:
        pvalor = 1.0
    else:
        _, pvalor = stats.ttest_ind(dados, baseline)

    print(f"{t:<10}{media:>12.2f}{desvio:>12.2f}{ic[0]:>12.2f}{ic[1]:>12.2f}{speedup:>10.3f}{eficiencia:>10.1f}{pvalor:>12.6f}")

    resultados.append({
        'threads': t,
        'media': media,
        'desvio': desvio,
        'ic_inf': ic[0],
        'ic_sup': ic[1],
        'speedup': speedup,
        'eficiencia': eficiencia,
        'pvalor': pvalor
    })

res = pd.DataFrame(resultados)

# ===== GRÁFICO 1: SPEEDUP =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.errorbar(res['threads'], res['speedup'],
             yerr=[res['speedup'] - res['ic_inf'] / np.mean(baseline),
                   res['ic_sup'] / np.mean(baseline) - res['speedup']],
             fmt='o-', color='steelblue', linewidth=2, markersize=8,
             label='Speedup observado', capsize=5)
ax1.plot(threads, threads, 'r--', linewidth=1.5, label='Speedup ideal (linear)')
ax1.set_xlabel('Número de threads', fontsize=12)
ax1.set_ylabel('Speedup', fontsize=12)
ax1.set_title('Speedup vs Threads — AMD Ryzen 7 4800H', fontsize=13)
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xticks(threads)

# ===== GRÁFICO 2: EFICIÊNCIA =====
ax2.bar(res['threads'], res['eficiencia'],
        color='steelblue', alpha=0.7, edgecolor='black')
ax2.axhline(y=100, color='red', linestyle='--', linewidth=1.5, label='Eficiência ideal')
ax2.set_xlabel('Número de threads', fontsize=12)
ax2.set_ylabel('Eficiência (%)', fontsize=12)
ax2.set_title('Eficiência do Paralelismo por Condição', fontsize=13)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3, axis='y')
ax2.set_xticks(threads)

os.makedirs('figures', exist_ok=True)
plt.tight_layout()
plt.savefig('figures/speedup_eficiencia.png', dpi=150)
print("\n✓ Gráfico salvo em: figures/speedup_eficiencia.png")

# ===== LEI DE AMDAHL =====
print("\n" + "=" * 60)
print("ESTIMATIVA DA FRAÇÃO SERIAL (Lei de Amdahl)")
print("=" * 60)
for _, row in res.iterrows():
    t = row['threads']
    s = row['speedup']
    if t > 1 and s < t:
        f = (1/s - 1/t) / (1 - 1/t)
        print(f"  {int(t):>2} threads → fração serial estimada: {f:.4f} ({f*100:.2f}%)")
