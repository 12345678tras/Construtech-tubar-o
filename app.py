import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma Profissional",
    page_icon="🏗️",
    layout="wide",
)

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
# 2. CONTROLE DE SESSÃO (NATIVO DO STREAMLIT)
# ==========================================
if "licenca_global_liberada" not in st.session_state:
    st.session_state.licenca_global_liberada = False

if "ja_fez_calculo_gratis" not in st.session_state:
    st.session_state.ja_fez_calculo_gratis = False

# Variável para controlar se acabou de rodar o cálculo gratuito nesta execução
if "mostrar_resultado_gratis" not in st.session_state:
    st.session_state.mostrar_resultado_gratis = False

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
        st.session_state.ja_fez_calculo_gratis = (
            False  # Reseta a trava ao liberar
        )
        st.sidebar.success("Licença definitiva ativada!")
        st.rerun()
    else:
        st.sidebar.error("Senha incorreta!")

if st.sidebar.button("🔒 Bloquear / Resetar Testes"):
    st.session_state.licenca_global_liberada = False
    st.session_state.ja_fez_calculo_gratis = False
    st.session_state.mostrar_resultado_gratis = False
    st.rerun()

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

if "orcamento_base" not in st.session_state:
    st.session_state.orcamento_base = 50000.0
if "bdi" not in st.session_state:
    st.session_state.bdi = 25.0
if "cliente" not in st.session_state:
    st.session_state.cliente = "Obra Residencial Exemplo"

# ==========================================
# 4. MÓDULOS DO SISTEMA
# ==========================================

# Se ele já usou o teste e tentou fazer algo novo, interceptamos aqui com o Paywall
bloqueado = (
    not st.session_state.licenca_global_liberada
    and st.session_state.ja_fez_calculo_gratis
)

if bloqueado:
    st.markdown("---")
    st.markdown(
        """
        <div class="paywall-box">
            <h2>⚠️ Seu Período de Testes Gratuitos Expirou!</h2>
            <p>Você já utilizou a sua demonstração gratuita nesta sessão.</p>
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
                link_infinitepay = "https://link.infinitepay.io/cristiane-da-260/VC1DLUMtUg-Aklf8ElJpW-20,00"
                st.success("Redirecionando para o ambiente seguro de pagamento!")
                st.markdown(
                    f"👉 **[Clique aqui para abrir o pagamento da"
                    f" InfinitePay]({link_infinitepay})**"
                )
                st.info(
                    "Após efetuar o pagamento, utilize sua senha de liberação na"
                    " aba ao lado."
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
                    st.session_state.ja_fez_calculo_gratis = False
                    st.success("Licença ativada com sucesso!")
                    st.rerun()
                else:
                    st.error("Senha incorreta!")

else:
    # Aviso amigável do teste grátis ativo (se ainda não gastou)
    if not st.session_state.licenca_global_liberada:
        st.markdown(
            '<div class="alerta-teste">⭐ Você está usando a sua <b>única demonstração gratuita</b>. Aproveite para testar!</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

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
            # Marca que o teste grátis foi consumido
            st.session_state.ja_fez_calculo_gratis = True
            st.success("Cálculo realizado com sucesso (Demonstração Gratuita)!")
            # Exemplo de resultado simples na tela
            custo_total = st.session_state.orcamento_base * (
                1 + st.session_state.bdi / 100
            )
            st.metric(
                label="Preço de Venda Sugerido (com BDI)",
                value=f"R$ {custo_total:,.2f}",
            )

    elif modulo == "🧱 Cálculo de Alvenaria":
        st.subheader("Dimensionamento Técnico de Alvenaria")
        area_paredes = st.number_input(
            "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
        )
        preco_tijolo_un = st.number_input(
            "Preço Unitário do Bloco (R$):", value=1.20, step=0.10
        )

        if st.button("Calcular Insumos de Alvenaria", type="primary"):
            st.session_state.ja_fez_calculo_gratis = True
            st.success("Insumos calculados com sucesso (Demonstração Gratuita)!")
            tijolos_estimados = area_paredes * 35  # Exemplo de cálculo
            custo_tijolos = tijolos_estimados * preco_tijolo_un
            st.metric(
                label="Quantidade Estimada de Blocos",
                value=f"{tijolos_estimados:.0f} un",
            )
            st.metric(label="Custo Total de Blocos", value=f"R$ {custo_tijolos:,.2f}")

    elif modulo in [
        "🏠 Cálculo Avançado de Lajes",
        "⚙️ Projeto de Ferragens e Aço",
        "🏗️ Estrutural, Vigas e Validação",
        "🚰 Sistema Hidráulico Profissional",
        "💼 Faturamento e CNPJ",
    ]:
        st.subheader(f"Painel do Módulo: {modulo}")
        if st.button("Executar Simulação do Módulo", type="primary"):
            st.session_state.ja_fez_calculo_gratis = True
            st.success("Simulação executada com sucesso (Demonstração Gratuita)!")
            st.info(
                "Resultados simulados para este módulo exibidos com sucesso."
            )

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
