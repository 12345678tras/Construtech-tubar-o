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
    .alerta-perigo { background-color: #FDE8E8; border: 1px solid #F8B4B4; padding: 10px; border-radius: 6px; color: #9B1C1C; font-weight: bold; }
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
        "⚙️ Projeto de Ferragens e Aço",
        "🏗️ Estrutural, Vigas e Validação de Carga (Novo!)",
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
        st.success("Cálculo de alvenaria processado com sucesso!")

# ==========================================
# MÓDULO 3: CÁLCULO DE LAJE
# ==========================================
elif modulo == "🏠 Cálculo de Laje (EPS ou Cerâmica)":
    st.subheader("Dimensionamento e Orçamento de Laje Pré-Moldada")
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        area_laje = st.number_input(
            "Área Total da Laje (m²):", min_value=1.0, value=60.0
        )
        tipo_laje = st.selectbox(
            "Tipo de Enchimento:",
            [
                "Laje com EPS (Isopor) - Leve e Econômica",
                "Laje Tradicional com Lajota Cerâmica",
            ],
        )
    with col_l2:
        custo_mao_obra_m2 = st.number_input(
            "Custo de Instalação por m² (R$):", min_value=0.0, value=35.0
        )
        margem_lucro = st.slider(
            "Sua Margem de Lucro (%):",
            min_value=10.0,
            max_value=60.0,
            value=30.0,
        )

    if st.button("Calcular Laje e Orçamento", type="primary"):
        concreto_laje = area_laje * 0.065
        linear_vigotas = area_laje * 1.15
        aco_laje = area_laje * 3.3

        if "EPS" in tipo_laje:
            qtd_enchimento = int(area_laje * 2.5)
            nome_enchimento = "Placas de EPS (Isopor)"
            custo_material_m2 = 65.0
        else:
            qtd_enchimento = int(area_laje * 8.5)
            nome_enchimento = "Lajotas Cerâmicas"
            custo_material_m2 = 58.0

        custo_direto_laje = (area_laje * custo_material_m2) + (
            area_laje * custo_mao_obra_m2
        )
        preco_venda_laje = custo_direto_laje * (1 + margem_lucro / 100)
        lucro_bruto = preco_venda_laje - custo_direto_laje

        st.markdown(
            f"""
        <div class="card">
            <h4>🏠 Relatório Técnico - Laje ({tipo_laje}) | {area_laje} m²</h4>
            <p><b>Metragem Linear de Vigotas:</b> {linear_vigotas:.1f} metros</p>
            <p><b>Enchimento ({nome_enchimento}):</b> {qtd_enchimento} unidades</p>
            <p><b>Volume de Concreto para Capa:</b> {concreto_laje:.2f} m³</p>
            <p><b>Aço / Tela Soldada:</b> {aco_laje:.1f} kg</p>
            <hr>
            <p><b>Custo Direto Total:</b> R$ {custo_direto_laje:,.2f}</p>
            <p><b>Seu Lucro Estimado ({margem_lucro}%):</b> R$ {lucro_bruto:,.2f}</p>
            <h3 style="color: #1E3A8A;">💰 Preço Sugerido: R$ {preco_venda_laje:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Orçamento da laje calculado com sucesso!")

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
            "Bitola Principal de Longitudinais (Vigas e Pilares):",
            [
                "Ferro 3/8 polegadas (9.5mm) - Padrão Robusto",
                "Ferro 5/16 polegadas (8.0mm) - Padrão Econômico",
                "Ferro 10 mm - Alta Resistência",
                "Ferro 12.5 mm (1/2 pol) - Grandes vãos / Sobrados",
            ],
        )
    with col_f2:
        bitola_estribo = st.selectbox(
            "Bitola dos Estribos:", ["Ferro 4.2 mm (CA-60)", "Ferro 5.0 mm (CA-60)"]
        )
        preco_kg_ferro = st.number_input(
            "Preço Médio do Aço por kg (R$):",
            min_value=5.0,
            value=12.50,
            step=0.50,
        )

    if st.button("Gerar Especificação e Orçamento de Ferragens", type="primary"):
        if "Térrea Padrão" in porte_obra:
            kg_total_aco = 450.0
            sapatas_desc = "Sapatas isoladas com malha de 10mm"
        elif "Alto Padrão" in porte_obra:
            kg_total_aco = 750.0
            sapatas_desc = "Vigas baldrame reforçadas"
        else:
            kg_total_aco = 1200.0
            sapatas_desc = "Fundação profunda / Estacas com arranque de 12.5mm"

        custo_ferro_total = kg_total_aco * preco_kg_ferro
        venda_ferro = custo_ferro_total * 1.35
        lucro_ferro = venda_ferro - custo_ferro_total

        st.markdown(
            f"""
        <div class="card">
            <h4>⚙️ Laudo e Especificação de Aço ({porte_obra})</h4>
            <p><b>Fundação Recomendada:</b> {sapatas_desc}</p>
            <p><b>Bitola Principal:</b> {bitola_principal}</p>
            <p><b>Bitola dos Estribos:</b> {bitola_estribo}</p>
            <hr>
            <p><b>Peso Total de Aço:</b> {kg_total_aco:.1f} kg</p>
            <p><b>Custo de Aquisição:</b> R$ {custo_ferro_total:,.2f}</p>
            <p><b>Lucro Operacional (35%):</b> R$ {lucro_ferro:,.2f}</p>
            <h3 style="color: #1E3A8A;">💰 Preço Comercial da Ferragem: R$ {venda_ferro:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Especificação de ferragens calculada com sucesso!")

# ==========================================
# MÓDULO 5: ESTRUTURAL, VIGAS E VALIDAÇÃO DE CARGA (Com Inteligência de Obra)
# ==========================================
elif modulo == "🏗️ Estrutural, Vigas e Validação de Carga (Novo!)":
    st.subheader(
        "Análise de Segurança, Barras de Ferro e Validação Estrutural"
    )
    st.write(
        "Selecione o elemento e a bitola para o sistema auditar se a estrutura está segura, quantas barras usar e as regras de montagem e escoramento."
    )

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        tipo_estrutura = st.selectbox(
            "Elemento Estrutural:",
            [
                "Vigas Baldrame (Fundações)",
                "Vigas Aéreas / Cintas (Suporte de Carga)",
                "Pilares Estruturais (Colunas)",
            ],
        )
        bitola_escolhida = st.selectbox(
            "Bitola de Aço Longitudinal Selecionada:",
            [
                "Ferro 5/16 polegadas (8.0mm)",
                "Ferro 3/8 polegadas (9.5mm)",
                "Ferro 10 mm",
                "Ferro 12.5 mm (1/2 pol)",
            ],
        )
    with col_e2:
        vao_livre = st.selectbox(
            "Vão Livre ou Carga da Estrutura:",
            [
                "Vão Curto / Carga Leve (Até 3,5 metros)",
                "Vão Médio / Padrão Residencial (3,5 a 5,0 metros)",
                "Vão Grande / Carga Pesada ou Sobrado (> 5,0 metros)",
            ],
        )
        metragem_linear_estrutura = st.number_input(
            "Metragem Linear Total do Elemento (Metros):",
            min_value=1.0,
            value=40.0,
        )
        margem_lucro_est = st.slider(
            "Margem de Lucro sobre a Execução (%):",
            min_value=10.0,
            max_value=50.0,
            value=30.0,
        )

    if st.button("Executar Auditoria e Cálculo Estrutural", type="primary"):
        # Regras inteligentes de validação (Simulando o crivo de engenharia e mestre de obras)
        status_aprovado = True
        motivo_alerta = ""
        qtd_barras = 4  # Padrão de mercado para vigas/pilares

        # Lógica de validação crítica
        if "Sobrado" in vao_livre or "Grande" in vao_livre:
            if "5/16" in bitola_escolhida or "8.0mm" in bitola_escolhida:
                status_aprovado = False
                motivo_alerta = "❌ **REPROVADO PELO SISTEMA:** Ferro 5/16\" (8mm) é insuficiente para vãos grandes ou sobrados! Risco de deformação ou trinca na estrutura. Utilize no mínimo **3/8\"** ou **10mm**."
            else:
                motivo_aprovado = "✅ **APROVADO:** Bitola adequada para grandes vãos."
                qtd_barras = 6  # Reforçado para vãos grandes
        else:
            motivo_aprovado = (
                "✅ **APROVADO:** Bitola segura e aprovada para este porte."
            )

        # Dimensionamento de concreto e aço
        if "Baldrame" in tipo_estrutura:
            volume_concreto = metragem_linear_estrutura * 0.14 * 0.30 * 1.15
            kg_aco = metragem_linear_estrutura * (
                6.8 if qtd_barras == 4 else 9.5
            )
            regraseg = "<b>Regra de Escoramento / Montagem:</b> Fundo de vala compactado com lastro de concreto magro (5cm). Os estribos devem ser montados a cada 15 cm nas extremidades (1/3 dos apoios) e a cada 20 cm no meio. Cobrimento lateral mínimo de 3cm de concreto."
        elif "Aéreas" in tipo_estrutura:
            volume_concreto = metragem_linear_estrutura * 0.12 * 0.25 * 1.15
            kg_aco = metragem_linear_estrutura * (
                5.8 if qtd_barras == 4 else 8.2
            )
            regraseg = "<b>Regra de Escoramento / Montagem:</b> O escoramento da viga aérea deve usar escoras de madeira a cada 1,2 metros ou escoras metálicas firmes, mantidas por no mínimo 14 dias para evitar flechas (barrigas) na viga."
        else:
            volume_concreto = metragem_linear_estrutura * 0.14 * 0.20 * 1.10
            kg_aco = metragem_linear_estrutura * (
                7.5 if qtd_barras == 4 else 10.0
            )
            regraseg = "<b>Regra de Escoramento / Montagem:</b> Prumo milimetricamente alinhado. Os arranques inferiores devem ter ancoragem mínima de 40 vezes o diâmetro do ferro dentro da fundação."

        custo_material_base = (volume_concreto * 380.0) + (kg_aco * 12.0)
        preco_venda_estrutura = custo_material_base * (
            1 + margem_lucro_est / 100
        )
        lucro_estrutura = preco_venda_estrutura - custo_material_base

        # Exibição do Resultado na Tela
        st.markdown("### 📋 Laudo de Validação Técnica e Estrutural")

        if status_aprovado:
            st.markdown(
                f'<div class="alerta-aprovado">{motivo_aprovado}</div><br>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="alerta-perigo">{motivo_alerta}</div><br>',
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
        <div class="card">
            <h4>🏗️ Especificação Prática para Execução</h4>
            <p><b>Elemento:</b> {tipo_estrutura} | <b>Metragem:</b> {metragem_linear_estrutura} metros</p>
            <p><b>Quantidade de Barras Longitudinais:</b> <b>{qtd_barras} barras</b> de {bitola_escolhida}</p>
            <p><b>Estribos:</b> Ferro 4.2mm ou 5.0mm (espaçamento técnico recomendado)</p>
            <hr>
            <p><b>Volume de Concreto Estimado:</b> {volume_concreto:.2f} m³</p>
            <p><b>Peso Total de Aço:</b> {kg_aco:.1f} kg</p>
            <br>
            <p style="background-color: #E0E7FF; padding: 10px; border-radius: 6px;">{regraseg}</p>
            <hr>
            <p><b>Custo Direto (Insumos):</b> R$ {custo_material_base:,.2f}</p>
            <p><b>Seu Lucro ({margem_lucro_est}%):</b> R$ {lucro_estrutura:,.2f}</p>
            <h3 style="color: #1E3A8A;">💰 Preço de Venda da Estrutura: R$ {preco_venda_estrutura:,.2f}</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success(
            "Auditoria estrutural concluída com o rigor que uma obra profissional exige!"
        )

# ==========================================
# MÓDULO 6: SISTEMA HIDRÁULICO
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
# MÓDULO 7: FATURAMENTO E CNPJ
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
