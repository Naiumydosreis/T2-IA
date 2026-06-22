import math
import random

from estado_atual import EstadoAtual
from heuristica import calcular_heuristica


# Parâmetros do algoritmo
ALPHA = 0.995
ITERACOES_POR_TEMP = 10
TEMPERATURA_MINIMA = 0.01
MAX_ITERACOES_SEM_MELHORA = 500
PAUSA_A_CADA = 10


def gerar_sucessor(estado):
    id_a1, id_a2 = estado.par_aleatorio()
    return estado.aplicar_troca(id_a1, id_a2)


def aceitar_solucao(delta, temperatura):
    if delta < 0:
        return True
    return random.random() < math.exp(-delta / temperatura)


def simulated_annealing(problema, passo_a_passo=False):
    n = problema.quantidade_alunos
    temperatura = 2.0 * n

    estado_atual = EstadoAtual.gerar_inicial(problema)
    custo_atual = estado_atual.calcular_descontentamento(problema)

    melhor_estado = estado_atual
    melhor_custo = custo_atual

    iteracoes_sem_melhora = 0
    nivel = 0
    historico_heuristica = []

    while temperatura > TEMPERATURA_MINIMA and iteracoes_sem_melhora < MAX_ITERACOES_SEM_MELHORA:
        for _ in range(ITERACOES_POR_TEMP):
            vizinho = gerar_sucessor(estado_atual)
            custo_vizinho = vizinho.calcular_descontentamento(problema)
            delta = custo_vizinho - custo_atual

            if aceitar_solucao(delta, temperatura):
                estado_atual = vizinho
                custo_atual = custo_vizinho

            if custo_atual < melhor_custo:
                melhor_estado = estado_atual
                melhor_custo = custo_atual
                iteracoes_sem_melhora = 0

        nivel += 1
        heuristica_atual = calcular_heuristica(melhor_estado, problema)
        historico_heuristica.append((nivel, temperatura, heuristica_atual, melhor_custo))

        if passo_a_passo and nivel % PAUSA_A_CADA == 0:
            print(f"  Nível {nivel:>4} | T={temperatura:>8.4f} | "
                  f"Heurística={heuristica_atual:.4f} | Descontentamento={melhor_custo}")
            entrada = input("  [Enter para continuar | q + Enter para terminar] ")
            if entrada.strip().lower() == "q":
                break

        iteracoes_sem_melhora += 1
        temperatura = temperatura * ALPHA

    return melhor_estado, melhor_custo, historico_heuristica
