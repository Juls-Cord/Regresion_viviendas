import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def calcular_regresion(superficies, precios):
    """Calcula pendiente, intercepto, estimaciones y R²."""

    promedio_x = sum(superficies) / len(superficies)
    promedio_y = sum(precios) / len(precios)

    suma_xx = sum(
        (x - promedio_x) ** 2
        for x in superficies
    )

    suma_xy = sum(
        (x - promedio_x) * (y - promedio_y)
        for x, y in zip(superficies, precios)
    )

    pendiente = suma_xy / suma_xx
    intercepto = promedio_y - pendiente * promedio_x

    precios_estimados = [
        intercepto + pendiente * x
        for x in superficies
    ]

    suma_errores_cuadrados = sum(
        (precio_real - precio_estimado) ** 2
        for precio_real, precio_estimado
        in zip(precios, precios_estimados)
    )

    variacion_total = sum(
        (precio_real - promedio_y) ** 2
        for precio_real in precios
    )

    r_cuadrado = 1 - (
        suma_errores_cuadrados / variacion_total
    )

    return pendiente, intercepto, precios_estimados, r_cuadrado


st.title("Estimación del precio de viviendas")

st.write(
    "Aplicación didáctica de regresión lineal simple "
    "con datos simulados."
)

st.caption(
    "Los precios están expresados en miles de soles. "
    "Por ejemplo, 163 representa S/ 163,000."
)

datos_iniciales = pd.DataFrame({
    "superficie_m2": [50, 60, 70, 80, 90, 100, 110, 120],
    "precio_miles_soles": [163, 208, 216, 265, 262, 307, 320, 359]
})

st.subheader("Datos de las viviendas")

datos = st.data_editor(
    datos_iniciales,
    num_rows="dynamic",
    key="tabla_viviendas"
)

superficies_columna = pd.to_numeric(
    datos["superficie_m2"],
    errors="coerce"
)

precios_columna = pd.to_numeric(
    datos["precio_miles_soles"],
    errors="coerce"
)

filas_validas = (
    superficies_columna.notna()
    & precios_columna.notna()
    & (superficies_columna > 0)
    & (precios_columna > 0)
)

superficies = superficies_columna[filas_validas].tolist()
precios = precios_columna[filas_validas].tolist()

filas_ignoradas = len(datos) - len(superficies)

if filas_ignoradas > 0:
    st.info(
        f"Se ignoraron {filas_ignoradas} fila(s) "
        "vacías o con valores no válidos."
    )

if len(superficies) < 2:
    st.warning(
        "Ingresa al menos dos viviendas con superficie "
        "y precio válidos."
    )
    st.stop()

if len(set(superficies)) < 2:
    st.warning(
        "Las superficies deben incluir al menos "
        "dos valores distintos."
    )
    st.stop()

if len(set(precios)) < 2:
    st.warning(
        "Los precios deben tener variación para calcular R²."
    )
    st.stop()

pendiente, intercepto, precios_estimados, r_cuadrado = (
    calcular_regresion(superficies, precios)
)

st.subheader("Resultados de la regresión")

st.write(
    f"**Ecuación:** ŷ = {intercepto:.4f} "
    f"+ {pendiente:.4f} × superficie"
)

st.write(
    f"**Pendiente:** {pendiente:.4f} "
    "miles de soles por m²"
)

st.write(
    f"**Intercepto:** {intercepto:.4f} "
    "miles de soles"
)

st.write(
    f"**R²:** {r_cuadrado:.4f} "
    f"({r_cuadrado:.2%})"
)

st.subheader("Estimar el precio de una vivienda")

superficie_consultada = st.number_input(
    "Ingresa la superficie en m²",
    min_value=1.0,
    value=75.0,
    step=1.0
)

precio_estimado = (
    intercepto + pendiente * superficie_consultada
)

st.metric(
    "Precio estimado",
    f"S/ {precio_estimado * 1000:,.0f}"
)

if (
    superficie_consultada < min(superficies)
    or superficie_consultada > max(superficies)
):
    st.warning(
        "La superficie está fuera del rango de la tabla. "
        "La estimación podría ser menos confiable."
    )

st.subheader("Gráfico de la regresión")

datos_ordenados = sorted(
    zip(superficies, precios),
    key=lambda fila: fila[0]
)

superficies_ordenadas = [
    fila[0] for fila in datos_ordenados
]

precios_ordenados = [
    fila[1] for fila in datos_ordenados
]

precios_recta = [
    intercepto + pendiente * superficie
    for superficie in superficies_ordenadas
]

figura, eje = plt.subplots()

eje.scatter(
    superficies,
    precios,
    label="Viviendas simuladas"
)

eje.plot(
    superficies_ordenadas,
    precios_recta,
    color="red",
    label="Recta de regresión"
)

eje.set_xlabel("Superficie (m²)")
eje.set_ylabel("Precio (miles de soles)")
eje.set_title("Relación entre superficie y precio")
eje.legend()
eje.grid(True)

st.pyplot(figura)