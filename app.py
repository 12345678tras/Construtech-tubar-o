import streamlit as st

# Configuração da Página (Deve ser sempre o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma Profissional",
    page_icon="🏗️",
    layout="wide",
)

# Estilização visual básica
st.markdown(
    """
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 16px; color: #4B5563; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 30px; border-radius: 10px; text-align: center; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# SISTEMA DE CONTROLE DE ACESSO (PAYWALL)
# ==========================================
# Inicializa as chaves de controle no session_state
if "acesso_liberado" not in st.session_state:
    # Verificamos se já existe um registro simulado neste navegador/computador
    st.session_state.acesso_liberado = st.session_state.get(
        "acesso_liberado", False
    )

# Parâmetro de simulação de pagamento via URL (ex: ?liberado=true)
params = st.query_params
if "liberado" in params and params["liberado"] == "sim":
    st.session_state.acesso_liberado = True

# Tela de Bloqueio se o acesso não foi liberado ou pago
if not st.session_state.acesso_liberado:
    st.markdown(
        '<p class="main-header" style="text-align: center;">🏗️ Construtech Tubarão</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header" style="text-align: center;">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown(
        """
        <div class="paywall-box">
            <h2>⚠️ Acesso Único Utilizado</h2>
            <p>Identificamos que este computador já utilizou o acesso de demonstração gratuito desta plataforma.</p>
            <p>Para continuar utilizando nossos módulos profissionais de cálculo e engenharia, por favor, realize o pagamento da licença de acesso.</p>
            <br>
            <h4>Chave PIX para Pagamento:</h4>
            <p style="font-size: 18px; font-weight: bold; color: #1E3A8A;">financeiro@construtechtubarao.com.br</p>
            <p><i>(Envie o comprovante para liberar seu acesso instantaneamente)</i></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.write("")
        # Botão de simulação para você testar a liberação após o "pagamento"
        if st.button(
            "Já fiz o pagamento / Simular Liberação",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.acesso_liberado = True
            st.rerun()

    st.stop(
    )  # Interrompe a execução do restante do código caso não esteja liberado


# ==========================================
# APLICAÇÃO PRINCIPAL (Liberada após acesso)
# ==========================================

# Cabeçalho Principal
st.markdown(
    '<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Menu Lateral para Navegação dos Módulos
st.sidebar.title("Navegação de Módulos")
modulo = st.sidebar.selectbox(
    "Selecione a Ferramenta:",
    [
        "📊 Visão Geral e BDI",
        "🧱 Cálculo de Materiais (Areia/Cimento)",
        "🏗️ Estrutural e Vigas",
        "🚰 Sistema Hidráulico",
        "💼 Faturamento e CNPJ",
    ],
)

# Botão na barra lateral para simular novo bloqueio (útil para testes)
if st.sidebar.button("🔒 Bloquear / Sair deste Computador"):
    st.session_state.acesso_liberado = False
    st.rerun()

# Controle de Sessão para Armazenar Dados do Orçamento
if "orcamento_base" not in st.session_state:
    st.session_state.orcamento_base = 50000.0
if "bdi" not in st.session_state:
    st.session_state.bdi = 25.0
if "cliente" not in st.session_state:
    st.session_state.cliente = "Obra Residencial Exemplo"

# ==========================================
# MÓDULO 1: VISÃO GERAL E BDI
# ==========================================
if modulo == "📊 Visão Geral e BDI":
    st.subheader("Painel de Controle e Viabilidade")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.cliente = st.text_input(
            "Nome do Projeto / Cliente:", value=st.session_state.cliente
        )
        st.session_state.orcamento_base = st.number_input(
            "Valor Base Estimado (R$):",
            min_value=0.0,
            value=st.session_state.orcamento_base,
            step=1000.0,
        )
    with col2:
        st.session_state.bdi = st.slider(
            "Taxa de BDI Aplicada (%):", min_value=0.0, max_value=50.0, value=25.0
        )

    if st.button("Calcular Viabilidade e Custos", type="primary"):
        total_com_bdi = st.session_state.orcamento_base * (
            1 + st.session_state.bdi / 100
        )

        st.markdown(
            f"""
        <div class="card">
            <h3>📊 Resumo para: {st.session_state.cliente}</h3>
            <p><b>Orçamento Base:</b> R$ {st.session_state.orcamento_base:,.2f}</p>
            <p><b>BDI Aplicado:</b> {st.session_state.bdi}%</p>
            <p><b>Valor Total Sugerido com BDI:</b> R$ {total_com_bdi:,.2f}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo realizado com sucesso!")

# ==========================================
# MÓDULO 2: CÁLCULO DE MATERIAIS
# ==========================================
elif modulo == "🧱 Cálculo de Materiais (Areia/Cimento)":
    st.subheader("Dimensionamento de Insumos Básicos")
    st.write(
        "Calcule a quantidade aproximada de areia, cimento e brita com base na metragem da obra."
    )

    area_construcao = st.number_input("Área da Construção (m²):", value=100.0)

    col1, col2, col3 = st.columns(3)
    with col1:
        qtd_cimento = area_construcao * 3.5
        st.metric(label="Sacos de Cimento (50kg)", value=f"{int(qtd_cimento)} un")
    with col2:
        qtd_areia = area_construcao * 0.12
        st.metric(label="Areia Média/Grossa", value=f"{qtd_areia:.2f} m³")
    with col3:
        qtd_brita = area_construcao * 0.10
        st.metric(label="Brita nº 1", value=f"{qtd_brita:.2f} m³")

    st.info(
        "💡 Os índices consideram traços padrões para alvenaria e contrapiso."
    )

# ==========================================
# MÓDULO 3: ESTRUTURAL E VIGAS
# ==========================================
elif modulo == "🏗️ Estrutural e Vigas":
    st.subheader("Dimensionamento de Elementos Estruturais")
    st.write("Estimativa de aço, concreto e formas para vigas e pilares.")

    vao_livre = st.slider(
        "Maior Vão Livre (metros):", min_value=2.0, max_value=10.0, value=4.0
    )
    pavimentos = st.number_input(
        "Número de Pavimentos:", min_value=1, max_value=5, value=1
    )

    if st.button("Calcular Estimativa Estrutural"):
        volume_concreto = vao_livre * pavimentos * 0.45
        peso_aco = volume_concreto * 90

        st.success(
            f"Para um vão de {vao_livre}m com {pavimentos} pavimento(s):"
        )
        st.write(f"- **Volume Estimado de Concreto:** {volume_concreto:.2f} m³")
        st.write(f"- **Consumo Estimado de Aço (CA-50):** {peso_aco:.2f} kg")

# ==========================================
# MÓDULO 4: SISTEMA HIDRÁULICO
# ==========================================
elif modulo == "🚰 Sistema Hidráulico":
    st.subheader("Orçamento de Instalações Hidráulicas")
    st.write("Levantamento preliminar de tubos, conexões e caixas d'água.")

    pontos_agua = st.number_input(
        "Número de Pontos de Água/Esgoto:", min_value=1, value=10
    )
    tem_reservatorio = st.checkbox("Incluir Caixa D'água de 1000L", value=True)

    custo_tubos = pontos_agua * 45.0
    custo_caixa = 650.0 if tem_reservatorio else 0.0
    total_hidraulico = custo_tubos + custo_caixa

    st.markdown(
        f"""
    <div class="card">
        <h4>Resumo Hidráulico</h4>
        <p><b>Tubulações e Conexões ({pontos_agua} pontos):</b> R$ {custo_tubos:,.2f}</p>
        <p><b>Reservatório:</b> R$ {custo_caixa:,.2f}</p>
        <p><b>Total Parcial Hidráulico:</b> R$ {total_hidraulico:,.2f}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# MÓDULO 5: FATURAMENTO E CNPJ
# ==========================================
elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Configurações de Faturamento e Dados Comerciais")
    st.write("Insira os dados da sua empresa para emissão do relatório.")

    cnpj_empresa = st.text_input(
        "CNPJ:", value="00.000.000/0001-00", placeholder="XX.XXX.XXX/0001-XX"
    )
    razao_social = st.text_input(
        "Razão Social / Nome do Engenheiro:", value="Construtech Tubarão LTDA"
    )
    chave_pix = st.text_input("Chave PIX para Recebimento:", value="")

    if st.button("Salvar Dados Fiscais"):
        st.success(
            f"Dados da empresa {razao_social} (CNPJ: {cnpj_empresa}) salvos com sucesso para os relatórios!"
        )

# Rodapé institucional
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
