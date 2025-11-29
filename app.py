import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date

# Caminho do arquivo de dados
DATA_PATH = Path("data/gastos.csv")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

# Colunas base do CSV
COLUMNS = [
    "id",
    "categoria",
    "fornecedor",
    "descricao",
    "valor_total",
    "entrada",
    "num_parcelas",
    "valor_parcela",
    "parcelas_pagas",
    "porcentagem_paga",
    "data_primeira_parcela",
    "observacoes",
]

# Configuração de estilo para casamento
def apply_wedding_styles():
    st.markdown("""
        <style>
        /* Cores temáticas para casamento */
        :root {
            --rosa-claro: #f9f0f5;
            --rosa-medio: #e8b4d4;
            --rosa-escuro: #d48aa9;
            --dourado: #d4af37;
            --verde-suave: #a8d5ba;
            --cinza-claro: #f5f5f5;
        }
        
        /* Background bonito com gradiente e padrão romântico */
        .stApp {
            background: linear-gradient(135deg, #f9f0f5 0%, #f5e6ef 25%, #f0dcf0 50%, #ebd2f1 75%, #e6c8f2 100%);
            background-attachment: fixed;
        }
        
        .stApp::before {
            content: "";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(212, 175, 55, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(232, 180, 212, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(168, 213, 186, 0.05) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }
        
        /* Padrão de corações sutis no background */
        .stApp::after {
            content: "💗💕💖";
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            font-size: 24px;
            opacity: 0.03;
            line-height: 1.5;
            letter-spacing: 20px;
            word-spacing: 50px;
            pointer-events: none;
            z-index: -1;
        }
        
        .main {
            background: rgba(255, 255, 255, 0.92);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            margin: 1rem;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        /* Cards de métricas - tema casamento */
        .metric-card {
            background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
            padding: 1.5rem;
            border-radius: 16px;
            border-left: 4px solid var(--dourado);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin: 0.5rem 0;
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }
        
        .metric-card h3 {
            color: var(--rosa-escuro);
            margin: 0 0 0.5rem 0;
            font-size: 1rem;
            font-weight: 600;
        }
        
        .metric-card h2 {
            color: #333;
            margin: 0;
            font-size: 1.6rem;
            font-weight: 700;
        }
        
        /* Cards de gastos */
        .gasto-card {
            background: linear-gradient(135deg, #ffffff 0%, #fefefe 100%);
            padding: 1.2rem;
            border-radius: 16px;
            border-left: 4px solid var(--rosa-medio);
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin: 0.8rem 0;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(10px);
        }
        
        .gasto-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(0,0,0,0.15);
            border-left: 4px solid var(--dourado);
        }
        
        .gasto-header {
            display: flex;
            justify-content: between;
            align-items: start;
            margin-bottom: 0.8rem;
        }
        
        .gasto-title {
            font-weight: 600;
            color: #333;
            font-size: 1.3rem;
            margin-bottom: 0.3rem;
        }
        
        .gasto-subtitle {
            color: #666;
            font-size: 1rem;
        }
        
        .gasto-progress {
            margin: 0.8rem 0;
        }
        
        .gasto-values {
            display: flex;
            justify-content: space-between;
            margin-top: 0.5rem;
            font-size: 1rem;
        }
        
        .valor-pago {
            color: var(--verde-suave);
            font-weight: 600;
        }
        
        .valor-restante {
            color: var(--rosa-escuro);
            font-weight: 600;
        }
        
        /* Botões */
        .stButton button {
            border-radius: 12px;
            border: none;
            padding: 0.7rem 1.5rem;
            font-weight: 600;
            background: linear-gradient(135deg, var(--rosa-medio), var(--rosa-escuro));
            color: white;
            box-shadow: 0 4px 15px rgba(212, 138, 169, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            background: linear-gradient(135deg, var(--rosa-escuro), var(--rosa-medio));
            color: white;
            box-shadow: 0 6px 20px rgba(212, 138, 169, 0.4);
            transform: translateY(-2px);
        }
        
        /* Progress bars */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, var(--rosa-medio), var(--dourado));
            border-radius: 10px;
        }
        
        /* Expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #ffffff, #fefefe);
            border-radius: 12px;
            border: 1px solid rgba(232, 180, 212, 0.3);
            font-weight: 600;
            color: var(--rosa-escuro);
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #fefefe, #ffffff);
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 12px 12px 0 0;
            padding: 12px 24px;
            border: 1px solid rgba(232, 180, 212, 0.3);
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #ffffff, #fefefe);
            border-bottom: 3px solid var(--rosa-medio);
        }
        
        /* Input fields styling */
        .stTextInput input, .stTextArea textarea, .stNumberInput input, .stDateInput input {
            border-radius: 10px;
            border: 1px solid rgba(232, 180, 212, 0.5);
            padding: 10px 12px;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus, .stNumberInput input:focus, .stDateInput input:focus {
            border-color: var(--rosa-medio);
            box-shadow: 0 0 0 2px rgba(232, 180, 212, 0.2);
        }
        
        /* Slider styling */
        .stSlider [data-baseweb="slider"] {
            color: var(--rosa-medio);
        }
        
        /* Header styling */
        .header-container {
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.8));
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            text-align: center;
        }
        
        /* Responsividade */
        @media (max-width: 768px) {
            .main {
                padding: 1rem;
                margin: 0.5rem;
            }
            .metric-card {
                padding: 1rem;
            }
            .gasto-card {
                padding: 1rem;
            }
            .header-container {
                padding: 1.5rem;
            }
        }
        </style>
    """, unsafe_allow_html=True)

