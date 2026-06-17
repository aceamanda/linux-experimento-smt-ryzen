#!/bin/bash
# Experimento: Eficiência do SMT no AMD Ryzen 7 4800H
# Descrição: Coleta dados de speedup com sysbench variando threads

set -e

# ===== CONFIGURAÇÕES =====
THREADS=(1 2 4 8 16)
WARMUP=3
REPETICOES=30
OUTPUT="data/results.csv"
PRIME_LIMIT=10000
TEMPO=10

# ===== CONTROLE DO AMBIENTE =====
echo "Configurando governor para performance..."
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo performance | sudo tee $cpu > /dev/null
done

# ===== CABEÇALHO DO CSV =====
mkdir -p data
echo "threads,repeticao,events_per_second" > $OUTPUT

# ===== EXPERIMENTO =====
for t in "${THREADS[@]}"; do
    echo ""
    echo "=============================="
    echo "Testando com $t thread(s)..."
    echo "=============================="

    # Warm-up (descartado)
    echo "  Rodando $WARMUP warm-ups..."
    for i in $(seq 1 $WARMUP); do
        sysbench cpu --threads=$t --time=$TEMPO --cpu-max-prime=$PRIME_LIMIT run > /dev/null
    done

    # Coleta real
    echo "  Coletando $REPETICOES repetições..."
    for i in $(seq 1 $REPETICOES); do
        RESULT=$(sysbench cpu --threads=$t --time=$TEMPO \
            --cpu-max-prime=$PRIME_LIMIT run \
            | grep "events per second" \
            | awk '{print $NF}')
        echo "$t,$i,$RESULT" >> $OUTPUT
        echo "    Rep $i/$REPETICOES: $RESULT events/s"
    done
done

# ===== RESTAURA GOVERNOR =====
echo ""
echo "Restaurando governor para powersave..."
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
    echo powersave | sudo tee $cpu > /dev/null
done

echo ""
echo "=============================="
echo "Concluído! Dados em: $OUTPUT"