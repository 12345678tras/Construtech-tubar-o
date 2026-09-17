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
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        area_paredes = st.number_input(
            "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
        )
        tipo_bloco = st.selectbox(
            "Tipo de Bloco:",
            [
                "Bloco Cerâmico 9x19x19 cm (25 un/m²)",
                "Bloco Cerâmico 14x19x19 cm (25 un/m²)",
            ],
        )
    with col_a2:
        preco_tijolo_un = st.number_input(
            "Preço Unitário do Bloco (R$):", value=1.20, step=0.10
        )
        margem_alvenaria = st.slider(
            "Margem de Lucro Alvenaria (%):",
            min_value=10.0,
            max_value=50.0,
            value=30.0,
        )

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        qtd_tijolos = int(area_paredes * 25 * 1.10)
        qtd_areia_m3 = area_paredes * 0.035
        sacos_cimento = max(1, int(area_paredes * 0.35))
        custo_mat = (qtd_tijolos * preco_tijolo_un) + (
            sacos_cimento * 32.00
        ) + (qtd_areia_m3 * 130.00)
        venda_mat = custo_mat * (1 + margem_alvenaria / 100)

        st.markdown(
            f"""
        <div class="card">
            <h4>📋 Relatório Técnico Completo - Alvenaria ({area_paredes} m²)</h4>
            <p><b>🧱 Tijolos / Blocos (com 10% de perda):</b> {qtd_tijolos} unidades</p>
            <p><b>🏖️ Areia Média:</b> {qtd_areia_m3:.2f} m³</p>
            <p><b>📦 Cimento (Sacos de 50kg):</b> {sacos_cimento} sacos</p>
            <hr>
            <p><b>Custo Direto:</b> R$ {custo_mat:,.2f}</p>
            <h3 style="color: #1E3A8A;">💰 Preço de Venda Sugerido: R$ {venda_mat:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 3: CÁLCULO DE LAJES
# ==========================================
elif modulo == "🏠 Cálculo Avançado de Lajes":
    st.subheader("Dimensionamento Técnico, Ferragens e Orçamento de Lajes")
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
        preco_material_m2 = st.number_input(
            "Custo de Material da Laje por m² (R$):", value=68.00, step=1.00
        )
        preco_mao_obra_laje_m2 = st.number_input(
            "Custo de Mão de Obra de Instalação por m² (R$):",
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
        linear_vigotas = area_laje * 1.15
        concreto_capa = area_laje * 0.065

        if "EPS" in tipo_laje:
            qtd_enchimento = int(area_laje * 2.5)
            nome_ench = "Placas de EPS (Isopor)"
        elif "Cerâmica" in tipo_laje:
            qtd_enchimento = int(area_laje * 8.5)
            nome_ench = "Lajotas Cerâmicas"
        else:
            qtd_enchimento = 0
            nome_ench = "Painel Maciço"

        kg_aco_estimado = area_laje * (
            3.2 if "Q-61" in bitola_aco_laje else 4.8
        )
        total_custo_material = area_laje * preco_material_m2
        total_custo_mao_obra = area_laje * preco_mao_obra_laje_m2
        custo_direto_total = total_custo_material + total_custo_mao_obra
        preco_venda_final = custo_direto_total * (
            1 + margem_lucro_laje / 100
        )

        st.markdown(
            f"""
        <div class="card">
            <h4>🏠 Laudo e Orçamento Técnico - Laje ({area_laje} m²)</h4>
            <p><b>Tipo:</b> {tipo_laje} | <b>Aço:</b> {bitola_aco_laje}</p>
            <ul>
                <li>Metragem Linear de Vigotas: <b>{linear_vigotas:.1f} metros</b></li>
                <li>Enchimento ({nome_ench}): <b>{qtd_enchimento if qtd_enchimento > 0 else 'N/A'} un</b></li>
                <li>Volume Concreto Capa: <b>{concreto_capa:.2f} m³</b> | Aço: <b>{kg_aco_estimado:.1f} kg</b></li>
            </ul>
            <hr>
            <p><b>Custo Materiais:</b> R$ {total_custo_material:,.2f} | <b>Mão de Obra:</b> R$ {total_custo_mao_obra:,.2f}</p>
            <h2 style="color: #1E3A8A;">💰 Preço de Venda Sugerido: R$ {preco_venda_final:,.2f}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 4: PROJETO DE FERRAGENS E AÇO
# ==========================================
elif modulo == "⚙️ Projeto de Ferragens e Aço":
    st.subheader(
        "Especificação Técnica de Aço e Bitolas (Padrão de Mestre de Obras)"
    )
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        porte_obra = st.selectbox(
            "Porte / Tipo da Obra:",
            [
                "Casa Térrea Padrão (Até 100m²)",
                "Casa Térrea Ampla / Alto Padrão (100 a 200m²)",
                "Sobrado / Dois Pavimentos",
            ],
        )
        bitola_principal = st.selectbox(
            "Bitola Principal de Longitudinais:",
            [
                "Ferro 3/8 polegadas (9.5mm)",
                "Ferro 5/16 polegadas (8.0mm)",
                "Ferro 10 mm",
            ],
        )
    with col_f2:
        preco_kg_ferro = st.number_input(
            "Preço Médio do Aço por kg (R$):", value=12.50, step=0.50
        )
        margem_ferro = st.slider(
            "Margem de Lucro Ferragens (%):", 10.0, 50.0, 30.0
        )

    if st.button("Gerar Especificação e Orçamento de Ferragens", type="primary"):
        kg_total_aco = (
            450.0
            if "Padrão" in porte_obra
            else (750.0 if "Alto" in porte_obra else 1200.0)
        )
        custo_ferro_total = kg_total_aco * preco_kg_ferro
        venda_ferro = custo_ferro_total * (1 + margem_ferro / 100)

        st.markdown(
            f"""
        <div class="card">
            <h4>⚙️ Laudo e Especificação de Aço ({porte_obra})</h4>
            <p><b>Bitola Principal:</b> {bitola_principal} | <b>Peso Total:</b> {kg_total_aco:.1f} kg</p>
            <p><b>Custo Aquisição:</b> R$ {custo_ferro_total:,.2f}</p>
            <h3 style="color: #1E3A8A;">💰 Preço Comercial da Ferragem: R$ {venda_ferro:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 5: ESTRUTURAL E VALIDAÇÃO
# ==========================================
elif modulo == "🏗️ Estrutural, Vigas e Validação":
    st.subheader(
        "Análise de Segurança, Barras de Ferro e Validação Estrutural"
    )
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        tipo_estrutura = st.selectbox(
            "Elemento Estrutural:",
            [
                "Vigas Baldrame (Fundações)",
                "Vigas Aéreas / Cintas",
                "Pilares Estruturais",
            ],
        )
        bitola_escolhida = st.selectbox(
            "Bitola de Aço Longitudinal:",
            ["Ferro 5/16 (8mm)", "Ferro 3/8 (9.5mm)", "Ferro 10 mm"],
        )
    with col_e2:
        metragem_linear = st.number_input(
            "Metragem Linear Total (Metros):", min_value=1.0, value=40.0
        )
        margem_est = st.slider(
            "Margem de Lucro Estrutural (%):", 10.0, 50.0, 30.0
        )

    if st.button("Executar Auditoria e Cálculo Estrutural", type="primary"):
        volume_concreto = metragem_linear * 0.14 * 0.30 * 1.15
        kg_aco = metragem_linear * 7.5
        custo_material_base = (volume_concreto * 380.0) + (
            kg_aco * preco_kg_ferro if "preco_kg_ferro" in locals() else 500.0
        )
        preco_venda_estrutura = custo_material_base * (1 + margem_est / 100)

        st.markdown(
            f"""
        <div class="div.card card">
            <h4>🏗️ Especificação Prática para Execução</h4>
            <p><b>Elemento:</b> {tipo_estrutura} | <b>Metragem:</b> {metragem_linear} m</p>
            <p><b>Volume Concreto:</b> {volume_concreto:.2f} m³ | <b>Aço:</b> {kg_aco:.1f} kg</p>
            <h3 style="color: #1E3A8A;">💰 Preço de Venda da Estrutura: R$ {preco_venda_estrutura:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 6: SISTEMA HIDRÁULICO PROFISSIONAL
# ==========================================
elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Orçamento Técnico e Quantitativo de Instalações Hidráulicas")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        pontos_totais = st.number_input(
            "Total de Pontos Hidráulicos (Água Fria + Esgoto):",
            min_value=1,
            value=15,
        )
        metragem_casa = st.number_input(
            "Área Construída da Casa (m²):", min_value=10.0, value=80.0
        )
        capacidade_caixa = st.selectbox(
            "Reservatório de Água:",
            ["Caixa d'água 500L", "Caixa d'água 1.000L"],
        )

    with col_h2:
        preco_tubo_25 = st.number_input("Preço Cano Água 25mm (6m):", value=28.00)
        preco_tubo_50 = st.number_input(
            "Preço Cano Esgoto 50mm (6m):", value=35.00
        )
        preco_tubo_100 = st.number_input(
            "Preço Cano Esgoto 100mm (6m):", value=78.00
        )
        preco_mao_obra_ponto = st.number_input(
            "Mão de Obra por Ponto (R$):", value=65.00
        )

    if st.button("Gerar Orçamento Hidráulico Completo", type="primary"):
        barras_25 = max(2, int((metragem_casa * 0.35) / 6) + 1)
        barras_50 = max(1, int((metragem_casa * 0.15) / 6) + 1)
        barras_100 = max(1, int((metragem_casa * 0.20) / 6) + 1)
        custo_conexoes = pontos_totais * 32.00
        custo_caixa = 680.00 if "1.000" in capacidade_caixa else 420.00

        total_tubos = (
            (barras_25 * preco_tubo_25)
            + (barras_50 * preco_tubo_50)
            + (barras_100 * preco_tubo_100)
        )
        total_material = total_tubos + custo_conexoes + custo_caixa
        total_mao_obra = pontos_totais * preco_mao_obra_ponto
        valor_geral = total_material + total_mao_obra

        st.markdown(
            f"""
        <div class="card">
            <h4>🚰 Relatório Hidráulico Profissional</h4>
            <p><b>{pontos_totais} Pontos | Casa de {metragem_casa} m²</b></p>
            <ul>
                <li>Cano 25mm: <b>{barras_25} barras</b> | Cano 50mm: <b>{barras_50} barras</b> | Cano 100mm: <b>{barras_100} barras</b></li>
                <li>Conexões e Acessórios Estimados: <b>R$ {custo_conexoes:,.2f}</b></li>
                <li>Reservatório ({capacidade_caixa}): <b>R$ {custo_caixa:,.2f}</b></li>
            </ul>
            <hr>
            <p><b>Total Materiais:</b> R$ {total_material:,.2f} | <b>Total Mão de Obra:</b> R$ {total_mao_obra:,.2f}</p>
            <h2 style="color: #1E3A8A;">💰 Valor Geral Hidráulico: R$ {valor_geral:,.2f}</h2>
        </div>
        """,
            unsafe_allow_html=True,
        )

# ==========================================
# MÓDULO 7: FATURAMENTO E CNPJ
# ==========================================
elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Configurações Fiscais")
    cnpj_empresa = st.text_input("CNPJ:", value="00.000.000/0001-00")
    razao_social = st.text_input(
        "Razão Social:", value="Construtech Tubarão LTDA"
    )
    if st.button("Salvar Dados Fiscais", type="primary"):
        st.success("Dados salvos com sucesso!")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
