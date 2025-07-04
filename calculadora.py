import streamlit as st

def calcular_bancas(porcentajes_fuerzas, total_bancas):
    suma_principales = sum(porcentajes_fuerzas)
    porcentaje_restante = 100 - suma_principales

    votos_validos = 100000
    votos_fuerzas = [votos_validos * (p / 100) for p in porcentajes_fuerzas]

    cuociente_electoral = votos_validos / total_bancas

    bancas_por_cociente = []
    residuos = []
    for votos in votos_fuerzas:
        if votos >= cuociente_electoral:
            bancas = int(votos // cuociente_electoral)
            residuo = votos % cuociente_electoral
        else:
            bancas = 0
            residuo = -1
        bancas_por_cociente.append(bancas)
        residuos.append(residuo)

    bancas_asignadas = sum(bancas_por_cociente)
    bancas_restantes = total_bancas - bancas_asignadas

    while bancas_restantes > 0:
        max_residuo = max(residuos)
        if max_residuo <= -1:
            break
        max_idx = residuos.index(max_residuo)
        bancas_por_cociente[max_idx] += 1
        residuos[max_idx] = -1
        bancas_restantes -= 1

    if bancas_restantes > 0:
        max_votos_idx = votos_fuerzas.index(max(votos_fuerzas))
        bancas_por_cociente[max_votos_idx] += bancas_restantes

    return bancas_por_cociente, porcentaje_restante

# Streamlit App
st.title("🗳️ Calculadora de bancas legislativas - La Plata / https://x.com/iterAR_eco'" )

st.write("Ingresá los porcentajes de votos de las fuerzas. El cálculo se hace según la Ley Electoral para concejales (12 bancas) y diputados (6 bancas).")

num_fuerzas = st.number_input("¿Cuántas fuerzas querés cargar?", min_value=2, max_value=10, value=3)

porcentajes_fuerzas = []
for i in range(num_fuerzas):
    porcentaje = st.number_input(f"Porcentaje de votos de la fuerza {i+1} (%)", min_value=0.0, max_value=100.0, step=0.1)
    porcentajes_fuerzas.append(porcentaje)

suma_porcentajes = sum(porcentajes_fuerzas)
if suma_porcentajes > 100:
    st.error(f"La suma de los porcentajes ({suma_porcentajes:.2f}%) supera el 100%. Corregilo para continuar.")
else:
    if st.button("Calcular bancas"):
        # Concejales
        bancas_concejales, restante_concejales = calcular_bancas(porcentajes_fuerzas, 12)
        st.subheader("🔹 Concejales (12 bancas)")
        for idx, (p, b) in enumerate(zip(porcentajes_fuerzas, bancas_concejales), 1):
            st.write(f"Fuerza {idx}: {p:.2f}% votos - {b} bancas")
        st.write(f"Porcentaje de otras fuerzas sin bancas: {restante_concejales:.2f}%")

        # Diputados
        bancas_diputados, restante_diputados = calcular_bancas(porcentajes_fuerzas, 6)
        st.subheader("🔹 Diputados (6 bancas)")
        for idx, (p, b) in enumerate(zip(porcentajes_fuerzas, bancas_diputados), 1):
            st.write(f"Fuerza {idx}: {p:.2f}% votos - {b} bancas")
        st.write(f"Porcentaje de otras fuerzas sin bancas: {restante_diputados:.2f}%")
