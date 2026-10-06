!pip install pandas matplotlib seaborn openpyxl

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import Markdown, display

arquivo = "Tabela13.xlsx"

# ============================================================
# PARTE 1
# ============================================================

df = pd.read_excel(
    arquivo,
    sheet_name="Exemplo Gráfico Brasil"
)

df = df.dropna(axis=1, how="all")

if "Meio de Transporte" not in df.columns:
    df = df.rename(columns={
        df.columns[0]: "Meio de Transporte"
    })

df = df[[
    "Meio de Transporte",
    "Branca",
    "Preta ou Parda",
    "Indígena"
]].copy()

for coluna in ["Branca", "Preta ou Parda", "Indígena"]:
    df[coluna] = pd.to_numeric(
        df[coluna],
        errors="coerce"
    )

df = df.dropna(
    subset=["Branca", "Preta ou Parda", "Indígena"]
)

print("DADOS DA PARTE 1")
display(df)

cores = [
    "#ff9999",
    "#66b3ff",
    "#99ff99",
    "#ffcc99",
    "#c2c2f0",
    "#ffb3e6"
]

grupos = [
    "Branca",
    "Preta ou Parda",
    "Indígena"
]

fig, axes = plt.subplots(
    1,
    3,
    figsize=(20, 7)
)

for i, col in enumerate(grupos):
    axes[i].pie(
        df[col],
        labels=df["Meio de Transporte"],
        autopct="%1.3f%%",
        startangle=180,
        colors=cores,
        wedgeprops={
            "edgecolor": "white",
            "linewidth": 1.2
        }
    )

    axes[i].set_title(
        f"Cor/Raça: {col}",
        fontsize=12,
        fontweight="bold"
    )

plt.suptitle(
    "Distribuição dos meios de transporte das mulheres por cor ou raça — Brasil, 2022",
    fontsize=14,
    fontweight="bold"
)

