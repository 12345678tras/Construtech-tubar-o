
import streamlit as st
import math

# Configuração inicial da página
st.set_page_config(
    page_title="Construtech Tubarão - Engenharia & Orçamentos",
    page_icon="🦈",
    layout="centered"
)

# Estilização visual profissional aprimorada
st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .main-title { font-size: 28px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    .subtitle { font-size: 15px; color: #475569; text-align: center; margin-bottom: 25px; }
    .card-resultado {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        padding: 20px;
        border-radius: 12px;
        margin-top: 15px;
        margin-bottom: 15px;
        border: 1px solid #BFDBFE;
    }
    </style>
""", unsafe_allow_html=True)

# Cabeçalho do Aplicativo
st.markdown('<div class="main-title">🦈 Construtech Tubarão</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Plataforma Profissional de Engenharia e Orçamentos</div>', unsafe_allow_html=True)

st.divider()

# Seção interativa inicial
st.subheader("Bem-vindo ao sistema!")
st.write("Utilize o menu lateral ou as opções abaixo para navegar pelos módulos de cálculo e orçamento.")

# Exemplo de entrada/interação
projeto_nome = st.text_input("Nome do Projeto / Cliente:", "Obra Residencial Exemplo")
orcamento_base = st.number_input("Valor Base Estimado (R$):", min_value=0.0, value=50000.0, step=1000.0)

if st.button("Calcular Viabilidade e Custos"):
    bdi = 0.25  # 25% de BDI padrão
    valor_total = orcamento_base * (1 + bdi)
    st.success("Cálculo realizado com sucesso!")

    
    st.markdown(f"""
        <div class="card-resultado">
            <h4>📊 Resumo para: {projeto_nome}</h4>
            <p><b>Orçamento Base:</b> R$ {orcamento_base:,.2f}</p>
            <p><b>BDI Aplicado:</b> {bdi*100}%</p>
            <p><b>Valor Total Sugerido com BDI:</b> R$ {valor_total:,.2f}</p>
        </div>
    """, unsafe_allow_html=True)