def load_data() -> pd.DataFrame:
    """Carrega o CSV de gastos, criando se não existir."""
    if not DATA_PATH.exists():
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(DATA_PATH, index=False)
        return df

    df = pd.read_csv(DATA_PATH)

    # Garante que todas as colunas existam
    for col in COLUMNS:
        if col not in df.columns:
            df[col] = None

    # Tipagem básica
    df["valor_total"] = pd.to_numeric(df["valor_total"], errors="coerce").fillna(0.0)
    df["entrada"] = pd.to_numeric(df["entrada"], errors="coerce").fillna(0.0)
    df["num_parcelas"] = pd.to_numeric(df["num_parcelas"], errors="coerce").fillna(1).astype(int)
    df["valor_parcela"] = pd.to_numeric(df["valor_parcela"], errors="coerce").fillna(0.0)
    df["parcelas_pagas"] = pd.to_numeric(df["parcelas_pagas"], errors="coerce").fillna(0).astype(int)
    df["porcentagem_paga"] = pd.to_numeric(df["porcentagem_paga"], errors="coerce").fillna(0.0)

    return df[COLUMNS]

def save_data(df: pd.DataFrame) -> None:
    """Salva o DataFrame de volta no CSV."""
    df.to_csv(DATA_PATH, index=False)

def calcular_resumos(df: pd.DataFrame) -> dict:
    """Calcula totais: planejado, pago e faltante."""
    if df.empty:
        return {
            "total_planejado": 0.0,
            "total_pago": 0.0,
            "total_faltante": 0.0,
            "progresso_geral": 0.0,
        }

    # Calcula valor pago considerando entrada + parcelas pagas
    valor_pago_por_linha = df["entrada"] + (df["parcelas_pagas"] * df["valor_parcela"])
    total_planejado = df["valor_total"].sum()
    total_pago = valor_pago_por_linha.sum()
    total_faltante = total_planejado - total_pago
    progresso_geral = (total_pago / total_planejado * 100) if total_planejado > 0 else 0

    return {
        "total_planejado": float(total_planejado),
        "total_pago": float(total_pago),
        "total_faltante": float(total_faltante),
        "progresso_geral": float(progresso_geral),
    }

def formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def sincronizar_parcelas_porcentagem(df: pd.DataFrame) -> pd.DataFrame:
    """Sincroniza parcelas_pagas e porcentagem_paga"""
    df_sinc = df.copy()
    
    # Se porcentagem foi alterada, atualiza parcelas_pagas
    mask_porc = df_sinc['porcentagem_paga'].notna()
    df_sinc.loc[mask_porc, 'parcelas_pagas'] = (
        (df_sinc.loc[mask_porc, 'valor_total'] - df_sinc.loc[mask_porc, 'entrada']) * 
        df_sinc.loc[mask_porc, 'porcentagem_paga'] / 100 / 
        df_sinc.loc[mask_porc, 'valor_parcela']
    ).round().astype(int)
    
    # Se parcelas foram alteradas, atualiza porcentagem
    mask_parc = df_sinc['parcelas_pagas'].notna()
    df_sinc.loc[mask_parc, 'porcentagem_paga'] = (
        (df_sinc.loc[mask_parc, 'entrada'] + 
         (df_sinc.loc[mask_parc, 'parcelas_pagas'] * df_sinc.loc[mask_parc, 'valor_parcela'])) / 
        df_sinc.loc[mask_parc, 'valor_total'] * 100
    ).round(1)
    
    return df_sinc

def render_gasto_card(gasto):
    """Renderiza um card individual para cada gasto"""
    valor_pago = gasto['entrada'] + (gasto['parcelas_pagas'] * gasto['valor_parcela'])
    valor_restante = gasto['valor_total'] - valor_pago
    porcentagem_paga = (valor_pago / gasto['valor_total'] * 100) if gasto['valor_total'] > 0 else 0
    
    # Informações de parcelas
    info_parcelas = f"{gasto['parcelas_pagas']}/{gasto['num_parcelas']} parcelas"
    
    # Vamos construir o HTML em partes para evitar problemas de quebra
    card_parts = []
    card_parts.append(f'<div class="gasto-card">')
    card_parts.append(f'<div class="gasto-header">')
    card_parts.append(f'<div style="flex: 1;">')
    card_parts.append(f'<div class="gasto-title">{gasto["categoria"]}</div>')
    card_parts.append(f'<div class="gasto-subtitle">{gasto["fornecedor"]}</div>')
    card_parts.append(f'<div class="gasto-subtitle" style="font-size: 0.9rem; margin-top: 0.2rem;">{gasto["descricao"]}</div>')
    card_parts.append(f'</div>')
    card_parts.append(f'<div style="text-align: right;">')
    card_parts.append(f'<div style="font-weight: 600; color: #333; font-size: 1.2rem;">{formatar_moeda(gasto["valor_total"])}</div>')
    card_parts.append(f'<div style="font-size: 0.9rem; color: #666;">{info_parcelas}</div>')
    card_parts.append(f'<div style="font-size: 0.9rem; color: #666;">Parcela: {formatar_moeda(gasto["valor_parcela"])}</div>')
    card_parts.append(f'</div>')
    card_parts.append(f'</div>')
    
    card_parts.append(f'<div class="gasto-progress">')
    card_parts.append(f'<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">')
    card_parts.append(f'<span style="font-size: 1rem;">Progresso</span>')
    card_parts.append(f'<span style="font-weight: 600; color: var(--rosa-escuro); font-size: 1rem;">{porcentagem_paga:.1f}%</span>')
    card_parts.append(f'</div>')
    card_parts.append(f'<div style="background: #e0e0e0; border-radius: 10px; height: 8px; overflow: hidden;">')
    card_parts.append(f'<div style="background: linear-gradient(90deg, var(--rosa-medio), var(--dourado)); width: {porcentagem_paga}%; height: 100%; border-radius: 10px;"></div>')
    card_parts.append(f'</div>')
    card_parts.append(f'</div>')
    
    card_parts.append(f'<div class="gasto-values">')
    card_parts.append(f'<div class="valor-pago">Pago: {formatar_moeda(valor_pago)}</div>')
    card_parts.append(f'<div class="valor-restante">Restante: {formatar_moeda(valor_restante)}</div>')
    card_parts.append(f'</div>')
    
    if gasto['entrada'] > 0:
        card_parts.append(f'<div style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">Entrada: {formatar_moeda(gasto["entrada"])}</div>')
    
    card_parts.append(f'</div>')
    
    # Junta todas as partes em uma única string
    card_html = ''.join(card_parts)
    
    st.markdown(card_html, unsafe_allow_html=True)
    