plt.tight_layout()
plt.savefig(
    "grafico_transporte.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


comparacao = df.copy()

comparacao["Branca - Preta ou Parda"] = (
    comparacao["Branca"]
    - comparacao["Preta ou Parda"]
)

comparacao["Branca - Indígena"] = (
    comparacao["Branca"]
    - comparacao["Indígena"]
)

comparacao["Preta ou Parda - Indígena"] = (
    comparacao["Preta ou Parda"]
    - comparacao["Indígena"]
)

print("DIFERENÇAS ENTRE OS GRUPOS")
display(comparacao)

print("\nANÁLISE DOS GRÁFICOS\n")

for _, linha in comparacao.iterrows():

    print(
        f"{linha['Meio de Transporte']}: "
        f"mulheres brancas - mulheres pretas ou pardas = "
        f"{linha['Branca - Preta ou Parda']:.3f}%"
    )

    print(
        f"{linha['Meio de Transporte']}: "
        f"mulheres brancas - mulheres indígenas = "
        f"{linha['Branca - Indígena']:.3f}%"
    )

    print(
        f"{linha['Meio de Transporte']}: "
        f"mulheres pretas ou pardas - mulheres indígenas = "
        f"{linha['Preta ou Parda - Indígena']:.3f}%"
    )

    print()

display(Markdown("""
## Análise dos gráficos

Os gráficos mostram diferenças na utilização dos meios de transporte entre mulheres brancas, pretas ou pardas e indígenas.

A tabela de diferenças permite comparar cada meio de transporte entre os três grupos.

Valores positivos indicam que o primeiro grupo da comparação apresenta percentual maior. Valores negativos indicam que apresenta percentual menor.

A maior diferença pode ser identificada observando os valores absolutos apresentados para cada meio de transporte.
"""))

# ============================================================
# PARTE 2
# ============================================================

df2 = pd.read_excel(
    arquivo,
    sheet_name="BR GR UF MU",
    header=[1, 2]
)

df2 = df2.dropna(
    axis=1,
    how="all"
)

df2.columns = [
    "_".join(
        [
            str(valor).strip()
            for valor in coluna
            if str(valor) != "nan"
        ]
    ).strip()
    for coluna in df2.columns
]

id_col = df2.columns[0]

print("DADOS DA ABA BR GR UF MU")
display(df2.head())


estados = [
    "Rondônia",
    "Acre",
    "Amazonas",
    "Roraima",
    "Pará",
    "Amapá",
    "Tocantins",
    "Maranhão",
    "Piauí",
    "Ceará",
    "Rio Grande do Norte",
    "Paraíba",
    "Pernambuco",
    "Alagoas",
    "Sergipe",
    "Bahia",
    "Minas Gerais",
    "Espírito Santo",
    "Rio de Janeiro",
    "São Paulo",
    "Paraná",
    "Santa Catarina",
    "Rio Grande do Sul",
    "Mato Grosso do Sul",
    "Mato Grosso",
    "Goiás",
    "Distrito Federal"
]

regioes = [
    "Brasil",
    "Norte",
    "Nordeste",
    "Sudeste",
    "Sul",
    "Centro-oeste",
    "Centro-Oeste"
]

df_estados = df2[
    df2[id_col].isin(estados)
].copy()

print("APENAS OS ESTADOS")
display(df_estados[[id_col]])


df_long = df_estados.melt(
    id_vars=id_col,
    var_name="Variavel",
    value_name="Percentual"
)

df_long["Percentual"] = pd.to_numeric(
    df_long["Percentual"],
    errors="coerce"
)

df_long = df_long.dropna(
    subset=["Percentual"]
)

print("DADOS NO FORMATO LONGO")
display(df_long.head())

coletivo = df_long[
    df_long["Variavel"].str.contains(
        "Transporte coletivo",
        case=False,
        na=False
    )
].copy()

maior_coletivo = (
    coletivo
    .groupby(id_col)["Percentual"]
    .mean()
    .sort_values(
        ascending=False
    )
)

menor_coletivo = (
    coletivo
    .groupby(id_col)["Percentual"]
    .mean()
    .sort_values()
)

estado_maior = maior_coletivo.index[0]
valor_maior = maior_coletivo.iloc[0]

estado_menor = menor_coletivo.index[0]
valor_menor = menor_coletivo.iloc[0]

print("MAIOR TRANSPORTE COLETIVO")
print(
    f"{estado_maior}: {valor_maior:.2f}%"
)

print("\nMENOR TRANSPORTE COLETIVO")
print(
    f"{estado_menor}: {valor_menor:.2f}%"
)

display(Markdown(
    f"""
## Estado com mais mulheres utilizando transporte coletivo

O estado com maior percentual é **{estado_maior}**, com **{valor_maior:.2f}%**.

## Estado com menos mulheres utilizando transporte coletivo

O estado com menor percentual é **{estado_menor}**, com **{valor_menor:.2f}%**.
"""
))


municipios = df2[
    ~df2[id_col].isin(
        estados + regioes
    )
].copy()

municipios_long = municipios.melt(
    id_vars=id_col,
    var_name="Variavel",
    value_name="Percentual"
)

municipios_long["Percentual"] = pd.to_numeric(
    municipios_long["Percentual"],
    errors="coerce"
)

municipios_long = municipios_long.dropna(
    subset=["Percentual"]
)


bicicleta = municipios_long[
    municipios_long["Variavel"].str.contains(
        "Bicicleta",
        case=False,
        na=False
    )
].copy()

cidade_bicicleta = (
    bicicleta
    .groupby(id_col)["Percentual"]
    .mean()
    .sort_values(
        ascending=False
    )
)

cidade_maior_bicicleta = cidade_bicicleta.index[0]
valor_bicicleta = cidade_bicicleta.iloc[0]

print("\nCIDADE COM MAIS MULHERES ANDANDO DE BICICLETA")
print(
    f"{cidade_maior_bicicleta}: "
    f"{valor_bicicleta:.2f}%"
)

display(Markdown(
    f"""
## Cidade com mais mulheres andando de bicicleta

A cidade com maior percentual é **{cidade_maior_bicicleta}**, com **{valor_bicicleta:.2f}%**.
"""
))


carro = municipios_long[
    municipios_long["Variavel"].str.contains(
        "Automóvel|Automovel|carro",
        case=False,
        na=False
    )
].copy()

cidade_carro = (
    carro
    .groupby(id_col)["Percentual"]
    .mean()
    .sort_values(
        ascending=False
    )
)

cidade_maior_carro = cidade_carro.index[0]
valor_carro = cidade_carro.iloc[0]

print("\nCIDADE COM MAIS MULHERES UTILIZANDO CARRO")
print(
    f"{cidade_maior_carro}: "
    f"{valor_carro:.2f}%"
)

display(Markdown(
    f"""
## Cidade com mais mulheres utilizando carro

A cidade com maior percentual é **{cidade_maior_carro}**, com **{valor_carro:.2f}%**.
"""
))

print("\n==============================")
print("RESUMO DAS RESPOSTAS")
print("==============================")

print(
    f"1. Mais transporte coletivo: "
    f"{estado_maior} ({valor_maior:.2f}%)"
)

print(
    f"2. Menos transporte coletivo: "
    f"{estado_menor} ({valor_menor:.2f}%)"
)

print(
    f"3. Mais mulheres andando de bicicleta: "
    f"{cidade_maior_bicicleta} ({valor_bicicleta:.2f}%)"
)

print(
    f"4. Mais mulheres utilizando carro: "
    f"{cidade_maior_carro} ({valor_carro:.2f}%)"
)


df_estados.to_excel(
    "estados_BR_GR_UF_MU.xlsx",
    index=False
)

df_long.to_excel(
    "BR_GR_UF_MU_melt.xlsx",
    index=False
)

comparacao.to_excel(
    "comparacao_meios_transporte.xlsx",
    index=False
)

maior_coletivo.to_csv(
    "maior_transporte_coletivo.csv",
    sep=";"
)

menor_coletivo.to_csv(
    "menor_transporte_coletivo.csv",
    sep=";"
)

cidade_bicicleta.to_csv(
    "cidades_bicicleta.csv",
    sep=";"
)

cidade_carro.to_csv(
    "cidades_carro.csv",
    sep=";"
)