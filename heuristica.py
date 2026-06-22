from __future__ import annotations
from hospedagem import hospedagem
from estado_atual import EstadoAtual

def _rank_de(aluno_id: int, parceiro_id: int, preferencias: dict[int, list[int]]) -> int:

    return preferencias[aluno_id].index(parceiro_id) + 1

def _satisfacao_par(rank: int, n: int) -> float:
    if n == 1:
        return 1.0
    return (n - rank) / (n - 1)

def calcular_heuristica(estado: EstadoAtual, problema: hospedagem) -> float:
    n = problema.quantidade_alunos

    if n == 0:
        return 0.0

    soma_satisfacoes = 0.0

    for id_a, id_b in estado.alocacao.items():
        rank_a = _rank_de(id_a, id_b, problema.preferencias_escola_a)
        sat_a = _satisfacao_par(rank_a, n)

        rank_b = _rank_de(id_b, id_a, problema.preferencias_escola_b)
        sat_b = _satisfacao_par(rank_b, n)

        sat_par = (sat_a + sat_b) / 2.0
        soma_satisfacoes += sat_par

    return soma_satisfacoes / n

def detalhes_por_par(estado: EstadoAtual, problema: hospedagem) -> list[dict]:
    n = problema.quantidade_alunos
    resultado = []

    for quarto, (id_a, id_b) in enumerate(sorted(estado.alocacao.items()), 1):
        rank_a = _rank_de(id_a, id_b, problema.preferencias_escola_a)
        rank_b = _rank_de(id_b, id_a, problema.preferencias_escola_b)
        sat_a = _satisfacao_par(rank_a, n)
        sat_b = _satisfacao_par(rank_b, n)
        sat_par = (sat_a + sat_b) / 2.0

        resultado.append({
            'quarto' : quarto,
            'id_a'   : id_a,
            'id_b'   : id_b,
            'rank_a' : rank_a,
            'rank_b' : rank_b,
            'sat_a'  : sat_a,
            'sat_b'  : sat_b,
            'sat_par': sat_par,
        })

    return resultado

def imprimir_avaliacao(estado: EstadoAtual, problema: hospedagem) -> None:
    detalhes = detalhes_por_par(estado, problema)
    h = calcular_heuristica(estado, problema)

    print()
    print(f"  {'Quarto':<8} {'A':<5} {'B':<5} "
          f"{'Rank A':<9} {'Rank B':<9} {'Sat A':<8} {'Sat B':<8} {'Sat Par'}")
    print("  " + "_" * 61)

    for d in detalhes:
        print(f"  {d['quarto']:<8} {d['id_a']:<5} {d['id_b']:<5} "
              f"{d['rank_a']:<9} {d['rank_b']:<9} "
              f"{d['sat_a']:<8.3f} {d['sat_b']:<8.3f} {d['sat_par']:.3f}")

    print(f"  Heurística: {h:.4f} ({'%.1f' % (h * 100)}%)")
    print()

def heuristica_minima(n: int) -> float:
    return 0.0

def heuristica_maxima(n: int) -> float:
    return 1.0

def _demo():
    import sys
    from preferencia_alunos import preferencia_alunos

    nome = sys.argv[1] if len(sys.argv) > 1 else input("Arquivo de teste: ")
    problema = preferencia_alunos(nome).carregar()
    n = problema.quantidade_alunos

    print(f"\n  Arquivo: {nome}  |  N = {n} duplas")
    print("  " + "_" * 61)

    print("\n  Teste 1 - Estado inicial aleatório")
    estado_rand = EstadoAtual.gerar_inicial(problema)
    imprimir_avaliacao(estado_rand, problema)

    print("  Teste 2 - Tentativa de estado ótimo")
    alocacao_otima = {}
    disponiveis_b = list(range(1, n + 1))

    for id_a in range(1, n + 1):
        for candidato in problema.preferencias_escola_a[id_a]:
            if candidato in disponiveis_b:
                alocacao_otima[id_a] = candidato
                disponiveis_b.remove(candidato)
                break

    estado_otimo = EstadoAtual(alocacao_otima)
    imprimir_avaliacao(estado_otimo, problema)

    print("  Teste 3 - Distribuição de 5 estados aleatórios")
    print(f"  {'#':<5} {'Heurística':>12}")
    print("  " + "_" * 18)
    valores = []
    for i in range(1, 6):
        e = EstadoAtual.gerar_inicial(problema)
        h = calcular_heuristica(e, problema)
        valores.append(h)
        print(f"  {i:<5} {h:>12.4f}")

    media = sum(valores) / len(valores)
    print(f"\n  Média aleatória: {media:.4f}")
    print(f"  Máximo teórico:  {heuristica_maxima(n):.4f}")
    print(f"  Mínimo teórico:  {heuristica_minima(n):.4f}")
    print()


if __name__ == "__main__":
    _demo()