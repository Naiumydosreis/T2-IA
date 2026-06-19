from hospedagem import hospedagem


class preferencia_alunos:

    def __init__(self, nome_arquivo):
        self.nome_arquivo = nome_arquivo

    def ler_txt(self):
        with open(self.nome_arquivo, "r", encoding="utf-8") as arquivo:
            return [linha.strip() for linha in arquivo if linha.strip()]
    def validar_quantidade_alunos(self, n):
        if n <= 0:
            raise ValueError(
            "A quantidade de alunos deve ser maior que zero."
        )
    def validar_quantidade_linhas(self, linhas, n):
        if len(linhas) != (2 * n + 1):
            raise ValueError(
            "Quantidade de linhas inválida no arquivo."
        )
    def validar_ranking(self, ranking, n):
        if sorted(ranking) != list(range(1, n + 1)):
            raise ValueError(
            "Ranking inválido."
        )
    def carregar(self):
        linhas = self.ler_txt()

        n = int(linhas[0])

        self.validar_quantidade_alunos(n)
        self.validar_quantidade_linhas(linhas, n)

        preferencias_a = {
            1: [1, 2, 3, 4, 5],
            2: [2, 3, 4, 5, 1],
            3: [3, 4, 5, 1, 2]
        }

        preferencias_b = {
            1: [5, 4, 3, 2, 1],
            2: [1, 5, 4, 3, 2],
            3: [2, 1, 5, 4, 3]
        }

        ids_a = set()
        ids_b = set()

        for linha in linhas[1:n + 1]:
            aluno_id, ranking = self.processar_linha(
                linha,
                n,
                ids_a
            )

            preferencias_a[aluno_id] = ranking

        for linha in linhas[n + 1:2 * n + 1]:
            aluno_id, ranking = self.processar_linha(
                linha,
                n,
                ids_b
            )

            preferencias_b[aluno_id] = ranking

        return hospedagem(
            n,
            preferencias_a,
            preferencias_b
        )

    def processar_linha(self, linha, n, ids_lidos):
        partes = linha.split()

        if len(partes) != n + 1:
            raise ValueError(
                f"Linha inválida: {linha}"
            )

        aluno_id = int(partes[0])

        if aluno_id < 1 or aluno_id > n:
            raise ValueError(
                f"ID inválido: {aluno_id}"
            )

        if aluno_id in ids_lidos:
            raise ValueError(
                f"Aluno duplicado: {aluno_id}"
            )

        ids_lidos.add(aluno_id)

        ranking = list(map(int, partes[1:]))

        self.validar_ranking(ranking, n)

        return aluno_id, ranking

    def main():
        nome_arquivo = input(
            "Digite o nome do arquivo: "
        )

        try:
            leitor = preferencia_alunos(nome_arquivo)

            problema = leitor.carregar()

            print("\nCarregou o arquivo")
            print(
                f"Quantidade de alunos: "
                f"{problema.quantidade_alunos}"
            )

        except Exception as erro:
            print(f"\nErro: {erro}")


if __name__ == "__main__":
    preferencia_alunos.main()