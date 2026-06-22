import random
import re
from hospedagem import hospedagem


class EstadoAtual:

    def __init__(self, alocacao: dict[int, int]):
        self.alocacao: dict[int, int] = alocacao


    @classmethod
    def gerar_inicial(cls, problema: hospedagem) -> "EstadoAtual":
        n = problema.quantidade_alunos
        ids_b = list(range(1, n + 1))
        random.shuffle(ids_b)
        alocacao = {id_a: ids_b[i] for i, id_a in enumerate(range(1, n + 1))}
        return cls(alocacao)

    def calcular_descontentamento(self, problema: hospedagem) -> int:
        total = 0
        for id_a, id_b in self.alocacao.items():
            rank_a = problema.preferencias_escola_a[id_a].index(id_b) + 1
            rank_b = problema.preferencias_escola_b[id_b].index(id_a) + 1
            total += rank_a + rank_b
        return total

    def aplicar_troca(self, id_a1: int, id_a2: int) -> "EstadoAtual":
        nova = dict(self.alocacao)
        nova[id_a1], nova[id_a2] = nova[id_a2], nova[id_a1]
        return EstadoAtual(nova)

    def par_aleatorio(self) -> tuple[int, int]:
        id_a1, id_a2 = random.sample(sorted(self.alocacao), 2)
        return id_a1, id_a2

    def codificar(self) -> str:
        linhas = [
            f"Quarto {i}: Escola A [ID {id_a}] - Escola B [ID {id_b}]"
            for i, (id_a, id_b) in enumerate(sorted(self.alocacao.items()), 1)
        ]
        return "\n".join(linhas)

    @staticmethod
    def decodificar(texto: str) -> "EstadoAtual":
        alocacao = {}
        for linha in texto.strip().splitlines():
            ids = re.findall(r"ID (\d+)", linha)
            if len(ids) == 2:
                alocacao[int(ids[0])] = int(ids[1])
        if not alocacao:
            raise ValueError("Texto inválido: nenhum par encontrado.")
        return EstadoAtual(alocacao)

    def __str__(self) -> str:
        return self.codificar()

    def __repr__(self) -> str:
        return f"EstadoAtual({self.alocacao!r})"

    def __eq__(self, outro: object) -> bool:
        if not isinstance(outro, EstadoAtual):
            return NotImplemented
        return self.alocacao == outro.alocacao

def _demo():
    from preferencia_alunos import preferencia_alunos

    nome = input("Arquivo de teste: ")
    problema = preferencia_alunos(nome).carregar()

    estado = EstadoAtual.gerar_inicial(problema)

    print("\n--- Estado inicial ---")
    print(estado)
    custo = estado.calcular_descontentamento(problema)
    print(f"\nDescontentamento total: {custo}")

    id_a1, id_a2 = estado.par_aleatorio()
    vizinho = estado.aplicar_troca(id_a1, id_a2)
    print(f"\n--- Vizinho (troca A{id_a1} <-> A{id_a2}) ---")
    print(vizinho)
    print(f"\nDescontentamento do vizinho: {vizinho.calcular_descontentamento(problema)}")

    print("\n--- Codificar / decodificar ---")
    texto = estado.codificar()
    reconstruido = EstadoAtual.decodificar(texto)
    print(f"Reconstrução idêntica: {estado == reconstruido}")


if __name__ == "__main__":
    _demo()
