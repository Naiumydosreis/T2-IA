import sys

from estado_atual import EstadoAtual
from preferencia_alunos import preferencia_alunos
from heuristica import calcular_heuristica
from simulated_annealing import simulated_annealing, PAUSA_A_CADA

import matplotlib.pyplot as plt

def mostrar_tabela_evolucao(historico):
    print("\n--- Evolução da heurística ---")
    print(f"  {'Nível':<8} {'Temperatura':<14} {'Heurística':<12} {'Descontentamento'}")
    print("  " + "-" * 52)

    passo = max(1, len(historico) // 20)
    for nivel, temp, h, custo in historico[::passo]:
        print(f"  {nivel:<8} {temp:<14.4f} {h:<12.4f} {custo}")

    nivel, temp, h, custo = historico[-1]
    print(f"  {nivel:<8} {temp:<14.4f} {h:<12.4f} {custo}  <- final")


def salvar_grafico_evolucao(historico, nome_arquivo):
    import os
    os.makedirs("resultados", exist_ok=True)

    niveis = [r[0] for r in historico]
    heuristicas = [r[2] for r in historico]

    base = os.path.splitext(os.path.basename(nome_arquivo))[0]
    caminho = os.path.join("resultados", f"{base}_heuristica.png")

    plt.figure(figsize=(9, 4))
    plt.plot(niveis, heuristicas, color="royalblue", linewidth=1.5)
    plt.xlabel("Nível de temperatura")
    plt.ylabel("Heurística (satisfação média)")
    plt.title(f"Evolução da heurística — {nome_arquivo}")
    plt.ylim(0, 1.05)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()
    print(f"\n  Gráfico salvo em: {caminho}")


def mostrar_solucao(melhor_estado, melhor_custo, problema):
    texto_codificado = melhor_estado.codificar()

    print("\n--- Solução codificada ---")
    print(texto_codificado)

    print("\n--- Solução decodificada ---")
    estado_decodificado = EstadoAtual.decodificar(texto_codificado)
    for id_a, id_b in sorted(estado_decodificado.alocacao.items()):
        print(f"  Aluno {id_a} (Escola A) vai dividir quarto com Aluno {id_b} (Escola B)")

    h = calcular_heuristica(melhor_estado, problema)
    print(f"\n  Descontentamento total : {melhor_custo}")
    print(f"  Satisfação média       : {h:.4f} ({h * 100:.1f}%)")


def main():
    if len(sys.argv) >= 2:
        nome_arquivo = sys.argv[1]
        print(f"Arquivo: {nome_arquivo}")
    else:
        nome_arquivo = input("Arquivo de teste: ").strip()

    problema = preferencia_alunos(nome_arquivo).carregar()
    n = problema.quantidade_alunos
    print(f"Instância carregada: {n} duplas")

    print("\nModos de execução:")
    print("  1 - Automático (exibe resultado ao final)")
    print("  2 - Passo a passo (pausa a cada 10 níveis de temperatura)")
    modo = input("Escolha (1 ou 2): ").strip()

    if modo == "2":
        print(f"\n  Executando passo a passo (pausa a cada {PAUSA_A_CADA} níveis | q + Enter para terminar)...\n")

    melhor_estado, melhor_custo, historico = simulated_annealing(problema, passo_a_passo=(modo == "2"))

    mostrar_tabela_evolucao(historico)
    salvar_grafico_evolucao(historico, nome_arquivo)
    mostrar_solucao(melhor_estado, melhor_custo, problema)


if __name__ == "__main__":
    main()
