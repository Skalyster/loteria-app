import streamlit as st
import random

# ==========================================
# ESTADÍSTICAS CONGELADAS (Extraídas de tu BD)
# ==========================================
DATOS = {
    "Bonoloto": {
        "calientes": [3, 10, 22, 33, 41, 46, 2, 34, 39, 45, 32, 47, 49, 5, 18, 26, 37, 11, 25, 8, 38, 15, 44, 1, 21],
        "frios": [29, 4, 16, 20, 36, 12, 48, 6, 13, 40, 31, 23, 30, 43, 14, 42, 9, 28, 7, 35, 17, 24, 19, 27, 45]
    },
    "Eurodreams": {
        "calientes": [21, 22, 24, 23, 3, 8, 37, 19, 30, 4, 15, 25, 29, 11, 17, 20, 38, 26, 27, 9, 16, 5, 33, 39, 36],
        "frios": [13, 31, 2, 10, 1, 6, 40, 14, 34, 18, 35, 28, 7, 32, 12, 21, 15, 20, 19, 26, 25, 37, 38, 9, 11]
    },
    "Lotería Nacional": {
        # Terminaciones de 2 cifras más premiadas extraídas de tu histórico
        "terminaciones_calientes": ["84", "22", "20", "97", "44", "08", "33", "70", "47", "80", "05", "11", "14", "10", "19"]
    }
}

# ==========================================
# CONFIGURACIÓN MÓVIL
# ==========================================
st.set_page_config(page_title="Generador Lotto", page_icon="📱", layout="centered")

st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>📱 Generador Lotto</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-top: 0px;'>Tus apuestas inteligentes al instante</p>", unsafe_allow_html=True)

juego = st.selectbox("Elige juego:", ["Bonoloto", "Eurodreams", "Lotería Nacional"])

# Solo mostramos la estrategia si no es Lotería Nacional
if juego != "Lotería Nacional":
    estrategia = st.selectbox("Estrategia:", ["🔥 Caliente", "❄️ Mixta (3 Calientes / 3 Fríos)"])
else:
    estrategia = "N/A" # En Lotería Nacional siempre usamos terminaciones calientes

# ==========================================
# MOTOR DE GENERACIÓN
# ==========================================
def generar(juego, estrategia):
    apuestas = []
    
    if juego == "Lotería Nacional":
        terminaciones = DATOS[juego]["terminaciones_calientes"]
        for _ in range(5):
            # Elegimos una terminación caliente de 2 cifras
            term = random.choice(terminaciones)
            # Generamos las 3 primeras cifras al azar (000 al 999)
            inicio = random.randint(0, 999)
            numero = f"{inicio:03d}{term}"
            apuestas.append(numero)
        return apuestas
        
    # Lógica para Bonoloto y Eurodreams
    datos = DATOS[juego]
    max_num = 49 if juego == "Bonoloto" else 40
    
    for _ in range(5):
        if estrategia == "🔥 Caliente":
            nums = random.choices(range(1, max_num + 1), 
                                 weights=[3 if n in datos["calientes"] else 1 for n in range(1, max_num + 1)], 
                                 k=6)
            comb = list(set(nums))
            while len(comb) < 6:
                nuevo = random.randint(1, max_num)
                if nuevo not in comb: comb.append(nuevo)
        else:
            comb = random.sample(datos["calientes"], 3) + random.sample(datos["frios"], 3)
            
        comb.sort()
        extra = random.randint(0, 9) if juego == "Bonoloto" else random.randint(1, 5)
        apuestas.append((comb, extra))
        
    return apuestas

# ==========================================
# INTERFAZ DE RESULTADOS (MÓVIL)
# ==========================================
if st.button("🎰 GENERAR 5 APUESTAS", use_container_width=True):
    res = generar(juego, estrategia)
    
    st.write("---")
    
    if juego == "Lotería Nacional":
        # Diseño de tarjetas planas para Lotería Nacional
        html = "<div style='display: flex; flex-direction: column; gap: 12px; align-items: center;'>"
        for i, num in enumerate(res):
            html += f"<div style='background: #f9f9f9; border-left: 5px solid #ff7f0e; padding: 12px 20px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); width: 80%; text-align: center;'>"
            html += f"<b style='color: #555; font-size: 12px;'>Apuesta {i+1}</b><br>"
            html += f"<span style='font-size: 28px; font-weight: bold; color: #333; letter-spacing: 3px;'>{num}</span>"
            html += f"</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
        
    else:
        # Diseño de bolas para Bonoloto y Eurodreams
        cp = "#1f77b4" if juego == "Bonoloto" else "#2ca02c"
        ce = "#d62728" if juego == "Bonoloto" else "#ff7f0e"
        txt = "R" if juego == "Bonoloto" else "E"
        
        html = "<div style='display: flex; flex-direction: column; gap: 15px;'>"
        for i, (nums, extra) in enumerate(res):
            html += f"<div style='display: flex; align-items: center; gap: 8px; justify-content: center;'>"
            html += f"<b style='width: 50px; color: #555;'>Ap {i+1}</b>"
            for n in nums:
                html += f"<span style='display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; border-radius: 50%; color: white; font-weight: bold; background-color: {cp}; box-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>{n}</span>"
            html += f"<span style='display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 50%; color: white; font-weight: bold; background-color: {ce}; box-shadow: 1px 1px 3px rgba(0,0,0,0.3); margin-left: 8px;'>{txt}:{extra}</span>"
            html += "</div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)