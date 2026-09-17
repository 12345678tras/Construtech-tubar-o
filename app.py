import streamlit as st

# Configuração da Página
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
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #1E3A8A; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 30px; border-radius: 10px; text-align: center; }
    .admin-box { background-color: #EFF6FF; border: 1px solid #3B82F6; padding: 15px; border-radius: 8px; margin-top: 20px; }
    .alerta-aprovado { background-color: #DEF7EC; border: 1px solid #31C48D; padding: 10px; border-radius: 6px; color: #03543F; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# CONTROLE DE ACESSO (PAYWALL + ADMIN)
# ==========================================
if "acesso_liberado" not in st.session_state:
    st.session_state.acesso_liberado = False

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
            <h2>⚠️ Acesso Restrito / Pagamento Pendente</h2>
            <p>Esta plataforma exige o licenciamento de uso por computador.</p>
            <p>Para continuar utilizando os módulos profissionais, realize o pagamento para liberar o acesso:</p>
            <br>
            <h4>Beneficiário:</h4>
            <p style="font-size: 18px; font-weight: bold; color: #1E3A8A;">CAC CONTABILIZANDO</p>
            <p><b>WhatsApp para envio do comprovante:</b> +55 (64) 99304-4147</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown(
            '<div class="admin-box">', unsafe_allow_html=True
        )
        st.write("🔑 **Área do Administrador**")
        senha_admin = st.text_input(
            "Senha de Administrador:",
            type="password",
            placeholder="Digite a senha (construtech123)",
        )
        if st.button("Liberar meu Computador (Admin)", type="primary"):
            if senha_admin == "construtech123":
                st.session_state.acesso_liberado = True
                st.success("Computador liberado com sucesso!")
                st.rerun()
            else:
                st.error("Senha incorreta!")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ==========================================
# APLICAÇÃO PRINCIPAL
# ==========================================
st.markdown(
    '<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Menu Lateral
st.sidebar.title("Navegação de Módulos")
modulo = st.sidebar.selectbox(
    "Selecione a Ferramenta:",
    [
        "📊 Visão Geral e BDI",
        "🧱 Cálculo de Alvenaria",
        "🏠 Cálculo Avançado de Lajes (Novo Padrão!)",
        "⚙️ Projeto de Ferragens e Aço",
        "🏗️ Estrutural, Vigas e Validação",
        "🚰 Sistema Hidráulico Profissional",
        "💼 Faturamento e CNPJ",
    ],
)

if st.sidebar.button("🔒 Bloquear Sistema (Testar Paywall)"):
    st.session_state.acesso_liberado = False
    st.rerun()

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
            "Taxa de BDI Aplicada (%):",
            min_value=0.0,
            max_value=50.0,
            value=25.0,
        )

    if st.button("Calcular Viabilidade e Venda", type="primary"):
        total_com_bdi = st.session_state.orcamento_base * (
            1 + st.session_state.bdi / 100
        )
        lucro_estimado = total_com_bdi - st.session_state.orcamento_base
        st.markdown(
            f"""
        <div class="card">
            <h3>📊 Proposta Comercial para: {st.session_state.cliente}</h3>
            <p><b>Custo Direto Total:</b> R$ {st.session_state.orcamento_base:,.2f}</p>
            <p><b>BDI / Margem Aplicada:</b> {st.session_state.bdi}%</p>
            <hr>
            <h4><b>Preço Final de Venda Sugerido:</b> R$ {total_com_bdi:,.2f}</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 2: CÁLCULO DE ALVENARIA
# ==========================================
elif modulo == "🧱 Cálculo de Alvenaria":
    st.subheader("Dimensionamento Técnico de Alvenaria")
    area_paredes = st.number_input(
        "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
    )
    if st.button("Calcular Alvenaria", type="primary"):
        qtd_tijolos = int(area_paredes * 25 * 1.10)
        st.markdown(
            f"""
        <div class="card">
            <h4>📋 Relatório de Alvenaria ({area_paredes} m²)</h4>
            <p><b>Tijolos / Blocos (com 10% perda):</b> {qtd_tijolos} unidades</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 3: CÁLCULO DE LAJES (ATUALIZADO COM ENCHIMENTOS E PREÇOS EDITÁVEIS)
# ==========================================
elif modulo == "🏠 Cálculo Avançado de Lajes (Novo Padrão!)":
    st.subheader("Dimensionamento Técnico, Ferragens e Orçamento de Lajes")
    st.write(
        "Selecione o tipo de laje moderna ou tradicional do mercado, configure os preços unitários da sua região e calcule separado: **Material vs. Mão de Obra**."
    )

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        area_laje = st.number_input(
            "Área Total da Laje (m²):", min_value=1.0, value=60.0
        )
        tipo_laje = st.selectbox(
            "Tipo de Laje e Enchimento no Mercado:",
            [
                "Laje Pré-Moldada com EPS (Isopor) - Leve e Térmica",
                "Laje Pré-Moldada com Lajota Cerâmica Tradicional",
                "Laje Painel Treliçado Maciço (Alta Resistência / Alto Padrão)",
            ],
        )
        bitola_aco_laje = st.selectbox(
            "Especificação da Malha / Aço da Laje:",
            [
                "Tela Soldada Q-61 (Aço CA-60 - Padrão)",
                "Tela Soldada Q-92 (Reforçada para Sobrados)",
                "Ferro Adicional Negativo 6.3mm / 8.0mm",
            ],
        )

    with col_l2:
        st.markdown(
            "<b>⚙️ Custos Unitários Regionais (Editáveis):</b>",
            unsafe_allow_html=True,
        )
        preco_material_m2 = st.number_input(
            "Custo de Material da Laje por m² (R$):",
            min_value=10.0,
            value=68.00,
            step=1.00,
        )
        preco_mao_obra_laje_m2 = st.number_input(
            "Custo de Mão de Obra de Instalação por m² (R$):",
            min_value=5.0,
            value=38.00,
            step=1.00,
        )
        margem_lucro_laje = st.slider(
            "Sua Margem de Lucro Comercial (%):",
            min_value=10.0,
            max_value=60.0,
            value=30.0,
        )

    if st.button("Gerar Relatório Completo de Laje", type="primary"):
        # Cálculos técnicos automáticos
        linear_vigotas = area_laje * 1.15
        concreto_capa = area_laje * 0.065  # 6.5 cm de capa média

        if "EPS" in tipo_laje:
            qtd_enchimento = int(area_laje * 2.5)
            nome_ench = "Placas de EPS (Isopor)"
        elif "Cerâmica" in tipo_laje:
            qtd_enchimento = int(area_laje * 8.5)
            nome_ench = "Lajotas Cerâmicas"
        else:
            qtd_enchimento = 0
            nome_ench = "Painel Maciço (Sem enchimento avulso)"

        kg_aco_estimado = area_laje * (
            3.2 if "Q-61" in bitola_aco_laje else 4.8
        )

        # Custos financeiros
        total_custo_material = area_laje * preco_material_m2
        total_custo_mao_obra = area_laje * preco_mao_obra_laje_m2
        custo_direto_total = total_custo_material + total_custo_mao_obra

        preco_venda_final = custo_direto_total * (
            1 + margem_lucro_laje / 100
        )
        lucro_estimado = preco_venda_final - custo_direto_total

        st.markdown(
            f"""
        <div class="card">
            <h4>🏠 Laudo e Orçamento Técnico - Laje ({area_laje} m²)</h4>
            <p><b>Tipo Escolhido:</b> {tipo_laje}</p>
            <p><b>Especificação de Aço / Malha:</b> {bitola_aco_laje}</p>
            <hr>
            <h5><b>1. Quantitativos de Obra:</b></h5>
            <ul>
                <li>Metragem Linear de Vigotas Treliçadas: <b>{linear_vigotas:.1f} metros</b></li>
                <li>Enchimento ({nome_ench}): <b>{qtd_enchimento if qtd_enchimento > 0 else 'N/A'} unidades</b></li>
                <li>Volume de Concreto para Capa: <b>{concreto_capa:.2f} m³</b></li>
                <li>Consumo Estimado de Aço/Tela: <b>{kg_aco_estimado:.1f} kg</b></li>
            </ul>
            <hr>
            <h5><b>2. Custos Operacionais:</b></h5>
            <ul>
                <li>Custo Total de Materiais (R$ {preco_material_m2:.2f}/m²): <b>R$ {total_custo_material:,.2f}</b></li>
                <li>Custo Total de Mão de Obra (R$ {preco_mao_obra_laje_m2:.2f}/m²): <b>R$ {total_custo_mao_obra:,.2f}</b></li>
                <li><b>Custo Direto Consolidado: R$ {custo_direto_total:,.2f}</b></li>
            </ul>
            <br>
            <h2 style="color: #1E3A8A; background-color: #E0E7FF; padding: 10px; border-radius: 6px;">
                💰 Preço de Venda Sugerido (com {margem_lucro_laje}% de lucro): R$ {preco_venda_final:,.2f}
            </h2>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success(
            "Orçamento detalhado da laje gerado e auditado com sucesso!"
        )

# ==========================================
# MÓDULO 4: FERRAGENS
# ==========================================
elif modulo == "⚙️ Projeto de Ferragens e Aço":
    st.subheader("Especificação de Aço")
    st.write(
        "Módulo de detalhamento de armações para baldrames e colunas."
    )

# ==========================================
# MÓDULO 5: ESTRUTURAL
# ==========================================
elif modulo == "🏗️ Estrutural, Vigas e Validação":
    st.subheader("Auditoria de Vigas e Pilares")

# ==========================================
# MÓDULO 6: HIDRÁULICO
# ==========================================
elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Orçamento Hidráulico")

# ==========================================
# MÓDULO 7: FATURAMENTO
# ==========================================
elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Configurações Fiscais")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
