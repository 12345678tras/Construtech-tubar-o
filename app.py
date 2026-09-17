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
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #1E3A8A; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 30px; border-radius: 10px; text-align: center; }
    .admin-box { background-color: #EFF6FF; border: 1px solid #3B82F6; padding: 15px; border-radius: 8px; margin-top: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# SISTEMA DE CONTROLE DE ACESSO (PAYWALL + ADMIN)
# ==========================================
if "acesso_liberado" not in st.session_state:
    st.session_state.acesso_liberado = False

# Tela de Bloqueio
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
            <p>Para continuar utilizando os módulos profissionais, escaneie o QR Code ou realize o Pix para os dados abaixo:</p>
            <br>
            <h4>Beneficiário:</h4>
            <p style="font-size: 18px; font-weight: bold; color: #1E3A8A;">CAC CONTABILIZANDO</p>
            <p><b>WhatsApp para envio do comprovante:</b> +55 (64) 99304-4147</p>
            <p><i>(Processado via InfinitePay)</i></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # SEÇÃO EXCLUSIVA PARA VOCÊ (DONO/ADMINISTRADOR)
    with st.container():
        st.markdown(
            '<div class="admin-box">', unsafe_allow_html=True
        )
        st.write("🔑 **Área do Desenvolvedor / Dono da Plataforma**")
        senha_admin = st.text_input(
            "Digite sua senha de Administrador para liberar seu computador:",
            type="password",
            placeholder="Digite a senha (construtech123)",
        )

        SENHA_MESTRE = "construtech123"

        if st.button("Liberar meu Computador (Admin)", type="primary"):
            if senha_admin == SENHA_MESTRE:
                st.session_state.acesso_liberado = True
                st.success(
                    "Computador reconhecido como Administrador! Entrando..."
                )
                st.rerun()
            else:
                st.error("Senha de administrador incorreta!")
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ==========================================
# APLICAÇÃO PRINCIPAL (Liberada)
# ==========================================

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
        "🧱 Cálculo de Alvenaria",
        "🏠 Cálculo de Laje",
        "🏗️ Estrutural e Vigas",
        "🚰 Sistema Hidráulico",
        "💼 Faturamento e CNPJ",
    ],
)

# Botão na barra lateral para bloquear novamente se precisar testar
if st.sidebar.button("🔒 Bloquear Sistema (Testar Paywall)"):
    st.session_state.acesso_liberado = False
    st.rerun()

# Controle de Sessão
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
            "Taxa de BDI Aplicada (% - Lucro e Despesas Indiretas):",
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
            <p><b>Custo Direto (Insumos/Mão de Obra):</b> R$ {st.session_state.orcamento_base:,.2f}</p>
            <p><b>BDI Aplicado:</b> {st.session_state.bdi}%</p>
            <p><b>Margem / Despesas Indiretas Estimadas:</b> R$ {lucro_estimado:,.2f}</p>
            <hr>
            <h4><b>Preço Final de Venda Sugerido:</b> R$ {total_com_bdi:,.2f}</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo financeiro consolidado com sucesso!")

