import streamlit as st
import random

# ==========================================
# ESTADÍSTICAS CONGELADAS (Extraídas de tu BD)
# ==========================================
# Top 25 números más calientes y más fríos
DATOS = {
    "Bonoloto": {
        "max": 49,
        "calientes": [3, 10, 22, 33, 41, 46, 2, 34, 39, 45, 32, 47, 49, 5, 18, 26, 37, 11, 25, 8, 38, 15, 44, 1, 21],
        "frios": [29, 4, 16, 20, 36, 12, 48, 6, 13, 40, 31, 23, 30, 43, 14, 42, 9, 28, 7, 35, 17, 24, 19, 27, 45]
    },
    "Eurodreams": {
        "max": 40,
        "calientes": [21, 22, 24, 23, 3, 8, 37, 19, 30, 4, 15, 25, 29, 11, 17, 20, 38, 26, 27, 9, 16, 5, 33, 39, 36],
        "frios": [13, 31, 2, 10, 1, 6, 40, 14, 34, 18, 35, 28, 7, 32, 12, 21, 15, 20, 19, 26, 25, 37, 38, 9, 11]
    }
}

# ==========================================
# CONFIGURACIÓN MÓVIL
# ==========================================
st.set_page_config(page_title="Generador Lotto", page_icon="📱", layout="centered")

st.markdown("<h1 style='text-align: center; margin-bottom: 5px;'>📱 Generador Lotto</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; margin-top: 0px;'>Tus apuestas inteligentes al instante</p>", unsafe_allow_html=True)

juego = st.selectbox("Elige juego:", ["Bonoloto", "Eurodreams"])
estrategia = st.selectbox("Estrategia:", ["🔥 Caliente", "❄️ Mixta (3 Calientes / 3 Fríos)"])

# ==========================================
# MOTOR DE GENERACIÓN
# ==========================================
def generar(juego, estrategia):
    datos = DATOS[juego]
    apuestas = []
    
    for _ in range(5):
        if estrategia == "🔥 Caliente":
            # Priorizamos los calientes pero damos una mínima opción al resto
            nums = random.choices(range(1, datos["max"] + 1), 
                                 weights=[3 if n in datos["calientes"] else 1 for n in range(1, datos["max"] + 1)], 
                                 k=6)
            comb = list(set(nums))
            while len(comb) < 6:
                nuevo = random.randint(1, datos["max"])
                if nuevo not in comb: comb.append(nuevo)
        else:
            # 3 calientes y 3 fríos exactos
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
    
    # Colores
    cp = "#1f77b4" if juego == "Bonoloto" else "#2ca02c"
    ce = "#d62728" if juego == "Bonoloto" else "#ff7f0e"
    txt = "R" if juego == "Bonoloto" else "E"
    
    st.write("---")
    
    # Mostrar apuestas formato móvil
    html = "<div style='display: flex; flex-direction: column; gap: 15px;'>"
    for i, (nums, extra) in enumerate(res):
        html += f"<div style='display: flex; align-items: center; gap: 10px; justify-content: center;'>"
        html += f"<b style='width: 60px; color: #555;'>Ap {i+1}</b>"
        for n in nums:
            html += f"<span style='display: inline-flex; align-items: center; justify-content: center; width: 38px; height: 38px; border-radius: 50%; color: white; font-weight: bold; background-color: {cp}; box-shadow: 1px 1px 3px rgba(0,0,0,0.3);'>{n}</span>"
        html += f"<span style='display: inline-flex; align-items: center; justify-content: center; width: 32px; height: 32px; border-radius: 50%; color: white; font-weight: bold; background-color: {ce}; box-shadow: 1px 1px 3px rgba(0,0,0,0.3); margin-left: 8px;'>{txt}:{extra}</span>"
        html += "</div>"
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)