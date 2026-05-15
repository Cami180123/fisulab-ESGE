import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Fisulab — Trazabilidad",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
/* ── Reset general: fondo claro, texto siempre oscuro ── */
.stApp { background-color: #f5f7fa !important; }
.stApp *, .stMarkdown, .stMarkdown *,
.element-container, .element-container *,
[data-testid="stVerticalBlock"] * {
    color: #1a1a2e !important;
}
/* Excepciones: badges y headers blancos */
.badge, .sh, .pac-hdr *, .mc-lbl,
.etapa-pill, .ib-lbl { color: inherit !important; }

h1,h2,h3,h4 { color: #0B3D91 !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0B3D91 0%,#1A7A3C 100%) !important;
}
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span { color: #e8f4ff !important; }

/* ── Tarjeta paciente ── */
.pac-card {
    background: white; border-radius: 10px;
    padding: 11px 14px; margin-bottom: 7px;
    border-left: 5px solid #0B3D91;
    box-shadow: 0 1px 5px rgba(0,0,0,0.07);
}
.pac-card.alta     { border-left-color:#1A7A3C; }
.pac-card.remitido { border-left-color:#E07B00; }
.pac-card.pendiente{ border-left-color:#C62828; }
.pac-card.abandono { border-left-color:#6A0DAD; }
.pac-nombre { font-size:13px; font-weight:700; color:#0B3D91 !important; }
.pac-sub    { font-size:11px; color:#555 !important; margin-top:2px; }
.pac-tags   { margin-top:5px; display:flex; gap:5px; flex-wrap:wrap; }
.pac-next   { font-size:11px; color:#6A0DAD !important; margin-top:4px; font-weight:600; }

/* ── Badges ── */
.badge { display:inline-block; border-radius:20px;
         padding:2px 9px; font-size:11px; font-weight:600; }
.b-azul   { background:#E3F2FD !important; color:#0B3D91 !important; border:1px solid #90CAF9; }
.b-verde  { background:#E8F5E9 !important; color:#1A7A3C !important; border:1px solid #A5D6A7; }
.b-naranja{ background:#FFF3E0 !important; color:#BF6000 !important; border:1px solid #FFCC80; }
.b-rojo   { background:#FCE4EC !important; color:#C62828 !important; border:1px solid #EF9A9A; }
.b-morado { background:#F3E5F5 !important; color:#6A0DAD !important; border:1px solid #CE93D8; }
.b-gris   { background:#F5F5F5 !important; color:#444    !important; border:1px solid #ccc; }

/* ── Header paciente ── */
.pac-hdr {
    background: linear-gradient(135deg,#0B3D91 0%,#1A7A3C 100%);
    border-radius:14px; padding:20px 26px; margin-bottom:14px;
}
.pac-hdr-nombre { font-size:22px; font-weight:800; color:white !important; margin-bottom:5px; }
.pac-hdr-sub    { font-size:12px; color:rgba(255,255,255,0.88) !important; line-height:2; }
.etapa-pill {
    display:inline-block; background:rgba(255,255,255,0.2);
    border:1px solid rgba(255,255,255,0.45);
    color:white !important; border-radius:20px;
    padding:3px 12px; font-size:12px; font-weight:600; margin-top:7px;
}

/* ── Barra info ── */
.info-bar {
    background:white; border-radius:10px;
    padding:13px 18px; margin-bottom:12px;
    box-shadow:0 1px 6px rgba(0,0,0,0.07);
    display:flex; gap:28px; flex-wrap:wrap; align-items:center;
}
.ib-lbl { font-size:11px; color:#888 !important; font-weight:600;
           text-transform:uppercase; letter-spacing:0.3px; }
.ib-val { font-size:14px; font-weight:700; color:#0B3D91 !important; margin-top:2px; }
.ib-val.m { color:#6A0DAD !important; }
.ib-sub { font-size:11px; color:#666 !important; margin-top:1px; }

/* ── Métricas ── */
.mc { background:white; border-radius:10px; padding:12px 15px;
      border-left:5px solid #0B3D91; box-shadow:0 1px 5px rgba(0,0,0,0.07);
      margin-bottom:8px; }
.mc.v { border-left-color:#1A7A3C; }
.mc.n { border-left-color:#E07B00; }
.mc.m { border-left-color:#6A0DAD; }
.mc-lbl { font-size:11px; color:#777 !important; font-weight:600;
          text-transform:uppercase; letter-spacing:0.3px; }
.mc-val { font-size:16px; font-weight:800; color:#0B3D91 !important; margin-top:3px; }
.mc-val.v { color:#1A7A3C !important; }
.mc-val.n { color:#E07B00 !important; }
.mc-val.m { color:#6A0DAD !important; }

/* ── Secciones ── */
.sh { padding:7px 13px; border-radius:8px 8px 0 0;
      font-weight:700; font-size:13px; margin-top:10px; }
.sh * { color:white !important; }
.sh.b { background:linear-gradient(90deg,#0B3D91,#1565C0); color:white !important; }
.sh.v { background:linear-gradient(90deg,#1A7A3C,#2E7D32); color:white !important; }
.sh.m { background:linear-gradient(90deg,#6A0DAD,#7B1FA2); color:white !important; }
.sh.n { background:linear-gradient(90deg,#BF360C,#D84315); color:white !important; }
.sh.c { background:linear-gradient(90deg,#006064,#00838F); color:white !important; }
.sh.g { background:linear-gradient(90deg,#37474F,#546E7A); color:white !important; }
.sb { background:white; border:1px solid #e0e0e0; border-top:none;
      border-radius:0 0 8px 8px; padding:13px; margin-bottom:6px; }

/* ── Campos dato ── */
.dl { font-size:11px; color:#888 !important; font-weight:600;
      text-transform:uppercase; letter-spacing:0.3px; }
.dv { font-size:13px; color:#222 !important; font-weight:500;
      margin-top:1px; margin-bottom:9px; line-height:1.5; }
.dv.e { color:#bbb !important; font-style:italic; }

/* ── Timeline ── */
.tl { display:flex; gap:11px; margin-bottom:9px; }
.tdot { width:11px; height:11px; border-radius:50%;
        margin-top:4px; flex-shrink:0; }
.tbox { background:white; border-radius:8px; padding:9px 13px;
        flex:1; box-shadow:0 1px 4px rgba(0,0,0,0.06); }
.tdate { font-size:11px; color:#888 !important; font-weight:600; }
.ttit  { font-weight:700; margin:2px 0 1px; font-size:13px; }

/* ── Chip historial ── */
.chip-consulta {
    background:#EEF2FF; border-radius:8px; padding:10px 14px;
    margin-bottom:8px; border-left:4px solid #0B3D91;
    font-size:12px; color:#222 !important;
}
.chip-consulta.activa { border-left-color:#1A7A3C; background:#F0FFF4; }

/* ── Sidebar logo ── */
.logo-t { font-size:20px; font-weight:800; color:white !important;
           text-align:center; padding:8px 0 2px; }
.logo-s { font-size:11px; color:#b0d4ff !important; text-align:center; margin-bottom:16px; }
</style>
""", unsafe_allow_html=True)

# ── Cargar datos ──────────────────────────────────────────────────
@st.cache_data
def cargar():
    base = Path(__file__).parent
    df = pd.read_excel(base / "Fisulab_BD_500pacientes_v3.xlsx",
                       sheet_name="Pacientes_Fisulab", header=1)
    df.columns = df.columns.str.strip()
    df = df.fillna("")

    hist = pd.read_excel(base / "Fisulab_Historial_Consultas_v3.xlsx", header=0)
    hist.columns = hist.columns.str.strip()
    hist = hist.fillna("")
    return df, hist

df, hist = cargar()

def v(p, col):
    val = str(p.get(col,"")).strip()
    return val if val and val.lower() != "nan" else "—"

def badge_estado(estado):
    cls = {"En tratamiento":"b-azul","Alta":"b-verde",
           "Remitido":"b-naranja","Pendiente":"b-rojo",
           "Abandono":"b-morado"}.get(estado,"b-gris")
    return f'<span class="badge {cls}">{estado}</span>'

def card_cls(estado):
    return {"Alta":"alta","Remitido":"remitido",
            "Pendiente":"pendiente","Abandono":"abandono"}.get(estado,"")

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="logo-t">🏥 Fisulab</div>', unsafe_allow_html=True)
    st.markdown('<div class="logo-s">Trazabilidad Clínica</div>', unsafe_allow_html=True)
    st.markdown("---")
    busqueda = st.text_input("🔍 Nombre o N° identificación", placeholder="Buscar…")
    st.markdown("**Filtros**")
    f_esp    = st.selectbox("Especialidad", ["Todas"] + sorted(df["Especialidad"].unique().tolist()))
    f_grupo  = st.selectbox("Grupo etario",  ["Todos"] + sorted(df["Grupo Etario"].unique().tolist()))
    f_estado = st.selectbox("Estado",        ["Todos"] + sorted(df["Estado al Cierre"].unique().tolist()))
    st.markdown("---")
    st.markdown(f"<small>Base: **{len(df)} pacientes**</small>", unsafe_allow_html=True)

# ── Filtrar ───────────────────────────────────────────────────────
dff = df.copy()
if busqueda.strip():
    mask = (dff["Nombre Paciente"].str.contains(busqueda, case=False, na=False) |
            dff["N° Identificación"].astype(str).str.contains(busqueda, na=False))
    dff = dff[mask]
if f_esp    != "Todas": dff = dff[dff["Especialidad"]     == f_esp]
if f_grupo  != "Todos": dff = dff[dff["Grupo Etario"]     == f_grupo]
if f_estado != "Todos": dff = dff[dff["Estado al Cierre"] == f_estado]

# ══════════════════════════════════════════════════════════════════
col_lista, col_detalle = st.columns([1, 2.2], gap="medium")

# ── LISTA ─────────────────────────────────────────────────────────
with col_lista:
    st.markdown(f"### 👥 Pacientes ({len(dff)})")

    if dff.empty:
        st.info("Sin resultados.")
        selected_id = None
    else:
        nombres = dff["Nombre Paciente"].tolist()
        ids     = dff["ID"].tolist()
        sel_i   = st.selectbox(
            "Seleccionar:",
            range(len(nombres)),
            format_func=lambda i: f"#{ids[i]} — {nombres[i]}"
        )
        selected_id = dff.iloc[sel_i]["ID"]

        # Mostrar solo 5 tarjetas (los primeros 5 del filtro)
        st.markdown(f"<small style='color:#666'>Mostrando 5 de {len(dff)}</small>",
                    unsafe_allow_html=True)
        st.markdown("")

        for _, row in dff.head(5).iterrows():
            nombre = str(row.get("Nombre Paciente","")).strip()
            edad   = str(row.get("Edad","")).strip()
            esp    = str(row.get("Especialidad","")).strip()
            estado = str(row.get("Estado al Cierre","")).strip()
            fprox  = str(row.get("Próxima Cita","")).strip()
            grupo  = str(row.get("Grupo Etario","")).strip()
            pid    = row.get("ID","")
            sel_sty= "outline:2px solid #0B3D91;" if row["ID"]==selected_id else ""
            b_est  = badge_estado(estado)
            fprox_html = (f'<div class="pac-next">📅 Próx: {fprox} · {esp}</div>'
                          if fprox and fprox.lower() not in ["nan","—",""] else "")
            st.markdown(f"""
            <div class="pac-card {card_cls(estado)}" style="{sel_sty}">
                <div class="pac-nombre">#{pid} — {nombre}</div>
                <div class="pac-sub">{grupo} · {edad}</div>
                <div class="pac-tags">
                    <span class="badge b-gris">{esp}</span>{b_est}
                </div>
                {fprox_html}
            </div>""", unsafe_allow_html=True)

# ── DETALLE ───────────────────────────────────────────────────────
with col_detalle:
    if dff.empty or selected_id is None:
        st.markdown("### Selecciona un paciente")
    else:
        p = dff[dff["ID"] == selected_id].iloc[0].to_dict()
        h = hist[hist["ID Paciente"] == selected_id].copy()

        # Ordenar historial por fecha
        def parse_fecha(s):
            for fmt in ["%d/%m/%Y","%Y-%m-%d"]:
                try: return pd.to_datetime(str(s).strip(), format=fmt)
                except: pass
            return pd.NaT
        h["Fecha_dt"] = h["Fecha"].apply(parse_fecha)
        h = h.sort_values("Fecha_dt").reset_index(drop=True)

        # ── Header ───────────────────────────────────────────────
        b_est = badge_estado(v(p,"Estado al Cierre"))
        st.markdown(f"""
        <div class="pac-hdr">
            <div class="pac-hdr-nombre">👤 {v(p,'Nombre Paciente')}</div>
            <div class="pac-hdr-sub">
                📋 ID #{v(p,'ID')} &nbsp;·&nbsp;
                🪪 {v(p,'N° Identificación')} ({v(p,'Tipo ID')}) &nbsp;·&nbsp;
                🎂 {v(p,'Edad')} &nbsp;·&nbsp; {v(p,'Sexo')} &nbsp;·&nbsp; 📍 {v(p,'Ciudad')}
            </div>
            <div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center">
                <span class="badge b-verde" style="font-size:12px;padding:4px 12px">
                    🩺 {v(p,'Especialidad')}</span>
                {b_est}
            </div>
            <div class="etapa-pill">🗓️ {v(p,'Etapa Protocolo LPH')}</div>
        </div>""", unsafe_allow_html=True)

        # ── Métricas ─────────────────────────────────────────────
        m1,m2,m3,m4 = st.columns(4)
        for col_m,lbl,campo,cc in [
            (m1,"Consultas","N° Consultas",""),
            (m2,"1ª Consulta","1ª Consulta","v"),
            (m3,"Última Consulta","Última Consulta","n"),
            (m4,"Próxima Cita","Próxima Cita","m"),
        ]:
            with col_m:
                st.markdown(f"""<div class="mc {cc}">
                    <div class="mc-lbl">{lbl}</div>
                    <div class="mc-val {cc}" style="font-size:14px">{v(p,campo)}</div>
                </div>""", unsafe_allow_html=True)

        # Barra especialidad / próxima cita
        st.markdown(f"""
        <div class="info-bar">
            <div>
                <div class="ib-lbl">Especialidad última consulta</div>
                <div class="ib-val">🩺 {v(p,'Especialidad')}</div>
                <div class="ib-sub">{v(p,'Tipo Consulta')} · {v(p,'Profesional Tratante')}</div>
            </div>
            <div style="border-left:2px solid #eee;padding-left:24px">
                <div class="ib-lbl">Próxima cita</div>
                <div class="ib-val m">📅 {v(p,'Próxima Cita')}</div>
                <div class="ib-sub">{v(p,'Especialidad')} · {v(p,'Sede Fisulab')}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        # ── Tabs ─────────────────────────────────────────────────
        tab1,tab2,tab3,tab4,tab5 = st.tabs([
            "👤 Datos Generales","🩺 Clínico",
            "💊 Tratamiento","📊 Signos Vitales","📈 Evolución"
        ])

        # ── TAB 1: Datos Generales ────────────────────────────────
        with tab1:
            ca,cb = st.columns(2)
            with ca:
                st.markdown('<div class="sh b">🧍 Identificación</div><div class="sb">',
                            unsafe_allow_html=True)
                for lbl,campo in [
                    ("Nombre completo","Nombre Paciente"),("N° Identificación","N° Identificación"),
                    ("Tipo ID","Tipo ID"),("Fecha nacimiento","Fecha Nac."),
                    ("Edad","Edad"),("Grupo etario","Grupo Etario"),
                    ("Sexo","Sexo"),("Estado civil","Estado Civil"),
                    ("Ocupación","Ocupación"),("Escolaridad","Escolaridad"),
                    ("Ciudad","Ciudad"),("Teléfono","Teléfono"),
                ]:
                    val=v(p,campo); e="e" if val=="—" else ""
                    st.markdown(f'<div class="dl">{lbl}</div><div class="dv {e}">{val}</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="sh v">👨‍👩‍👧 Acudiente & Seguro</div><div class="sb">',
                            unsafe_allow_html=True)
                for lbl,campo in [
                    ("Acudiente","Acudiente"),("Parentesco","Parentesco"),
                    ("EPS / Aseguradora","EPS / Aseguradora"),
                    ("Tipo afiliación","Tipo Afiliación"),("Régimen","Régimen"),
                ]:
                    val=v(p,campo); e="e" if val=="—" else ""
                    st.markdown(f'<div class="dl">{lbl}</div><div class="dv {e}">{val}</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="sh m">🔬 Antecedentes</div><div class="sb">',
                            unsafe_allow_html=True)
                for lbl,campo in [
                    ("Personales LPH","Antec. Personales LPH"),
                    ("Familiares","Antec. Familiares"),
                    ("Quirúrgicos","Antec. Quirúrgicos"),
                    ("Alergias","Alergias"),
                    ("Toxicológicos","Antec. Toxicológicos"),
                    ("Gineco-obstétrico","F. Obstétrica"),
                ]:
                    val=v(p,campo); e="e" if val=="—" else ""
                    st.markdown(f'<div class="dl">{lbl}</div><div class="dv {e}">{val}</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ── TAB 2: Clínico ────────────────────────────────────────
        with tab2:
            ca,cb = st.columns(2)
            with ca:
                st.markdown('<div class="sh b">📋 Consulta</div><div class="sb">',
                            unsafe_allow_html=True)
                for lbl,campo in [
                    ("Especialidad","Especialidad"),("Profesional","Profesional Tratante"),
                    ("Sede","Sede Fisulab"),("Tipo consulta","Tipo Consulta"),
                    ("Motivo","Motivo Consulta"),("Etapa protocolo","Etapa Protocolo LPH"),
                ]:
                    val=v(p,campo); e="e" if val=="—" else ""
                    st.markdown(f'<div class="dl">{lbl}</div><div class="dv {e}">{val}</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
            with cb:
                st.markdown('<div class="sh n">🦷 Diagnóstico</div><div class="sb">',
                            unsafe_allow_html=True)
                for lbl,campo in [
                    ("Diagnóstico principal (CIE-10)","Diagnóstico Principal (CIE-10)"),
                    ("Diagnóstico secundario","Dx Secundario"),
                    ("Tipo diagnóstico","Tipo Diagnóstico"),
                    ("Hallazgo genético","Hallazgo Genético"),
                ]:
                    val=v(p,campo); e="e" if val=="—" else ""
                    st.markdown(f'<div class="dl">{lbl}</div><div class="dv {e}">{val}</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            st.markdown('<div class="sh c">🔬 Hallazgos por Especialidad</div><div class="sb">',
                        unsafe_allow_html=True)
            ce1,ce2,ce3 = st.columns(3)
            campos_esp = [
                ("Higiene oral","Higiene Oral"),("Oclusión","Oclusión LPH"),
                ("Piezas afectadas","Piezas Afectadas"),("Tipo parto","Tipo Parto"),
                ("Semanas gestación","Sem. Gestación"),("Peso nacer (g)","Peso Nacer g"),
                ("APGAR","APGAR"),("Lactancia","Lactancia"),("Esquema vac.","Esquema Vac."),
                ("Eval. habla","Evaluación Habla"),("Eval. deglución","Evaluación Deglución"),
                ("Eval. auditiva","Evaluación Auditiva"),("Enfoque terapéutico","Enfoque Terapéutico"),
                ("Riesgo suicida","Riesgo Suicida"),("Frec. sesiones","Frecuencia Sesiones"),
            ]
            alguno = False
            for i,(lbl,campo) in enumerate(campos_esp):
                val=v(p,campo)
                if val!="—":
                    alguno=True
                    with [ce1,ce2,ce3][i%3]:
                        st.markdown(f'<div class="dl">{lbl}</div><div class="dv">{val}</div>',
                                    unsafe_allow_html=True)
            if not alguno:
                st.markdown('<div class="dv e">No aplica para esta especialidad</div>',
                            unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # ── TAB 3: Tratamiento ────────────────────────────────────
        with tab3:
            ca,cb = st.columns(2)
            with ca:
                st.markdown('<div class="sh b">💊 Medicamentos</div><div class="sb">',
                            unsafe_allow_html=True)
                meds_raw=v(p,"Medicamentos")
                if meds_raw!="—":
                    for med in meds_raw.split("|"):
                        med=med.strip()
                        if med:
                            st.markdown(f'<div style="background:#f0f4ff;border-left:3px solid #0B3D91;padding:7px 10px;border-radius:4px;margin-bottom:6px;font-size:12px">💊 {med}</div>',
                                        unsafe_allow_html=True)
                else:
                    st.markdown('<div class="dv e">Sin medicamentos</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="sh v">🔧 Procedimiento</div><div class="sb">',
                            unsafe_allow_html=True)
                proc=v(p,"Procedimiento Realizado"); e="e" if proc=="—" else ""
                st.markdown(f'<div class="dv {e}">🩺 {proc}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            with cb:
                st.markdown('<div class="sh m">🧪 Exámenes</div><div class="sb">',
                            unsafe_allow_html=True)
                for lbl,campo in [("Laboratorios","Laboratorios"),
                                   ("Imagen / Estudio","Imagen / Estudio")]:
                    val=v(p,campo); e="e" if val=="—" else ""
                    st.markdown(f'<div class="dl">{lbl}</div><div class="dv {e}">{val}</div>',
                                unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="sh n">📝 Recomendaciones</div><div class="sb">',
                            unsafe_allow_html=True)
                rec=v(p,"Recomendaciones"); e="e" if rec=="—" else ""
                st.markdown(f'<div class="dv {e}" style="line-height:1.6">{rec}</div>',
                            unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="sh g">🗒️ Observaciones</div><div class="sb">',
                            unsafe_allow_html=True)
                obs=v(p,"Observaciones"); e="e" if obs=="—" else ""
                st.markdown(f'<div class="dv {e}" style="line-height:1.6">{obs}</div>',
                            unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

        # ── TAB 4: Signos Vitales ─────────────────────────────────
        with tab4:
            # Fecha y hora de última toma de signos vitales
            if not h.empty:
                ultima = h.iloc[-1]
                fecha_sv = str(ultima.get("Fecha","")).strip()
                hora_sv  = str(ultima.get("Hora","")).strip()
                st.markdown(f"""
                <div style="background:#E8F5E9;border-radius:8px;padding:8px 14px;
                            margin-bottom:12px;font-size:13px;border-left:4px solid #1A7A3C">
                    🕐 <strong>Últimos signos vitales registrados:</strong>
                    {fecha_sv} a las {hora_sv}
                </div>""", unsafe_allow_html=True)

            sv1,sv2 = st.columns(2)
            sv_c = [
                ("Peso (kg)","Peso kg"),("Talla (cm)","Talla cm"),
                ("IMC","IMC"),("Perímetro cefálico","PC cm"),
                ("Presión arterial","TA mmHg"),("FC (lpm)","FC lpm"),
                ("FR (rpm)","FR rpm"),("Temperatura (°C)","Temp °C"),
                ("SatO₂ (%)","SatO₂ %"),("Estado general","Estado General"),
            ]
            hay=False
            for i,(lbl,campo) in enumerate(sv_c):
                val=v(p,campo)
                if val!="—":
                    hay=True; cc="v" if i%2==0 else ""
                    with (sv1 if i%2==0 else sv2):
                        st.markdown(f'<div class="mc {cc}"><div class="mc-lbl">{lbl}</div><div class="mc-val {cc}" style="font-size:16px">{val}</div></div>',
                                    unsafe_allow_html=True)
            if not hay:
                st.info("Sin signos vitales registrados.")

            # Radar de signos vitales
            if hay:
                sv_num={}
                for lbl,campo in [("FC","FC lpm"),("FR","FR rpm"),
                                   ("Temp","Temp °C"),("SatO₂","SatO₂ %")]:
                    try: sv_num[lbl]=float(str(p.get(campo,"")).strip())
                    except: pass
                if len(sv_num)>=3:
                    st.markdown("**📡 Radar de signos vitales** *(valores numéricos de la última consulta)*")
                    fig=go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=list(sv_num.values()), theta=list(sv_num.keys()),
                        fill='toself', fillcolor='rgba(11,61,145,0.12)',
                        line=dict(color='#0B3D91',width=2), name="Signos vitales"
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True,color="#444",
                                                   tickfont=dict(color="#444"))),
                        showlegend=False, height=280,
                        margin=dict(l=40,r=40,t=20,b=20),
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color="#222")
                    )
                    st.plotly_chart(fig, use_container_width=True)

        # ── TAB 5: Evolución ──────────────────────────────────────
        with tab5:
            if h.empty:
                st.info("No hay historial de consultas disponible para este paciente.")
            else:
                n_cons = len(h)
                esp_pac = v(p, "Especialidad")

                # ── Resumen rápido ────────────────────────────────
                r1,r2,r3 = st.columns(3)
                with r1:
                    st.markdown(f'<div class="mc"><div class="mc-lbl">Total consultas</div><div class="mc-val">{n_cons}</div></div>',
                                unsafe_allow_html=True)
                with r2:
                    primera = str(h.iloc[0]["Fecha"]) if not h.empty else "—"
                    st.markdown(f'<div class="mc v"><div class="mc-lbl">Primera consulta</div><div class="mc-val v" style="font-size:13px">{primera}</div></div>',
                                unsafe_allow_html=True)
                with r3:
                    ultima_f = str(h.iloc[-1]["Fecha"]) if not h.empty else "—"
                    st.markdown(f'<div class="mc n"><div class="mc-lbl">Última consulta</div><div class="mc-val n" style="font-size:13px">{ultima_f}</div></div>',
                                unsafe_allow_html=True)

                st.markdown("---")

                # ── Gráfica de peso a lo largo del tiempo ────────
                h_peso = h[h["Peso kg"] != ""].copy()
                try:
                    h_peso["Peso_num"] = pd.to_numeric(h_peso["Peso kg"], errors="coerce")
                    h_peso = h_peso.dropna(subset=["Peso_num","Fecha_dt"])
                    if len(h_peso) >= 2:
                        st.markdown("#### ⚖️ Evolución del peso")
                        fig_peso = px.line(
                            h_peso, x="Fecha_dt", y="Peso_num",
                            markers=True,
                            labels={"Fecha_dt":"Fecha","Peso_num":"Peso (kg)"},
                            color_discrete_sequence=["#0B3D91"]
                        )
                        fig_peso.update_traces(line=dict(width=3), marker=dict(size=8))
                        fig_peso.update_layout(
                            height=260, margin=dict(l=10,r=10,t=10,b=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            xaxis=dict(showgrid=True,gridcolor="#eee",
                                       tickfont=dict(color="#333")),
                            yaxis=dict(showgrid=True,gridcolor="#eee",
                                       tickfont=dict(color="#333")),
                            font=dict(color="#222")
                        )
                        st.plotly_chart(fig_peso, use_container_width=True)
                except: pass

                # ── Gráfica de signos vitales (FC y Temp) ─────────
                try:
                    h_sv = h.copy()
                    h_sv["FC_num"]   = pd.to_numeric(h_sv["FC lpm"],  errors="coerce")
                    h_sv["Temp_num"] = pd.to_numeric(h_sv["Temp C"],  errors="coerce")
                    h_sv["Sat_num"]  = pd.to_numeric(h_sv["SatO2 pct"], errors="coerce")
                    h_sv = h_sv.dropna(subset=["Fecha_dt"])

                    sv_ok = h_sv[h_sv["FC_num"].notna() | h_sv["Temp_num"].notna()]
                    if len(sv_ok) >= 2:
                        st.markdown("#### 💓 Signos vitales a lo largo del tiempo")
                        fig_sv = go.Figure()
                        if h_sv["FC_num"].notna().sum() >= 2:
                            fig_sv.add_trace(go.Scatter(
                                x=h_sv["Fecha_dt"], y=h_sv["FC_num"],
                                name="FC (lpm)", mode="lines+markers",
                                line=dict(color="#0B3D91",width=2),
                                marker=dict(size=7)
                            ))
                        if h_sv["Temp_num"].notna().sum() >= 2:
                            fig_sv.add_trace(go.Scatter(
                                x=h_sv["Fecha_dt"], y=h_sv["Temp_num"],
                                name="Temp (°C)", mode="lines+markers",
                                line=dict(color="#BF360C",width=2,dash="dot"),
                                marker=dict(size=7), yaxis="y2"
                            ))
                        if h_sv["Sat_num"].notna().sum() >= 2:
                            fig_sv.add_trace(go.Scatter(
                                x=h_sv["Fecha_dt"], y=h_sv["Sat_num"],
                                name="SatO₂ (%)", mode="lines+markers",
                                line=dict(color="#1A7A3C",width=2,dash="dash"),
                                marker=dict(size=7), yaxis="y3"
                            ))
                        fig_sv.update_layout(
                            height=300, margin=dict(l=10,r=80,t=10,b=10),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            legend=dict(orientation="h",y=-0.2,font=dict(color="#222")),
                            xaxis=dict(showgrid=True,gridcolor="#eee",
                                       tickfont=dict(color="#333")),
                            yaxis=dict(showgrid=True,gridcolor="#eee",
                                       tickfont=dict(color="#333"),title="FC"),
                            yaxis2=dict(overlaying="y",side="right",
                                        tickfont=dict(color="#BF360C"),title="Temp"),
                            yaxis3=dict(overlaying="y",side="right",position=0.95,
                                        tickfont=dict(color="#1A7A3C")),
                            font=dict(color="#222")
                        )
                        st.plotly_chart(fig_sv, use_container_width=True)
                except: pass

                # ── Gráfica progresión especialidad específica ────
                try:
                    if esp_pac in ["Odontología","Odontopediatría","Ortodoncia"]:
                        h_hig = h[h["Higiene Oral"] != ""].copy()
                        if len(h_hig) >= 2:
                            orden = {"Mala":1,"Regular":2,"Buena":3}
                            h_hig["Hig_num"] = h_hig["Higiene Oral"].map(orden)
                            h_hig = h_hig.dropna(subset=["Hig_num","Fecha_dt"])
                            st.markdown("#### 🦷 Evolución de higiene oral")
                            fig_hig = px.line(
                                h_hig, x="Fecha_dt", y="Hig_num",
                                markers=True,
                                labels={"Fecha_dt":"Fecha","Hig_num":"Nivel"},
                                color_discrete_sequence=["#1A7A3C"]
                            )
                            fig_hig.update_traces(line=dict(width=3), marker=dict(size=8))
                            fig_hig.update_layout(
                                height=220, margin=dict(l=10,r=10,t=10,b=10),
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                yaxis=dict(tickvals=[1,2,3],
                                           ticktext=["Mala","Regular","Buena"],
                                           tickfont=dict(color="#333")),
                                xaxis=dict(tickfont=dict(color="#333")),
                                font=dict(color="#222")
                            )
                            st.plotly_chart(fig_hig, use_container_width=True)

                    if esp_pac == "Fonoaudiología":
                        h_hab = h[h["Estado Habla"] != ""].copy()
                        if len(h_hab) >= 2:
                            orden = {"Severa":1,"Moderada":2,"Leve":3,
                                     "Sin hipernasalidad":4}
                            h_hab["Hab_num"] = h_hab["Estado Habla"].map(orden)
                            h_hab = h_hab.dropna(subset=["Hab_num","Fecha_dt"])
                            st.markdown("#### 🗣️ Evolución de hipernasalidad")
                            fig_hab = px.line(
                                h_hab, x="Fecha_dt", y="Hab_num",
                                markers=True,
                                labels={"Fecha_dt":"Fecha","Hab_num":"Nivel"},
                                color_discrete_sequence=["#6A0DAD"]
                            )
                            fig_hab.update_traces(line=dict(width=3), marker=dict(size=8))
                            fig_hab.update_layout(
                                height=220, margin=dict(l=10,r=10,t=10,b=10),
                                paper_bgcolor="rgba(0,0,0,0)",
                                plot_bgcolor="rgba(0,0,0,0)",
                                yaxis=dict(tickvals=[1,2,3,4],
                                           ticktext=["Severa","Moderada","Leve","Sin hipernasalidad"],
                                           tickfont=dict(color="#333")),
                                xaxis=dict(tickfont=dict(color="#333")),
                                font=dict(color="#222")
                            )
                            st.plotly_chart(fig_hab, use_container_width=True)
                except: pass

                # ── Respuesta al tratamiento por consulta ─────────
                try:
                    h_resp = h[h["Respuesta Tx"] != ""].copy()
                    if len(h_resp) >= 2:
                        orden_r = {"Buena":3,"Regular":2,"No evaluada":1,
                                   "Sin respuesta":0,"Deterioro":-1}
                        h_resp["Resp_num"] = h_resp["Respuesta Tx"].map(orden_r)
                        h_resp = h_resp.dropna(subset=["Resp_num","Fecha_dt"])
                        st.markdown("#### ✅ Respuesta al tratamiento por consulta")
                        colores_resp = {3:"#1A7A3C",2:"#E07B00",1:"#888",0:"#C62828",-1:"#7F0000"}
                        bar_colors = [colores_resp.get(int(r),  "#888")
                                      for r in h_resp["Resp_num"]]
                        fig_resp = go.Figure(go.Bar(
                            x=[str(f)[:10] for f in h_resp["Fecha_dt"]],
                            y=h_resp["Resp_num"],
                            marker_color=bar_colors,
                            text=h_resp["Respuesta Tx"],
                            textposition="outside",
                            textfont=dict(color="#222", size=11),
                        ))
                        fig_resp.update_layout(
                            height=240, margin=dict(l=10,r=10,t=10,b=30),
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            yaxis=dict(tickvals=[-1,0,1,2,3],
                                       ticktext=["Deterioro","Sin resp.","No eval.","Regular","Buena"],
                                       showgrid=True, gridcolor="#eee",
                                       tickfont=dict(color="#333")),
                            xaxis=dict(tickfont=dict(color="#333")),
                            font=dict(color="#222"), showlegend=False
                        )
                        st.plotly_chart(fig_resp, use_container_width=True)
                except: pass

                # ── Línea de tiempo de consultas ──────────────────
                st.markdown("#### 📅 Línea de tiempo de consultas")
                for _, row in h.iterrows():
                    fecha_c = str(row.get("Fecha","")).strip()
                    hora_c  = str(row.get("Hora","")).strip()
                    tipo_c  = str(row.get("Tipo Consulta","")).strip()
                    motivo  = str(row.get("Motivo","")).strip()
                    proc_c  = str(row.get("Procedimiento","")).strip()
                    evol_c  = str(row.get("Evolucion","")).strip()
                    resp_c  = str(row.get("Respuesta Tx","")).strip()
                    n_c     = str(row.get("N Consulta","")).strip()

                    color_tl = {"Primera vez":"#0B3D91","Control":"#1A7A3C",
                                "Postquirúrgico":"#E07B00","Urgencias":"#C62828"}.get(tipo_c,"#555")
                    st.markdown(f"""
                    <div class="tl">
                        <div class="tdot" style="background:{color_tl}"></div>
                        <div class="tbox">
                            <div class="tdate">📅 {fecha_c} {f'· ⏰ {hora_c}' if hora_c else ''} · Consulta #{n_c}</div>
                            <div class="ttit" style="color:{color_tl}">
                                {tipo_c} — {motivo}</div>
                            <div style="font-size:12px;color:#444;margin-top:3px">{evol_c}</div>
                            {f'<div style="font-size:11px;color:#666;margin-top:2px">🔧 {proc_c}</div>' if proc_c else ''}
                            <div style="margin-top:4px">
                                <span class="badge {'b-verde' if resp_c=='Buena' else 'b-naranja' if resp_c=='Regular' else 'b-gris'}">{resp_c}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