# ==========================================
# MÓDULO 2: CÁLCULO DE ALVENARIA (Melhorado)
# ==========================================
elif modulo == "🧱 Cálculo de Alvenaria":
    st.subheader("Dimensionamento Técnico de Alvenaria (Blocos e Argamassa)")
    st.write(
        "Informe os dados da área de paredes para calcular com precisão os insumos."
    )

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        area_paredes = st.number_input(
            "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
        )
    with col_a2:
        tipo_bloco = st.selectbox(
            "Tipo de Bloco Cerâmico:",
            [
                "Bloco 9x19x19 cm (25 un/m²)",
                "Bloco 14x19x19 cm (25 un/m²)",
            ],
        )

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        # Parâmetros de engenharia: 25 blocos por m² + 10% de quebra/perda
        qtd_bruta_tijolos = area_paredes * 25 * 1.10
        # Argamassa de assentamento: ~18 kg por m² de parede
        qtd_argamassa_kg = area_paredes * 18.0
        sacos_cimento_alv = (
            qtd_argamassa_kg / 250
        ) * 50  # Estimativa de proporção em sacos de 50kg

        st.markdown(
            f"""
        <div class="card">
            <h4>📋 Relatório Técnico - Alvenaria ({area_paredes} m²)</h4>
            <p><b>Quantidade de Blocos (com 10% de margem de perda):</b> {int(qtd_bruta_tijolos)} unidades</p>
            <p><b>Argamassa de Assentamento Estimada:</b> {qtd_argamassa_kg:.1f} kg</p>
            <p><b>Sacos de Cimento (50kg) para Argamassa:</b> aprox. {max(1, int(sacos_cimento_alv))} sacos</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo de alvenaria processado com sucesso!")

# ==========================================
# MÓDULO 3: CÁLCULO DE LAJE (Melhorado)
# ==========================================
elif modulo == "🏠 Cálculo de Laje":
    st.subheader("Dimensionamento de Laje Pré-Moldada (Vigotas e Concreto)")
    area_laje = st.number_input(
        "Área Total da Laje (m²):", min_value=1.0, value=50.0
    )
    sobrecarga = st.selectbox(
        "Uso da Laje / Sobrecarga:",
        ["Residencial (150 kg/m²)", "Comercial / Laje acessível (200 kg/m²)"],
    )

    if st.button("Calcular Materiais da Laje", type="primary"):
        # Concreto para capa de 4cm a 5cm: ~0.05 m3 a 0.08 m3 por m²
        concreto_laje = area_laje * 0.065
        # Vigotas pré-moldadas: proporcional ao vão (média de 1.1 m linear por m²)
        linear_vigotas = area_laje * 1.15
        # Aço (Tela soldada Q-61 / Q-92): aprox 3.2 kg por m²
        aco_laje = area_laje * 3.3

        st.markdown(
            f"""
        <div class="card">
            <h4>🏠 Relatório Técnico - Laje ({area_laje} m²)</h4>
            <p><b>Volume de Concreto para Capa (fck >= 25 MPa):</b> {concreto_laje:.2f} m³</p>
            <p><b>Metragem Linear de Vigotas Pré-moldadas:</b> {linear_vigotas:.1f} metros</p>
            <p><b>Aço / Tela Soldada Estrutural:</b> {aco_laje:.1f} kg</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo de laje processado com sucesso!")

# ==========================================
# MÓDULO 4: ESTRUTURAL E VIGAS (Melhorado)
# ==========================================
elif modulo == "🏗️ Estrutural e Vigas":
    st.subheader("Dimensionamento Estimado de Concreto e Aço Estrutural")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        vao_livre = st.slider(
            "Maior Vão Livre das Vigas (metros):",
            min_value=2.0,
            max_value=10.0,
            value=4.0,
        )
    with col_e2:
        pavimentos = st.number_input(
            "Número de Pavimentos da Estrutura:",
            min_value=1,
            max_value=5,
            value=1,
        )

    if st.button("Calcular Estrutura Completa", type="primary"):
        # Base de cálculo estrutural ajustada por vão e pavimentos
        volume_concreto = vao_livre * pavimentos * 0.42
        peso_aco = volume_concreto * 95.0  # Consumo médio de aço CA-50 por m³

        st.markdown(
            f"""
        <div class="card">
            <h4>🏗️ Relatório Estrutural (Vigas, Pilares e Fundações)</h4>
            <p><b>Vão Referência:</b> {vao_livre} metros | <b>Pavimentos:</b> {pavimentos}</p>
            <p><b>Volume Total Estimado de Concreto:</b> {volume_concreto:.2f} m³</p>
            <p><b>Consumo Estimado de Aço (CA-50/CA-60):</b> {peso_aco:.2f} kg</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Estimativa estrutural calculada com sucesso!")

# ==========================================
# MÓDULO 5: SISTEMA HIDRÁULICO (Melhorado)
# ==========================================
elif modulo == "🚰 Sistema Hidráulico":
    st.subheader("Orçamento Técnico de Instalações Hidráulicas (Água e Esgoto)")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        pontos_agua = st.number_input(
            "Total de Pontos (Água Fria, Quente e Esgoto):",
            min_value=1,
            value=12,
        )
    with col_h2:
        capacidade_caixa = st.selectbox(
            "Capacidade do Reservatório (Caixa D'água):",
            ["1.000 Litros", "1.500 Litros", "2.000 Litros", "Sem Reservatório"],
        )

    if st.button("Calcular Orçamento Hidráulico", type="primary"):
        # Custos médios de mercado por ponto hidráulico (tubos PVC, conexões, registros, joelhos)
        custo_materiais_hid = pontos_agua * 55.0

        if "1.000" in capacidade_caixa:
            custo_caixa = 680.0
        elif "1.500" in capacidade_caixa:
            custo_caixa = 980.0
        elif "2.000" in capacidade_caixa:
            custo_caixa = 1350.0
        else:
            custo_caixa = 0.0

        total_hidraulico = custo_materiais_hid + custo_caixa

        st.markdown(
            f"""
        <div class="card">
            <h4>🚰 Resumo do Orçamento Hidráulico</h4>
            <p><b>Tubulações, Conexões e Registros ({pontos_agua} pontos):</b> R$ {custo_materiais_hid:,.2f}</p>
            <p><b>Reservatório ({capacidade_caixa}):</b> R$ {custo_caixa:,.2f}</p>
            <hr>
            <h4><b>Custo Parcial Hidráulico Estimado:</b> R$ {total_hidraulico:,.2f}</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Orçamento hidráulico processado com sucesso!")

# ==========================================
# MÓDULO 6: FATURAMENTO E CNPJ
# ==========================================
elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Configurações de Faturamento e Dados Comerciais")
    cnpj_empresa = st.text_input(
        "CNPJ da Empresa:",
        value="00.000.000/0001-00",
        placeholder="XX.XXX.XXX/0001-XX",
    )
    razao_social = st.text_input(
        "Razão Social / Nome do Responsável Técnico:",
        value="Construtech Tubarão LTDA",
    )
    chave_pix = st.text_input(
        "Chave Pix Comercial:", value="contato@construtechtubarao.com.br"
    )

    if st.button("Salvar Dados Fiscais", type="primary"):
        st.success(
            f"Dados da empresa {razao_social} (CNPJ: {cnpj_empresa}) salvos e vinculados aos relatórios!"
        )

# Rodapé institucional
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
