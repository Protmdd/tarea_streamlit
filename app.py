"""
Dashboard de Ventas - Bodega El Porvenir
Estudiante: Luis Atto
Curso: Programacion Avanzada para la Ciencia de Datos
Fecha: Mayo 2025
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

st.set_page_config(
    page_title="Bodega El Porvenir - Ventas 2024",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .header-box {
        background: linear-gradient(135deg, #1a3a2a 0%, #2d6a4f 100%);
        padding: 2rem 2.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .header-box h1 { margin: 0; font-size: 1.8rem; }
    .header-box p  { margin: 0.3rem 0 0; opacity: 0.85; font-size: 0.9rem; }
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.07);
        border-left: 4px solid #2d6a4f;
        margin-bottom: 1rem;
    }
    .metric-card h3 { margin: 0; font-size: 0.75rem; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; }
    .metric-card p  { margin: 0.3rem 0 0; font-size: 1.6rem; font-weight: 700; color: #1a3a2a; }
    .footer {
        text-align: center;
        color: #9ca3af;
        font-size: 0.78rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>Bodega El Porvenir - Dashboard de Ventas 2024</h1>
    <p>
        <strong>Estudiante:</strong> Luis Atto &nbsp;|&nbsp;
        <strong>Curso:</strong> Programacion Avanzada para la Ciencia de Datos &nbsp;|&nbsp;
        <strong>Fecha:</strong> Mayo 2025 &nbsp;|&nbsp;
        <strong>Descripcion:</strong> Analisis de ventas de una bodega local en Miraflores, Lima, durante el primer semestre de 2024.
    </p>
</div>
""", unsafe_allow_html=True)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "datos.csv")

@st.cache_data
def cargar_datos(path):
    df = pd.read_csv(path, parse_dates=["fecha"])
    df["mes"] = df["fecha"].dt.strftime("%b %Y")
    df["mes_num"] = df["fecha"].dt.to_period("M")
    return df

df = cargar_datos(DATA_PATH)

with st.sidebar:
    st.markdown("## Filtros")

    categorias = sorted(df["categoria"].unique())
    cats_sel = st.multiselect(
        "Categoria de producto",
        options=categorias,
        default=categorias
    )

    vendedores = ["Todos"] + sorted(df["vendedor"].unique())
    vend_sel = st.selectbox("Vendedor", options=vendedores)

    min_total = int(df["total"].min())
    max_total = int(df["total"].max())
    rango_total = st.slider(
        "Rango de total (S/.)",
        min_value=min_total,
        max_value=max_total,
        value=(min_total, max_total),
        step=5
    )

    busqueda = st.text_input("Buscar producto", placeholder="Ej: Coca-Cola, Arroz...")

    if st.button("Reiniciar filtros"):
        st.rerun()

    st.markdown("---")
    st.caption("Registros: enero - junio 2024 | Miraflores, Lima")

df_f = df.copy()
if cats_sel:
    df_f = df_f[df_f["categoria"].isin(cats_sel)]
if vend_sel != "Todos":
    df_f = df_f[df_f["vendedor"] == vend_sel]
df_f = df_f[(df_f["total"] >= rango_total[0]) & (df_f["total"] <= rango_total[1])]
if busqueda.strip():
    df_f = df_f[df_f["producto"].str.contains(busqueda.strip(), case=False, na=False)]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><h3>Total ventas (S/.)</h3><p>S/. {df_f["total"].sum():,.2f}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><h3>Registros</h3><p>{len(df_f)}</p></div>', unsafe_allow_html=True)
with col3:
    prod_top = df_f.groupby("producto")["total"].sum().idxmax() if not df_f.empty else "-"
    st.markdown(f'<div class="metric-card"><h3>Producto top</h3><p style="font-size:1rem">{prod_top}</p></div>', unsafe_allow_html=True)
with col4:
    ticket = df_f["total"].mean() if not df_f.empty else 0
    st.markdown(f'<div class="metric-card"><h3>Ticket promedio</h3><p>S/. {ticket:,.2f}</p></div>', unsafe_allow_html=True)

