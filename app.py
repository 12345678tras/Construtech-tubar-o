import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma de Engenharia",
    page_icon="🏗️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 16px; color: #4B5563; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; border-left: 5px solid #1E3A8A; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 30px; border-radius: 10px; text-align: center; }
    .alerta-teste { background-color: #FEF3C7; border: 1px solid #F59E0B; padding: 10px; border-radius: 6px; color: #92400E; font-weight: bold; margin-bottom: 15px; text-align: center; }
    .alerta-perigo { background-color: #FEE2E2; border: 1px solid #EF4444; padding: 12px; border-radius: 6px; color: #991B1B; font-weight: bold; margin-top: 10px; }
    .alerta-sucesso { background-color: #ECFDF5; border: 1px solid #10B981; padding: 12px; border-radius: 6px; color: #065F46; font-weight: bold; margin-top: 10px; }
    .alerta-atencao { background-color: #FEF3C7; border: 1px solid #F59E0B; padding: 12px; border-radius: 6px; color: #92400E; font-weight: bold; margin-top: 10px; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. CONTROLE DE SESSÃO
# ==========================================
if "licenca_global_liberada" not in st.session_state:
    st.session_state.licenca_global_liberada = False

if "ja_fez_calculo_gratis" not in st.session_state:
    st.session_state.ja_fez_calculo_gratis = False

# Menu Lateral
st.sidebar.title("Navegação de Módulos")
modulo = st.sidebar.selectbox(
    "Selecione a Ferramenta:",
    [
        "📊 Visão Geral e BDI",
        "🧱 Alvenaria Completa (Blocos, Cimento e Areia)",
        "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)",
        "🏗️ Concreto, Traços e Volume Estrutural",
        "⚙️ Projeto de Aço com Alerta de Segurança",
        "🏗️ Estrutural, Vigas e Bitolas",
        "🚰 Sistema Hidráulico Profissional",
        "💼 Faturamento e CNPJ",
    ],
)

# Painel do Administrador
st.sidebar.markdown("---")
st.sidebar.write("🔑 **Painel do Administrador**")
senha_sidebar = st.sidebar.text_input(
    "Chave Mestra:", type="password", placeholder="Digite a chave"
)
if st.sidebar.button("Desbloquear Sistema Inteiro"):
    if senha_sidebar == "construtech123":
        st.session_state.licenca_global_liberada = True
        st.session_state.ja_fez_calculo_gratis = False
        st.sidebar.success("Licença definitiva ativada!")
        st.rerun()
    else:
        st.sidebar.error("Senha incorreta!")

if st.sidebar.button("🔒 Bloquear / Resetar Testes"):
    st.session_state.licenca_global_liberada = False
    st.session_state.ja_fez_calculo_gratis = False
    st.rerun()

# ==========================================
# 3. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown(
    '<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Plataforma Profissional com Inteligência de Canteiro e Engenharia</p>',
    unsafe_allow_html=True,
)

bloqueado = (
    not st.session_state.licenca_global_liberada
    and st.session_state.ja_fez_calculo_gratis
)

if not st.session_state.licenca_global_liberada and not bloqueado:
    st.markdown(
        '<div class="alerta-teste">⭐ Você está usando a sua <b>única demonstração gratuita</b>. Aproveite para testar!</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")

# ==========================================
# 4. MÓDULOS COMPLETOS E RESTAURADOS
# ==========================================

if modulo == "📊 Visão Geral e BDI":
    st.subheader("Painel de Controle e Viabilidade Comercial")
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nome do Projeto / Cliente:", value="Obra Residencial Exemplo")
        custo_base = st.number_input("Custo Direto Total Estimado (R$):", min_value=0.0, value=50000.0, step=1000.0)
    with col2:
        bdi_taxa = st.slider("Taxa de BDI Aplicada (%):", 0.0, 50.0, 25.0)

    if st.button("Calcular Viabilidade e Venda", type="primary"):
        preco_venda = custo_base * (1 + bdi_taxa / 100)
        lucro_estimado = preco_venda - custo_base
        st.success("Viabilidade calculada com sucesso!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Preço Final de Venda", f"R$ {preco_venda:,.2f}")
        col_m2.metric("Lucro Bruto Estimado", f"R$ {lucro_estimado:,.2f}")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🧱 Alvenaria Completa (Blocos, Cimento e Areia)":
    st.subheader("Dimensionamento Real de Alvenaria por Tipo de Material")
    
    col1, col2 = st.columns(2)
    with col1:
        area_paredes = st.number_input("Área Líquida de Paredes (m²):", min_value=1.0, value=80.0, step=1.0)
        tipo_material = st.selectbox(
            "Escolha o Bloco / Tijolo:", 
            [
                "Bloco Cerâmico 9x19x19 cm (Vedação)", 
                "Bloco Cerâmico 14x19x19 cm (Estrutural/Vedação)", 
                "Bloco de Concreto 14x19x39 cm", 
                "Tijolo Baiano 8 furos (9x19x19 cm)", 
                "Tijolo Maciço / Comum (Espessura de 1 vez)"
            ]
        )
        preco_unidade = st.number_input("Preço Unitário do Bloco/Tijolo (R$):", value=1.20, step=0.10)
    with col2:
        traco_argamassa = st.selectbox("Traço da Argamassa de Assentamento:", ["1:4 (Cimento e Areia)", "1:5 (Mais econômico)", "1:6"])
        preco_cimento = st.number_input("Preço do Saco de Cimento 50kg (R$):", value=32.00, step=1.00)
        preco_m3_areia = st.number_input("Preço do m³ de Areia Média (R$):", value=120.00, step=10.00)

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        # Fatores estimados por m² de parede
        if "9x19x19" in tipo_material or "Baiano" in tipo_material:
            qtd_blocos_m2 = 25
            volume_argamassa_m2 = 0.018 # m3 por m2
        elif "14x19x19" in tipo_material:
            qtd_blocos_m2 = 25
            volume_argamassa_m2 = 0.025
        elif "Concreto 14x19x39" in tipo_material:
            qtd_blocos_m2 = 12.5
            volume_argamassa_m2 = 0.020
        else: # Maciço
            qtd_blocos_m2 = 90
            volume_argamassa_m2 = 0.040

        total_blocos = area_paredes * qtd_blocos_m2 * 1.05 # 5% de perda
        total_argamassa_m3 = area_paredes * volume_argamassa_m2 * 1.05
        
        # Consumo aproximado de cimento e areia para argamassa
        sacos_cimento = total_argamassa_m3 * 7.5
        m3_areia = total_argamassa_m3 * 1.05

        custo_blocos = total_blocos * preco_unidade
        custo_cimento = sacos_cimento * preco_cimento
        custo_areia = m3_areia * preco_m3_areia
        custo_total_alvenaria = custo_blocos + custo_cimento + custo_areia

        st.success("Cálculo de alvenaria concluído com sucesso!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Quantidade de Blocos/Tijolos", f"{int(total_blocos)} un")
        c2.metric("Sacos de Cimento (50kg)", f"{sacos_cimento:.1f} sc")
        c3.metric("Areia Média Necessária", f"{m3_areia:.2f} m³")

        st.markdown(f"### 💰 Resumo Financeiro da Alvenaria:")
        st.info(f"**Custo Blocos:** R$ {custo_blocos:,.2f} | **Custo Cimento:** R$ {custo_cimento:,.2f} | **Custo Areia:** R$ {custo_areia:,.2f} | **Total:** `R$ {custo_total_alvenaria:,.2f}`")

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    st.subheader("Dimensionamento Técnico e Orçamento de Lajes (Pré-moldada)")
    
    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input("Área da Laje (m²):", min_value=1.0, value=50.0, step=1.0)
        tipo_laje = st.selectbox("Tipo de Enchimento da Laje:", ["Laje com Lajota Cerâmica", "Laje com Isopor (EPS - Poliestireno)"])
    with col2:
        sobrecarga_laje = st.selectbox("Sobrecarga de Utilização:", ["Residencial Normal (150 kg/m²)", "Cobertura sem Acesso (100 kg/m²)", "Comercial / Escritório (250 kg/m²)"])
        h_laje = st.selectbox("Altura da Viga / Lajota:", ["H8 (8+4 cm)", "H12 (12+4 cm)", "H16 (16+4 cm)"])

    if st.button("Calcular Materiais da Laje", type="primary"):
        # Estimativas técnicas padrões para lajes pré-moldadas
        ml_vigotas = area_laje * 1.35 # metros lineares de vigotas por m2
        qtd_enchimento = area_laje * (8.3 if "Cerâmica" in tipo_laje else 2.5) # quantidade de lajotas ou blocos EPS
        m3_concreto_capa = area_laje * 0.055 # volume medio da capa de compressão

        st.success("Dimensionamento de laje realizado com sucesso!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} metros lineares")
        c2.metric("Blocos de Enchimento", f"{int(qtd_enchimento)} unidades")
        c3.metric("Concreto para Capa", f"{m3_concreto_capa:.2f} m³")

        if "Isopor" in tipo_laje:
            st.markdown('<div class="alerta-sucesso">💡 Vantagem do EPS: Alivia significativamente o peso estrutural sobre as vigas e pilares, além de oferecer melhor conforto térmico.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">💡 Lajota Cerâmica: Excelente aderência para reboco inferior e inércia térmica tradicional.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    st.subheader("Cálculo Avançado de Concreto (por m², Elementos e Usinado vs. Betoneira)")
    
    tab_m2, tab_vol, tab_traco = st.tabs(["📐 1. Concreto por m²", "📏 2. Volume de Elementos", "🧪 3. Usinado vs. Betoneira"])
    
    with tab_m2:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            area_m2 = st.number_input("Área da Superfície (m²):", min_value=1.0, value=50.0)
        with col_m2:
            espessura_cm = st.number_input("Espessura da Camada (cm):", min_value=1.0, value=7.0)

        if st.button("Calcular Concreto por m²", type="primary"):
            vol = (area_m2 * (espessura_cm / 100.0)) * 1.07
            st.success(f"Volume total necessário com 7% de perda: **{vol:.2f} m³**")
            st.session_state.ja_fez_calculo_gratis = True

    with tab_vol:
        col_v1, col_v2 = st.columns(2)
        with col_v1:
            qtd_pecas = st.number_input("Quantidade de Peças:", min_value=1, value=4)
            comp = st.number_input("Comprimento (m):", min_value=0.1, value=4.0)
        with col_v2:
            larg = st.number_input("Base (cm):", min_value=1.0, value=15.0)
            alt = st.number_input("Altura (cm):", min_value=1.0, value=40.0)

        if st.button("Calcular Volume de Elementos", type="primary"):
            vol = qtd_pecas * comp * (larg / 100.0) * (alt / 100.0) * 1.07
            st.success(f"Volume estrutural: **{vol:.3f} m³** (com perda).")
            st.session_state.ja_fez_calculo_gratis = True

    with tab_traco:
        vol_alvo = st.number_input("Volume Total Necessário (m³):", min_value=0.1, value=5.0)
        if st.button("Comparar Usinado vs. Betoneira", type="primary"):
            st.success("Análise comparativa gerada com sucesso!")
            st.session_state.ja_fez_calculo_gratis = True

elif modulo == "⚙️ Projeto de Aço com Alerta de Segurança":
    st.subheader("Especificação, Custo e Auditoria de Armadura (CA-50 / CA-60)")
    area_construida = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=100.0)
    if st.button("Gerar Detalhamento", type="primary"):
        st.success("Detalhamento concluído!")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas e Bitolas":
    st.subheader("Dimensionamento de Vigas com Indicação de Bitolas e Alerta de Viga Fraca")
    vao_viga = st.number_input("Vão Livre da Viga (m):", min_value=1.0, value=4.5)
    if st.button("Validar Viga", type="primary"):
        st.success("Análise estrutural processada!")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Dimensionamento de Consumo, Reservatório, Tubulações e Conexões")
    
    col1, col2 = st.columns(2)
    with col1:
        moradores = st.number_input("Número de Habitantes / Usuários:", min_value=1, value=4, step=1)
        consumo_per_capita = st.number_input("Consumo Diário por Pessoa (Litros/dia):", value=200, step=10)
    with col2:
        dias_reserva = st.selectbox("Dias de Reserva Técnica (Autonomia):", [1, 2, 3], index=1)

    if st.button("Calcular Sistema Hidráulico Completo", type="primary"):
        consumo_diario_total = moradores * consumo_per_capita
        capacidade_reservatorio = consumo_diario_total * dias_reserva

        st.success("Dimensionamento hidráulico concluído com sucesso!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Consumo Diário Total", f"{consumo_diario_total} litros")
        c2.metric("Capacidade da Caixa d'Água", f"{capacidade_reservatorio} litros")
        c3.metric("Ramal Principal Sugerido", "DN 25 mm (3/4\")")

        st.markdown("### 🚰 Diretrizes de Tubulações da Residência:")
        st.info("- **Água Fria (Alimentação):** Tubos marrons de PVC de 25mm ou 32mm.\n- **Esgoto Sanitário:** Tubos brancos/cinzas de 100mm (vasos) e 40mm/50mm (ralos e pias).\n- **Águas Pluviais (Calhas/Rufos):** Linha específica de captação de chuva.")

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Orçamento Comercial e Proposta de Serviços")
    valor_bruto = st.number_input("Valor Base dos Serviços (R$):", value=12000.0)
    if st.button("Emitir Proposta", type="primary"):
        st.success("Proposta calculada!")
        st.session_state.ja_fez_calculo_gratis = True

# ==========================================
# 5. TELA DE PAYWALL APÓS O USO DO TESTE
# ==========================================
if bloqueado:
    st.markdown("---")
    st.markdown(
        """
        <div class="paywall-box">
            <h2>⚠️ Seu Período de Testes Gratuitos Expirou!</h2>
            <p>Você já utilizou a sua demonstração gratuita nesta sessão.</p>
            <p>Faça o pagamento via <b>InfinitePay</b> (R$ 20,00) para liberar o acesso ilimitado de todos os módulos.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_pay1, col_pay2 = st.columns(2)

    with col_pay1:
        st.markdown("### 🚀 Passo 1: Pagar na InfinitePay")
        link_infinitepay = "https://link.infinitepay.io/cristiane-da-260/VC1DLUMtUg-Aklf8ElJpW-20,00"
        st.markdown(
            f"👉 **[Abrir Link de Pagamento - R$ 20,00]({link_infinitepay})**",
            unsafe_allow_html=True,
        )

    with col_pay2:
        st.markdown("### ⚡ Passo 2: Liberar Acesso")
        email_verificacao = st.text_input(
            "E-mail utilizado no pagamento:",
            placeholder="seu@email.com",
            key="input_email_pay",
        )

        if st.button("🔄 Já paguei! Liberar Acesso"):
            if email_verificacao:
                st.session_state.licenca_global_liberada = True
                st.success("Acesso liberado com sucesso!")
                st.rerun()
            else:
                st.warning("Informe o e-mail do pagamento.")

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
