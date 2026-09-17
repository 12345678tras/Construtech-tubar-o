import streamlit as st
from streamlit_cookies_controller import CookieController

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma Profissional",
    page_icon="🏗️",
    layout="wide",
)

# Inicializa o controlador de cookies do navegador
controller = CookieController()

# Estilização visual limpa e profissional
st.markdown(
    """
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 16px; color: #4B5563; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #1E3A8A; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 30px; border-radius: 10px; text-align: center; }
    .admin-box { background-color: #EFF6FF; border: 1px solid #3B82F6; padding: 15px; border-radius: 8px; margin-top: 20px; }
    .alerta-teste { background-color: #FEF3C7; border: 1px solid #F59E0B; padding: 10px; border-radius: 6px; color: #92400E; font-weight: bold; margin-bottom: 15px; text-align: center; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. CONTROLE DE SESSÃO E COOKIES (TRAVA POR MÁQUINA)
# ==========================================
if "licenca_global_liberada" not in st.session_state:
    cookie_liberado = controller.get("construtech_liberado")
    if cookie_liberado == "true":
        st.session_state.licenca_global_liberada = True
    else:
        st.session_state.licenca_global_liberada = False

# Menu Lateral de Navegação
st.sidebar.title("Navegação de Módulos")
modulo = st.sidebar.selectbox(
    "Selecione a Ferramenta:",
    [
        "📊 Visão Geral e BDI",
        "🧱 Cálculo de Alvenaria",
        "🏠 Cálculo Avançado de Lajes",
        "⚙️ Projeto de Ferragens e Aço",
        "🏗️ Estrutural, Vigas e Validação",
        "🚰 Sistema Hidráulico Profissional",
        "💼 Faturamento e CNPJ",
    ],
)

# Painel do Administrador na barra lateral
st.sidebar.markdown("---")
st.sidebar.write("🔑 **Painel do Administrador**")
senha_sidebar = st.sidebar.text_input(
    "Chave Mestra:", type="password", placeholder="Digite a chave"
)
if st.sidebar.button("Desbloquear Sistema Inteiro"):
    if senha_sidebar == "construtech123":
        st.session_state.licenca_global_liberada = True
        controller.set("construtech_liberado", "true", max_age=31536000)
        st.sidebar.success("Licença definitiva ativada e salva na máquina!")
        st.rerun()
    else:
        st.sidebar.error("Senha incorreta!")

if st.sidebar.button("🔒 Bloquear / Resetar Testes (Zerar Cookie)"):
    st.session_state.licenca_global_liberada = False
    controller.remove("construtech_liberado")
    controller.remove("ja_fez_calculo_gratis")
    st.rerun()


# Função para verificar se o usuário já gastou o cálculo gratuito usando Cookies
def verificar_acesso_global():
    if st.session_state.licenca_global_liberada:
        return True

    ja_usou = controller.get("ja_fez_calculo_gratis")
    if ja_usou == "true":
        return False

    return True


# ==========================================
# 3. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown(
    '<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
    unsafe_allow_html=True,
)

# ==========================================
# 4. SISTEMA DE PAYWALL E INFINITEPAY
# ==========================================
liberado_atual = verificar_acesso_global()

if not liberado_atual:
    st.markdown("---")
    st.markdown(
        """
        <div class="paywall-box">
            <h2>⚠️ Seu Período de Testes Gratuitos Expirou!</h2>
            <p>Você já utilizou a sua demonstração gratuita neste computador.</p>
            <p>Para desbloquear o acesso completo e ilimitado, faça o pagamento via <b>InfinitePay</b> (R$ 20,00).</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_pay1, col_pay2 = st.columns(2)

    with col_pay1:
        st.markdown("### 🚀 Pagamento Instantâneo (InfinitePay)")
        email_cliente = st.text_input(
            "Seu e-mail:", placeholder="seu@email.com"
        )

        if st.button("Ir para o Pagamento (R$ 20,00)"):
            if email_cliente:
                # SEU LINK REAL DA INFINITEPAY INSERIDO AQUI:
                link_infinitepay = "https://link.infinitepay.io/cristiane-da-260/VC1DLUMtUg-Aklf8ElJpW-20,00"

                st.success("Redirecionando para o ambiente seguro de pagamento!")
                st.markdown(
                    f"👉 **[Clique aqui para abrir o pagamento da"
                    f" InfinitePay]({link_infinitepay})**"
                )
                st.info(
                    "Após efetuar o pagamento, entre em contato ou utilize sua"
                    " senha de liberação."
                )
            else:
                st.warning("Por favor, preencha o seu e-mail.")

    with col_pay2:
        st.markdown("### 🔑 Liberação Manual (Admin)")
        with st.form(key="form_admin_paywall"):
            senha_admin = st.text_input(
                "Chave Mestra:",
                type="password",
                placeholder="Digite a senha",
            )
            botao_enviar = st.form_submit_button("Liberar com Chave")
            if botao_enviar:
                if senha_admin == "construtech123":
                    st.session_state.licenca_global_liberada = True
                    controller.set("construtech_liberado", "true", max_age=31536000)
                    st.success("Licença ativada com sucesso!")
                    st.rerun()
                else:
                    st.error("Senha incorreta!")

    st.stop()

# Aviso amigável do teste grátis ativo
if not st.session_state.licenca_global_liberada:
    st.markdown(
        f'<div class="alerta-teste">⭐ Você está usando a sua <b>única demonstração gratuita</b> liberada para este computador. Aproveite para testar!</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

if "orcamento_base" not in st.session_state:
    st.session_state.orcamento_base = 50000.0
if "bdi" not in st.session_state:
    st.session_state.bdi = 25.0
if "cliente" not in st.session_state:
    st.session_state.cliente = "Obra Residencial Exemplo"

# ==========================================
# 5. MÓDULOS DO SISTEMA
# ==========================================

if modulo == "📊 Visão Geral e BDI":
    st.subheader("Painel de Controle e Viabilidade Comercial")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.cliente = st.text_input(
            "Nome do Projeto / Cliente:", value=st.session_state.cliente
        )
        st.session_state.orcamento_base = st.number_input(
            "Custo Direto Total Estimado (R$):",
            min_value=0.0,
            value=st.session_state.orcamento_base,
            step=1000.0,
        )
    with col2:
        st.session_state.bdi = st.slider(
            "Taxa de BDI Aplicada (%):", 0.0, 50.0, 25.0
        )

    if st.button("Calcular Viabilidade e Venda", type="primary"):
        controller.set("ja_fez_calculo_gratis", "true", max_age=31536000)
        st.rerun()

elif modulo == "🧱 Cálculo de Alvenaria":
    st.subheader("Dimensionamento Técnico de Alvenaria")
    area_paredes = st.number_input(
        "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
    )
    preco_tijolo_un = st.number_input(
        "Preço Unitário do Bloco (R$):", value=1.20, step=0.10
    )

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        controller.set("ja_fez_calculo_gratis", "true", max_age=31536000)
        st.rerun()

elif modulo in [
    "🏠 Cálculo Avançado de Lajes",
    "⚙️ Projeto de Ferragens e Aço",
    "🏗️ Estrutural, Vigas e Validação",
    "🚰 Sistema Hidráulico Profissional",
    "💼 Faturamento e CNPJ",
]:
    st.subheader(f"Painel do Módulo: {modulo}")
    if st.button("Executar Simulação do Módulo", type="primary"):
        controller.set("ja_fez_calculo_gratis", "true", max_age=31536000)
        st.rerun()

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