# ==========================
#   APP STREAMLIT
# ==========================

def main():
    apply_wedding_styles()
    
    st.set_page_config(
        page_title="Controle Financeiro - Nosso Casamento",
        page_icon="💍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Header com novo estilo
    st.markdown("""
        <div class="header-container">
            <h1 style="color: #d48aa9; margin: 0; font-size: 2.5rem;">💍 Nosso Casamento</h1>
            <p style="color: #666; font-size: 1.3rem; margin: 0.5rem 0 0 0; font-weight: 500;">Controle financeiro dos nossos sonhos</p>
            <div style="margin-top: 1rem; font-size: 1.1rem; color: #888;">
                💕 Cada detalhe planejado com amor 💕
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Carrega dados
    df = load_data()
    resumos = calcular_resumos(df)

    # --------- FORMULÁRIO EXPANDÍVEL ---------
    # Inicializa o estado do expander
    if 'expander_aberto' not in st.session_state:
        st.session_state.expander_aberto = False

    # Botão para abrir o formulário se estiver fechado
    if not st.session_state.expander_aberto:
        col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
        with col_btn2:
            if st.button("➕ **Adicionar Novo Gasto**", use_container_width=True, key="abrir_form"):
                st.session_state.expander_aberto = True
                st.rerun()

    # Mostra o formulário apenas se o expander estiver aberto
    if st.session_state.expander_aberto:
        with st.expander("➕ **Adicionar Novo Gasto**", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                categoria = st.text_input("Categoria", placeholder="Ex.: Buffet, Decoração, Fotógrafo...", key="categoria")
                fornecedor = st.text_input("Fornecedor", placeholder="Nome do fornecedor", key="fornecedor")
                descricao = st.text_area("Descrição", placeholder="Detalhes do serviço/gasto", key="descricao")
                valor_total = st.number_input("Valor total (R$)", min_value=0.0, step=100.0, format="%.2f", key="valor_total")
                entrada = st.number_input("Entrada (R$)", min_value=0.0, step=100.0, format="%.2f", value=0.0, key="entrada")
            
            with col2:
                num_parcelas = st.number_input("Número de parcelas", min_value=1, step=1, value=1, key="num_parcelas")
                
                # Agora recalcula dinâmico a cada mudança
                valor_parcela = 0.0
                if valor_total > entrada and num_parcelas > 0:
                    valor_parcela = (valor_total - entrada) / num_parcelas
                
                st.info(f"**💎 Valor por parcela:** {formatar_moeda(valor_parcela)}")
                
                # Slider agora acompanha num_parcelas dinamicamente
                parcelas_pagas = st.slider(
                    "Parcelas já pagas",
                    0,
                    int(num_parcelas),
                    key="parcelas_pagas"
                )
                
                # Calcula porcentagem paga em tempo real
                valor_pago_total = entrada + (parcelas_pagas * valor_parcela)
                porcentagem_paga = (valor_pago_total / valor_total * 100) if valor_total > 0 else 0
                
                st.caption(f"📊 **Progresso:** {porcentagem_paga:.1f}%")
                
                data_primeira_parcela = st.date_input("Data da primeira parcela", value=date.today(), key="data_parcela")
                observacoes = st.text_area("Observações", placeholder="Alguma observação importante?", key="observacoes")

            # Botão de submit
            col_sub1, col_sub2, col_sub3 = st.columns([1,2,1])
            with col_sub2:
                submitted = st.button("💕 Adicionar à Nossa Lista", use_container_width=True)

            if submitted:
                # Validações
                erros = []
                if valor_total <= 0:
                    erros.append("O valor total deve ser maior que zero.")
                if entrada > valor_total:
                    erros.append("A entrada não pode ser maior que o valor total.")
                if not categoria.strip():
                    erros.append("Informe uma categoria.")
                if not fornecedor.strip():
                    erros.append("Informe o fornecedor.")

                if erros:
                    for e in erros:
                        st.error(e)
                else:
                    novo_id = 1 if df.empty else int(df["id"].max()) + 1

                    nova_linha = {
                        "id": novo_id,
                        "categoria": categoria.strip(),
                        "fornecedor": fornecedor.strip(),
                        "descricao": descricao.strip(),
                        "valor_total": float(valor_total),
                        "entrada": float(entrada),
                        "num_parcelas": int(num_parcelas),
                        "valor_parcela": float(valor_parcela),
                        "parcelas_pagas": int(parcelas_pagas),
                        "porcentagem_paga": float(porcentagem_paga),
                        "data_primeira_parcela": data_primeira_parcela.isoformat(),
                        "observacoes": observacoes.strip(),
                    }

                    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
                    save_data(df)
                    st.success("Gasto adicionado com sucesso! 💝")
                    
                    # Fecha o expander e limpa os campos
                    st.session_state.expander_aberto = False
                    
                    # Limpa os campos
                    keys_to_clear = ["categoria", "fornecedor", "descricao", "valor_total", "entrada", 
                                   "num_parcelas", "parcelas_pagas", "data_parcela", "observacoes"]
                    for key in keys_to_clear:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    st.rerun()

    # --------- RESUMO EM CARDS ---------
    st.markdown("---")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Total Planejado</h3>
                <h2>{formatar_moeda(resumos["total_planejado"])}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Total Pago</h3>
                <h2>{formatar_moeda(resumos["total_pago"])}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Saldo a Pagar</h3>
                <h2>{formatar_moeda(resumos["total_faltante"])}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <h3>Progresso Geral</h3>
                <h2>{resumos["progresso_geral"]:.1f}%</h2>
            </div>
        """, unsafe_allow_html=True)

    # Barra de progresso geral
    st.progress(resumos["progresso_geral"] / 100, text=f"Progresso geral do nosso casamento: {resumos['progresso_geral']:.1f}%")

    st.markdown("---")

    # --------- VISUALIZAÇÃO PRINCIPAL ---------
    if not df.empty:
        # Prepara dados para exibição
        df_display = df.copy()
        df_display["valor_pago"] = df_display["entrada"] + (df_display["parcelas_pagas"] * df_display["valor_parcela"])
        df_display["valor_restante"] = df_display["valor_total"] - df_display["valor_pago"]

        # Abas para diferentes visualizações
        tab1, tab2, tab3 = st.tabs(["🎀 Nossos Gastos", "📊 Edição Avançada", "📈 Gráficos"])

        with tab1:
            st.subheader("Nossa Lista de Gastos")
            
            # Filtros
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                categorias = ["Todas"] + list(df_display['categoria'].unique())
                categoria_filtro = st.selectbox("Filtrar por categoria:", categorias)
            
            with col_f2:
                status_options = ["Todos", "Completos (100%)", "Em andamento", "Não iniciados (0%)"]
                status_filtro = st.selectbox("Filtrar por status:", status_options)
            
            # Aplica filtros
            df_filtrado = df_display.copy()
            if categoria_filtro != "Todas":
                df_filtrado = df_filtrado[df_filtrado['categoria'] == categoria_filtro]
            
            if status_filtro == "Completos (100%)":
                df_filtrado = df_filtrado[df_filtrado['porcentagem_paga'] == 100]
            elif status_filtro == "Em andamento":
                df_filtrado = df_filtrado[(df_filtrado['porcentagem_paga'] > 0) & (df_filtrado['porcentagem_paga'] < 100)]
            elif status_filtro == "Não iniciados (0%)":
                df_filtrado = df_filtrado[df_filtrado['porcentagem_paga'] == 0]
            
            # Exibe cards
            for _, gasto in df_filtrado.iterrows():
                render_gasto_card(gasto)

        with tab2:
            st.subheader("Edição Detalhada")
            st.caption("Edite os valores diretamente na tabela abaixo")
            
            editable_cols = [
                "id", "categoria", "fornecedor", "descricao", "valor_total", "entrada",
                "num_parcelas", "valor_parcela", "parcelas_pagas", "porcentagem_paga",
                "data_primeira_parcela", "observacoes"
            ]

            edited_df = st.data_editor(
                df[editable_cols],
                num_rows="fixed",
                use_container_width=True,
                key="editor_avancado",
            )

            col_salvar, col_cancelar = st.columns(2)
            with col_salvar:
                if st.button("💾 Salvar Alterações", use_container_width=True, type="primary"):
                    # Sincroniza parcelas e porcentagem
                    edited_df = sincronizar_parcelas_porcentagem(edited_df)
                    
                    # Reaplica tipagem
                    edited_df["valor_total"] = pd.to_numeric(edited_df["valor_total"], errors="coerce").fillna(0.0)
                    edited_df["entrada"] = pd.to_numeric(edited_df["entrada"], errors="coerce").fillna(0.0)
                    edited_df["num_parcelas"] = pd.to_numeric(edited_df["num_parcelas"], errors="coerce").fillna(1).astype(int)
                    edited_df["valor_parcela"] = pd.to_numeric(edited_df["valor_parcela"], errors="coerce").fillna(0.0)
                    edited_df["parcelas_pagas"] = pd.to_numeric(edited_df["parcelas_pagas"], errors="coerce").fillna(0).astype(int)
                    edited_df["porcentagem_paga"] = pd.to_numeric(edited_df["porcentagem_paga"], errors="coerce").fillna(0.0)

                    # Garante consistência
                    edited_df["parcelas_pagas"] = edited_df[["parcelas_pagas", "num_parcelas"]].min(axis=1)
                    edited_df["porcentagem_paga"] = edited_df["porcentagem_paga"].clip(0, 100)

                    save_data(edited_df[COLUMNS])
                    st.success("Alterações salvas com sucesso! 💝")
                    st.rerun()

            with col_cancelar:
                if st.button("❌ Descartar Alterações", use_container_width=True):
                    st.rerun()

        with tab3:
            st.subheader("Visualizações Gráficas")
            
            # Prepara dados para os gráficos
            df_graficos = df.copy()
            df_graficos["valor_pago"] = df_graficos["entrada"] + (df_graficos["parcelas_pagas"] * df_graficos["valor_parcela"])
            df_graficos["valor_restante"] = df_graficos["valor_total"] - df_graficos["valor_pago"]
            
            # Gráfico 1: Distribuição por Categoria
            st.write("### 📊 Distribuição de Gastos por Categoria")
            
            # Agrupa por categoria
            gastos_por_categoria = df_graficos.groupby('categoria').agg({
                'valor_total': 'sum',
                'valor_pago': 'sum',
                'valor_restante': 'sum'
            }).reset_index()
            
            # Mostra como tabela e gráfico de barras
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                st.dataframe(
                    gastos_por_categoria[['categoria', 'valor_total', 'valor_pago', 'valor_restante']]
                    .rename(columns={
                        'categoria': 'Categoria',
                        'valor_total': 'Total (R$)',
                        'valor_pago': 'Pago (R$)',
                        'valor_restante': 'Restante (R$)'
                    })
                    .sort_values('Total (R$)', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
            
            with col_g2:
                # Gráfico de barras para totais por categoria
                st.bar_chart(
                    gastos_por_categoria.set_index('categoria')['valor_total'],
                    use_container_width=True
                )
            
            # Gráfico 2: Progresso por Categoria
            st.write("### 📈 Progresso de Pagamento por Categoria")
            
            # Calcula progresso percentual por categoria
            gastos_por_categoria['progresso_percentual'] = (
                gastos_por_categoria['valor_pago'] / gastos_por_categoria['valor_total'] * 100
            ).round(1)
            
            col_g3, col_g4 = st.columns(2)
            
            with col_g3:
                # Gráfico de barras horizontais para progresso
                st.bar_chart(
                    gastos_por_categoria.set_index('categoria')['progresso_percentual'],
                    use_container_width=True
                )
            
            with col_g4:
                # Métricas de progresso por categoria
                for _, cat in gastos_por_categoria.iterrows():
                    st.metric(
                        label=f"{cat['categoria']}",
                        value=f"{cat['progresso_percentual']}%",
                        delta=formatar_moeda(cat['valor_pago']),
                        delta_color="normal"
                    )
            
            # Gráfico 3: Status dos Pagamentos
            st.write("### 🎯 Status dos Pagamentos")
            
            # Classifica os gastos por status
            def classificar_status(porcentagem):
                if porcentagem == 0:
                    return "Não Iniciado"
                elif porcentagem == 100:
                    return "Completo"
                elif porcentagem > 0 and porcentagem < 100:
                    return "Em Andamento"
                else:
                    return "Outro"
            
            df_graficos['status'] = df_graficos['porcentagem_paga'].apply(classificar_status)
            status_counts = df_graficos['status'].value_counts()
            
            col_g5, col_g6 = st.columns(2)
            
            with col_g5:
                # Gráfico de pizza para status
                st.write("**Distribuição por Status**")
                for status, count in status_counts.items():
                    st.write(f"**{status}:** {count} gasto(s)")
            
            with col_g6:
                # Métricas resumidas
                total_gastos = len(df_graficos)
                completos = len(df_graficos[df_graficos['porcentagem_paga'] == 100])
                andamento = len(df_graficos[(df_graficos['porcentagem_paga'] > 0) & (df_graficos['porcentagem_paga'] < 100)])
                nao_iniciados = len(df_graficos[df_graficos['porcentagem_paga'] == 0])
                
                st.metric("Total de Gastos", total_gastos)
                st.metric("Completos", completos)
                st.metric("Em Andamento", andamento)
                st.metric("Não Iniciados", nao_iniciados)
            
            # Gráfico 4: Linha do Tempo (Próximos Vencimentos)
            st.write("### ⏰ Próximos Vencimentos")
            
            # Filtra gastos que ainda têm valor a pagar
            gastos_pendentes = df_graficos[df_graficos['valor_restante'] > 0].copy()
            
            if not gastos_pendentes.empty:
                # Ordena pela data da primeira parcela
                gastos_pendentes['data_primeira_parcela'] = pd.to_datetime(gastos_pendentes['data_primeira_parcela'])
                gastos_pendentes = gastos_pendentes.sort_values('data_primeira_parcela')
                
                # Mostra os próximos vencimentos
                st.dataframe(
                    gastos_pendentes[['categoria', 'fornecedor', 'valor_restante', 'data_primeira_parcela']]
                    .rename(columns={
                        'categoria': 'Categoria',
                        'fornecedor': 'Fornecedor',
                        'valor_restante': 'Valor Restante (R$)',
                        'data_primeira_parcela': 'Próximo Vencimento'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.success("🎉 Todos os gastos estão quitados!")

    else:
        # Estado vazio
        st.markdown("""
            <div style='text-align: center; padding: 4rem; background: rgba(255,255,255,0.9); border-radius: 20px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); border: 1px solid rgba(255,255,255,0.2);'>
                <h3 style="color: #d48aa9;">💕 Comece a Planejar Nosso Casamento!</h3>
                <p style="color: #666; font-size: 1.1rem;">Adicione seu primeiro gasto expandindo o formulário acima.</p>
                <div style="font-size: 3rem; margin-top: 1rem;">💍✨</div>
            </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()