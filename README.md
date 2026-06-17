# Eficiência do SMT no AMD Ryzen 7 4800H: Escalonamento multicore sob Linux

## Repositório do artigo científico submetido à disciplina de Infraestrutura de Hardware 2026.1 — CESAR School.

> O SMT (Simultaneous Multithreading) é uma tecnologia que permite que um único núcleo físico execute mais de uma thread simultaneamente. O AMD Ryzen 7 4800H foi um dos primeiros processadores móveis da AMD a apresentar ganhos expressivos de desempenho com essa tecnologia em notebooks. O uso do SMT impacta diretamente o desempenho do sistema ao possibilitar uma melhor utilização dos recursos do processador, beneficiando aplicações paralelizáveis, como compilação de programas e jogos modernos que distribuem suas tarefas entre múltiplas threads. Esse repositório contém um script que tem como objetivo avaliar a eficiência do SMT no Ryzen 7 4800H em ambiente Linux, por meio da coleta e análise de dados de speedup obtidos com a ferramenta Sysbench, variando-se o número de threads utilizadas nos testes.

## Pergunta de Pesquisa

O aumento do número de threads produz ganhos proporcionais de desempenho até o limite lógico do AMD Ryzen 7 4800H executando Linux?

## Hipóteses

- **H0:** O speedup escala linearmente com o número de threads
- **H1:** O speedup é significativamente inferior ao linear devido ao overhead do SMT e disputa por recursos compartilhados

## Ambiente Experimental

| Componente | Especificação |
|---|---|
| CPU | AMD Ryzen 7 4800H (8 núcleos, 16 threads, Zen 2) |
| RAM | 7,1 GiB DDR4 |
| SSD | SanDisk WD Blue SN550 NVMe |
| SO | Pop!_OS 24.04 LTS (x86_64) |
| Kernel | Linux 6.x |
| Sysbench | 1.0.20 |
| Python | 3.x |

### Artigo disponível na pasta "Artigo" como um pdf!

## 💻 Como executar
> ⚠️ Atenção! caso queira reproduzir esse experimento em outros processadores prestar atenção na sessão "Reprodução em Outros Processadores" (Compativél com qualquer Linux já que usa sysbench)

### 1. Requisitos

```bash
sudo apt install -y sysbench python3-pip
pip3 install --break-system-packages pandas scipy matplotlib numpy
```

### 2. Clone o repositório

```bash
git clone https://github.com/aceamanda/linux-experimento-smt-ryzen
cd linux-experimento-smt-ryzen
```
## Estrutura do Repositório
linux-experimento-smt-ryzen/
├── README.md
├── data/
│   └── results.csv
├── figures/
│   └── speedup_eficiencia.png
└── scripts/
    ├── run_experiments.sh
    └── analyze.py

### 3. Execute o experimento

> ⚠️ O script requer sudo para controlar o governor de CPU.
> Duração estimada: 30-40 minutos.

```bash
sudo bash scripts/run_experiments.sh
```

Os dados serão salvos em `data/results.csv`.

### 4. Gere a análise e os gráficos

```bash
python3 scripts/analyze.py
```

Os gráficos serão salvos em `figures/speedup_eficiencia.png`.

---

## Resultados Principais

| Threads | Média (events/s) | Speedup | Eficiência (%) |
|---|---|---|---|
| 1 | 2080,19 ± 0,67 | 1,000 | 100,0 |
| 2 | 4161,48 ± 0,90 | 2,001 | 100,0 |
| 4 | 8276,69 ± 20,11 | 3,979 | 99,5 |
| 8 | 15966,97 ± 54,28 | 7,676 | 95,9 |
| 16 | 17112,39 ± 21,74 | 8,226 | 51,4 |

O speedup escala de forma quase linear até 8 threads (núcleos físicos).
A transição para 16 threads via SMT produziu ganho adicional de apenas 7%,
com queda de eficiência para 51,4%.

## Reprodução em Outros Processadores

O script `run_experiments.sh` é compatível com qualquer processador
Linux. Para adaptar ao seu hardware:

1. Descubra seus núcleos e threads:
```bash
lscpu | grep -E "núcleo|Thread|CPU\(s\)"
```

2. Edite a linha `THREADS` no script:
```bash
# Exemplo para Intel i5-8265U (4 núcleos, 8 threads)
THREADS=(1 2 4 8)

# Exemplo para Ryzen 9 5900X (12 núcleos, 24 threads)
THREADS=(1 2 4 8 12 24)
```

3. Execute normalmente:
```bash
sudo bash scripts/run_experiments.sh
python3 scripts/analyze.py
```

Contribuições com resultados de outros hardwares são bem-vindas
via Pull Request :)!

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/aceamanda" title="Github Amanda">
        <img src="https://avatars.githubusercontent.com/u/205168124?v=4" width="100px;" alt="Foto de Amanda Bormann"/><br>
        <sub>
          <b>Amanda Bormann</b>
        </sub>
      </a>
    </td>
  