with st.expander("Ver tabla de datos", expanded=False):
    cols_mostrar = ["fecha", "producto", "categoria", "cantidad", "precio_unitario", "total", "vendedor"]
    st.dataframe(
        df_f[cols_mostrar].rename(columns={
            "fecha": "Fecha",
            "producto": "Producto",
            "categoria": "Categoria",
            "cantidad": "Cantidad",
            "precio_unitario": "Precio unit. (S/.)",
            "total": "Total (S/.)",
            "vendedor": "Vendedor"
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Mostrando {len(df_f)} de {len(df)} registros.")

st.divider()

VERDE  = "#2d6a4f"
VERDE2 = "#52b788"
CREMA  = "#f7f3ee"
PALETA = ["#1a3a2a", "#2d6a4f", "#52b788", "#95d5b2", "#b7e4c7", "#d8f3dc"]

if df_f.empty:
    st.warning("No hay datos para los filtros seleccionados.")
else:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("Ventas por categoria")
        cat_totales = df_f.groupby("categoria")["total"].sum().sort_values(ascending=True)
        fig1, ax1 = plt.subplots(figsize=(6, 4))
        fig1.patch.set_facecolor(CREMA)
        ax1.set_facecolor(CREMA)
        bars = ax1.barh(cat_totales.index, cat_totales.values, color=VERDE, height=0.5)
        ax1.bar_label(bars, fmt="S/. %.0f", padding=4, fontsize=9, color="#1a3a2a")
        ax1.set_xlabel("Total (S/.)", color="#4b5563")
        ax1.tick_params(colors="#4b5563")
        ax1.spines[["top", "right", "left"]].set_visible(False)
        ax1.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"S/. {x:,.0f}"))
        st.pyplot(fig1, use_container_width=True)

    with col_b:
        st.subheader("Participacion por categoria")
        cat_part = df_f.groupby("categoria")["total"].sum()
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        fig2.patch.set_facecolor(CREMA)
        wedges, texts, autotexts = ax2.pie(
            cat_part.values,
            labels=cat_part.index,
            autopct="%1.1f%%",
            colors=PALETA[:len(cat_part)],
            startangle=140,
            wedgeprops={"linewidth": 1.5, "edgecolor": "white"}
        )
        for at in autotexts:
            at.set_fontsize(9)
            at.set_color("white")
        st.pyplot(fig2, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.subheader("Tendencia mensual de ventas")
        mensual = df_f.groupby("mes_num")["total"].sum().reset_index().sort_values("mes_num")
        mensual["mes_label"] = mensual["mes_num"].dt.strftime("%b %Y")
        fig3, ax3 = plt.subplots(figsize=(6, 4))
        fig3.patch.set_facecolor(CREMA)
        ax3.set_facecolor(CREMA)
        ax3.plot(mensual["mes_label"], mensual["total"],
                 marker="o", color=VERDE, linewidth=2.5,
                 markersize=7, markerfacecolor=VERDE2)
        ax3.fill_between(range(len(mensual)), mensual["total"], alpha=0.1, color=VERDE)
        ax3.set_xlabel("Mes", color="#4b5563")
        ax3.set_ylabel("Total (S/.)", color="#4b5563")
        ax3.tick_params(colors="#4b5563", axis="x", rotation=25)
        ax3.spines[["top", "right"]].set_visible(False)
        ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"S/. {x:,.0f}"))
        ax3.set_xticks(range(len(mensual)))
        ax3.set_xticklabels(mensual["mes_label"])
        st.pyplot(fig3, use_container_width=True)

    with col_d:
        st.subheader("Cantidad vendida vs. Total")
        cat_colores = {c: PALETA[i % len(PALETA)] for i, c in enumerate(sorted(df_f["categoria"].unique()))}
        fig4, ax4 = plt.subplots(figsize=(6, 4))
        fig4.patch.set_facecolor(CREMA)
        ax4.set_facecolor(CREMA)
        for cat, grupo in df_f.groupby("categoria"):
            ax4.scatter(grupo["cantidad"], grupo["total"],
                        color=cat_colores.get(cat, VERDE),
                        alpha=0.75, s=70, label=cat,
                        edgecolors="white", linewidths=0.5)
        ax4.set_xlabel("Cantidad vendida", color="#4b5563")
        ax4.set_ylabel("Total (S/.)", color="#4b5563")
        ax4.spines[["top", "right"]].set_visible(False)
        ax4.tick_params(colors="#4b5563")
        ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"S/. {x:,.0f}"))
        ax4.legend(fontsize=8, frameon=False)
        st.pyplot(fig4, use_container_width=True)

    st.subheader("Ventas por vendedor")
    vend_total = df_f.groupby("vendedor")["total"].sum().sort_values(ascending=False)
    fig5, ax5 = plt.subplots(figsize=(10, 3.5))
    fig5.patch.set_facecolor(CREMA)
    ax5.set_facecolor(CREMA)
    bars5 = ax5.bar(vend_total.index, vend_total.values,
                    color=PALETA[:len(vend_total)], width=0.45)
    ax5.bar_label(bars5, fmt="S/. %.0f", padding=4, fontsize=10, color="#1a3a2a")
    ax5.set_ylabel("Total (S/.)", color="#4b5563")
    ax5.tick_params(colors="#4b5563")
    ax5.spines[["top", "right", "left"]].set_visible(False)
    ax5.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"S/. {x:,.0f}"))
    st.pyplot(fig5, use_container_width=True)

st.markdown("""
<div class="footer">
    Bodega El Porvenir | Miraflores, Lima | Tarea Streamlit en Linux/WSL
</div>
""", unsafe_allow_html=True)
