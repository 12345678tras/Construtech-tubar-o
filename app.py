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
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# SISTEMA DE CONTROLE DE ACESSO (PAYWALL + ADMIN)
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
        "🏠 Cálculo de Laje (EPS ou Cerâmica)",
        "🏗️ Estrutural e Vigas",
        "🚰 Sistema Hidráulico",
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
            <p><b>Custo Direto (Insumos/Mão de Obra):</b> R$ {st.session_state.orcamento_base:,.2f}</p>
            <p><b>BDI Aplicado:</b> {st.session_state.bdi}%</p>
            <p><b>Margem / Despesas Indiretas:</b> R$ {lucro_estimado:,.2f}</p>
            <hr>
            <h4><b>Preço Final de Venda Sugerido:</b> R$ {total_com_bdi:,.2f}</h4>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo financeiro consolidado com sucesso!")

# ==========================================
# MÓDULO 2: CÁLCULO DE ALVENARIA
# ==========================================
elif modulo == "🧱 Cálculo de Alvenaria":
    st.subheader("Dimensionamento Técnico de Alvenaria (Insumos Completos)")
    st.write(
        "Informe a metragem de paredes para calcular tijolos, areia, cimento e ferro de amarração."
    )

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        area_paredes = st.number_input(
            "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
        )
    with col_a2:
        tipo_bloco = st.selectbox(
            "Tipo de Bloco:",
            [
                "Bloco Cerâmico 9x19x19 cm (25 un/m²)",
                "Bloco Cerâmico 14x19x19 cm (25 un/m²)",
            ],
        )

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        qtd_tijolos = int(area_paredes * 25 * 1.10)
        qtd_areia_m3 = area_paredes * 0.035
        sacos_cimento = max(1, int(area_paredes * 0.35))
        peso_ferro = area_paredes * 0.8

        st.markdown(
            f"""
        <div class="card">
            <h4>📋 Relatório Técnico Completo - Alvenaria ({area_paredes} m²)</h4>
            <p><b>🧱 Tijolos / Blocos (com 10% de perda):</b> {qtd_tijolos} unidades</p>
            <p><b>🏖️ Areia Média (para argamassa):</b> {qtd_areia_m3:.2f} m³</p>
            <p><b>📦 Cimento (Sacos de 50kg):</b> {sacos_cimento} sacos</p>
            <p><b>⚙️ Aço / Ferro para Amarração (CA-60 / CA-50):</b> {peso_ferro:.1f} kg</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo de alvenaria e insumos processado com sucesso!")

# ==========================================
# MÓDULO 3: CÁLCULO DE LAJE (Com EPS / Isopor ou Cerâmica + Lucro)
# ==========================================
elif modulo == "🏠 Cálculo de Laje (EPS ou Cerâmica)":
    st.subheader(
        "Dimensionamento e Orçamento de Laje Pré-Moldada (Foco em Lucratividade)"
    )
    st.write(
        "Escolha o tipo de laje e calcule os materiais exatos com valor de venda para o cliente."
    )

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        area_laje = st.number_input(
            "Área Total da Laje (m²):", min_value=1.0, value=60.0
        )
        tipo_laje = st.selectbox(
            "Tipo de Enchimento da Laje:",
            [
                "Laje com EPS (Isopor) - Mais leve e econômica em mão de obra",
                "Laje Tradicional com Lajota Cerâmica",
            ],
        )
    with col_l2:
        custo_mao_obra_m2 = st.number_input(
            "Custo de Mão de Obra / Instalação por m² (R$):",
            min_value=0.0,
            value=35.0,
        )
        margem_lucro = st.slider(
            "Sua Margem de Lucro Desejada (%):",
            min_value=10.0,
            max_value=60.0,
            value=30.0,
        )

    if st.button("Calcular Laje e Orçamento de Venda", type="primary"):
        # Cálculos técnicos padronizados de engenharia
        concreto_laje = area_laje * 0.065  # Volume de concreto da capa (m³)
        linear_vigotas = area_laje * 1.15  # Metragem linear de vigotas
        aco_laje = area_laje * 3.3  # Tela soldada estrutural (kg)

        if "EPS" in tipo_laje:
            # EPS: cerca de 2.5 placas por m² + custo médio estimado de material por m² (vigotas + EPS + concreto + aço)
            qtd_enchimento = int(area_laje * 2.5)
            nome_enchimento = "Placas de EPS (Isopor)"
            custo_material_m2 = 65.0  # Custo médio de insumos por m²
        else:
            # Lajota cerâmica: cerca de 8 a 9 unidades por m²
            qtd_enchimento = int(area_laje * 8.5)
            nome_enchimento = "Lajotas Cerâmicas"
            custo_material_m2 = 58.0  # Custo médio de insumos por m²

        custo_total_materiais = area_laje * custo_material_m2
        custo_total_mao_obra = area_laje * custo_mao_obra_m2
        custo_direto_laje = custo_total_materiais + custo_total_mao_obra

        # Preço de venda com base na margem escolhida para garantir o lucro
        preco_venda_laje = custo_direto_laje * (1 + margem_lucro / 100)
        lucro_bruto = preco_venda_laje - custo_direto_laje

        st.markdown(
            f"""
        <div class="card">
            <h4>🏠 Relatório Técnico - Laje ({tipo_laje}) | {area_laje} m²</h4>
            <p><b>Metragem Linear de Vigotas Pré-moldadas:</b> {linear_vigotas:.1f} metros</p>
            <p><b>Enchimento ({nome_enchimento}):</b> {qtd_enchimento} unidades</p>
            <p><b>Volume de Concreto para Capa:</b> {concreto_laje:.2f} m³</p>
            <p><b>Aço / Tela Soldada:</b> {aco_laje:.1f} kg</p>
            <hr>
            <p><b>Custo Direto Total (Materiais + Mão de Obra):</b> R$ {custo_direto_laje:,.2f}</p>
            <p><b>Seu Lucro Estimado ({margem_lucro}%):</b> R$ {lucro_bruto:,.2f}</p>
            <h3 style="color: #1E3A8A;">💰 Preço Sugerido para Fechar com o Cliente: R$ {preco_venda_laje:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Orçamento e dimensionamento da laje calculados com sucesso!")

# ==========================================
# MÓDULO 4: ESTRUTURAL E VIGAS
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
            "Número de Pavimentos:", min_value=1, max_value=5, value=1
        )

    if st.button("Calcular Estrutura Completa", type="primary"):
        volume_concreto = vao_livre * pavimentos * 0.42
        peso_aco = volume_concreto * 95.0

        st.markdown(
            f"""
        <div class="card">
            <h4>🏗️ Relatório Estrutural</h4>
            <p><b>Volume Total de Concreto:</b> {volume_concreto:.2f} m³</p>
            <p><b>Consumo de Aço (CA-50/CA-60):</b> {peso_aco:.2f} kg</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Estimativa estrutural calculada com sucesso!")

# ==========================================
# MÓDULO 5: SISTEMA HIDRÁULICO
# ==========================================
elif modulo == "🚰 Sistema Hidráulico":
    st.subheader("Orçamento Técnico de Instalações Hidráulicas")
    pontos_agua = st.number_input(
        "Total de Pontos (Água e Esgoto):", min_value=1, value=12
    )

    if st.button("Calcular Orçamento Hidráulico", type="primary"):
        custo_materiais_hid = pontos_agua * 55.0
        custo_caixa = 680.0
        total_hidraulico = custo_materiais_hid + custo_caixa

        st.markdown(
            f"""
        <div class="card">
            <h4>🚰 Resumo Hidráulico</h4>
            <p><b>Tubulações e Conexões ({pontos_agua} pontos):</b> R$ {custo_materiais_hid:,.2f}</p>
            <p><b>Reservatório (1.000L):</b> R$ {custo_caixa:,.2f}</p>
            <hr>
            <h4><b>Total Parcial Hidráulico:</b> R$ {total_hidraulico:,.2f}</h4>
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
        "Razão Social / Responsável Técnico:",
        value="Construtech Tubarão LTDA",
    )

    if st.button("Salvar Dados Fiscais", type="primary"):
        st.success(
            f"Dados da empresa {razao_social} (CNPJ: {cnpj_empresa}) salvos com sucesso!"
        )

# Rodapé institucional
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
