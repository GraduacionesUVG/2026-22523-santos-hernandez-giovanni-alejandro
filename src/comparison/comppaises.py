import pandas as pd

df = pd.read_csv("TROPOMI_GHSSMOD_ANNUAL1.csv")

df["NO2_VCD"] = pd.to_numeric(df["NO2_VCD"], errors="coerce")
df["year"] = pd.to_numeric(df["year"], errors="coerce")

df = df.loc[df["year"].between(2019, 2024)].dropna(subset=["NO2_VCD"])

referencia_mol_m2 = 3.02e-5
factor_conversion = 6.02214076e19 / 1e15
referencia = referencia_mol_m2 * factor_conversion

tolerancia = 0.10
limite_inferior = referencia * (1 - tolerancia)
limite_superior = referencia * (1 + tolerancia)

resumen = (
    df.groupby("ID_UC_G0", as_index=False)
    .agg(
        city=("city", "first"),
        country=("country", "first"),
        NO2_VCD=("NO2_VCD", "mean"),
        anios_disponibles=("year", "nunique"),
    )
)

resultados = resumen.loc[
    resumen["NO2_VCD"].between(limite_inferior, limite_superior)
    & resumen["anios_disponibles"].eq(6)
].copy()

resultados["NO2_mol_m2"] = resultados["NO2_VCD"] / factor_conversion
resultados["diferencia_pct"] = (
    (resultados["NO2_VCD"] / referencia - 1) * 100
)

resultados = resultados.sort_values(
    "diferencia_pct", key=lambda columna: columna.abs()
)
ciudades = resultados["city"].astype("string").str.strip()

resultados = resultados.loc[
    ciudades.notna()
    & ~ciudades.str.lower().isin(["none", "nan", "null", ""])
].copy()

print(f"Referencia escalada: {referencia:.4f}")
print(f"Rango: {limite_inferior:.4f}–{limite_superior:.4f}")
print(f"Áreas urbanas encontradas: {len(resultados)}")
print(resultados.to_string(index=False))

