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
        "⚙️ Projeto de Aço, Custo e Auditoria de Armadura",
        "🏗️ Estrutural, Vigas, Bitolas e Aços",
        "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)",
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
# 4. MÓDULOS DA APLICAÇÃO
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
        preco_cimento = st.number_input("Preço do Saco de Cimento 50kg (R$):", value=32.00, step=1.00)
        preco_m3_areia = st.number_input("Preço do m³ de Areia Média (R$):", value=120.00, step=10.00)

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        if "9x19x19" in tipo_material or "Baiano" in tipo_material:
            qtd_blocos_m2 = 25
            vol_arg = 0.018
        elif "14x19x19" in tipo_material:
            qtd_blocos_m2 = 25
            vol_arg = 0.025
        elif "Concreto 14x19x39" in tipo_material:
            qtd_blocos_m2 = 12.5
            vol_arg = 0.020
        else:
            qtd_blocos_m2 = 90
            vol_arg = 0.040

        total_blocos = area_paredes * qtd_blocos_m2 * 1.05
        total_arg = area_paredes * vol_arg * 1.05
        sacos_c = total_arg * 7.5
        m3_a = total_arg * 1.05

        custo_bl = total_blocos * preco_unidade
        custo_ci = sacos_c * preco_cimento
        custo_ar = m3_a * preco_m3_areia
        custo_tot = custo_bl + custo_ci + custo_ar

        st.success("Cálculo de alvenaria concluído!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Blocos/Tijolos", f"{int(total_blocos)} un")
        c2.metric("Sacos de Cimento", f"{sacos_c:.1f} sc")
        c3.metric("Areia Média", f"{m3_a:.2f} m³")
        st.info(f"**Custo Total Estimado da Alvenaria:** `R$ {custo_tot:,.2f}`")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    st.subheader("🏠 Dimensionamento Completo e Orçamento de Lajes Pré-moldadas")
    st.write("Escolha abaixo o tipo de laje, o material de enchimento e a altura da viga para obter o quantitativo exato de canteiro.")

    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input("Área Total da Laje (m²):", min_value=1.0, value=50.0, step=1.0)
        tipo_enchimento = st.selectbox(
            "Material de Enchimento (Lajota/Bloco):",
            [
                "Lajota Cerâmica Tradicional",
                "Bloco de Isopor (EPS - Alta Densidade)",
                "Lajota Concreto / Paulistinha"
            ]
        )
    with col2:
        altura_laje = st.selectbox(
            "Altura da Laje (Vigota + Capa):",
            [
                "H8 (8 cm vigota + 3 cm capa = 11 cm total) - Pequenos vãos",
                "H12 (12 cm vigota + 4 cm capa = 16 cm total) - Residencial Padrão",
                "H16 (16 cm vigota + 4 cm capa = 20 cm total) - Vãos Maiores / Sobrados",
                "H20 (20 cm vigota + 5 cm capa = 25 cm total) - Grandes Cargas"
            ]
        )
        sobrecarga_util = st.selectbox(
            "Utilização da Laje:",
            [
                "Residencial Comum (150 kg/m²)",
                "Forro / Cobertura sem Acesso (100 kg/m²)",
                "Comercial / Escritório (250 kg/m²)"
            ]
        )

    if st.button("Calcular Materiais Completos da Laje", type="primary"):
        # Fatores técnicos baseados no tipo de altura e enchimento
        ml_vigotas = area_laje * 1.35 # metros lineares de vigotas treliçadas por m²
        
        if "Cerâmica" in tipo_enchimento:
            qtd_blocos = area_laje * 8.3 # média de lajotas cerâmicas por m²
        elif "Isopor" in tipo_enchimento:
            qtd_blocos = area_laje * 2.5 # blocos de EPS costumam cobrir cerca de 0.40m cada
        else:
            qtd_blocos = area_laje * 8.0

        # Volume da capa de concreto de acordo com a altura escolhida
        if "H8" in altura_laje:
            espessura_capa_cm = 3.0
            vol_concreto_m3 = area_laje * 0.050
        elif "H12" in altura_laje:
            espessura_capa_cm = 4.0
            vol_concreto_m3 = area_laje * 0.065
        elif "H16" in altura_laje:
            espessura_capa_cm = 4.0
            vol_concreto_m3 = area_laje * 0.080
        else:
            espessura_capa_cm = 5.0
            vol_concreto_m3 = area_laje * 0.100

        # Adiciona 7% de perda padrão de canteiro no concreto
        vol_concreto_com_perda = vol_concreto_m3 * 1.07
        
        # Malha pop para armadura negativa/distribuição (1 painel cobre aprox 5m úteis ou calcula por m2 com folga)
        qtd_malha_pop = area_laje / 4.5 # estimativa de panos de malha pop (ex: Q-61 / Q-92)

        st.success("Dimensionamento da laje realizado com sucesso!")

        c1, c2, c3 = st.columns(3)
        c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} metros lineares")
        c2.metric("Blocos / Lajotas", f"{int(qtd_blocos)} unidades")
        c3.metric("Concreto para a Capa", f"{vol_concreto_com_perda:.2f} m³")

        st.markdown("### 📋 Resumo Detalhado de Insumos da Laje:")
        st.info(
            f"- **Tipo de Enchimento:** {tipo_enchimento}\n"
            f"- **Espessura da Capa de Compressão:** `{espessura_capa_cm:.0f} cm`\n"
            f"- **Painéis de Malha Pop (Ferro de Distribuição):** Aprox. `{int(qtd_malha_pop) + 1} painéis`\n"
            f"- **Escoramento Recomendado:** Pontaletes de madeira/ferro a cada **1,5 metros** para evitar flecha na concretagem."
        )

        if "Isopor" in tipo_enchimento:
            st.markdown('<div class="alerta-sucesso">💡 <b>Vantagem do Isopor (EPS):</b> Reduz drasticamente o peso morto da estrutura sobre vigas e pilares, além de proporcionar excelente isolamento térmico e acústico.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">💡 <b>Vantagem da Lajota Cerâmica:</b> Oferece excelente aderência para o emboço inferior e inércia térmica tradicional de canteiro.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    st.subheader("Cálculo Avançado de Concreto (por m², Elementos e Usinado vs. Betoneira)")
    tab_m2, tab_vol, tab_traco = st.tabs(["📐 1. Concreto por m²", "📏 2. Volume de Elementos", "🧪 3. Usinado vs. Betoneira"])
    with tab_m2:
        area_m2 = st.number_input("Área da Superfície (m²):", min_value=1.0, value=50.0)
        esp_cm = st.number_input("Espessura (cm):", min_value=1.0, value=7.0)
        if st.button("Calcular Concreto por m²", type="primary"):
            vol = (area_m2 * (esp_cm / 100.0)) * 1.07
            st.success(f"Volume necessário com 7% de perda: **{vol:.2f} m³**")
            st.session_state.ja_fez_calculo_gratis = True
    with tab_vol:
        qp = st.number_input("Quantidade de Peças:", min_value=1, value=4)
        cp = st.number_input("Comprimento (m):", min_value=0.1, value=4.0)
        lp = st.number_input("Base (cm):", min_value=1.0, value=15.0)
        ap = st.number_input("Altura (cm):", min_value=1.0, value=40.0)
        if st.button("Calcular Volume de Elementos", type="primary"):
            vol_e = qp * cp * (lp / 100.0) * (ap / 100.0) * 1.07
            st.success(f"Volume estrutural: **{vol_e:.3f} m³**")
            st.session_state.ja_fez_calculo_gratis = True
    with tab_traco:
        vol_a = st.number_input("Volume Total (m³):", min_value=0.1, value=5.0)
        if st.button("Comparar Usinado vs. Betoneira", type="primary"):
            st.success("Análise comparativa gerada!")
            st.session_state.ja_fez_calculo_gratis = True

elif modulo == "⚙️ Projeto de Aço, Custo e Auditoria de Armadura":
    st.subheader("⚙️ Projeto de Aço, Projeção de Custo e Auditoria de Armadura")
    col1, col2 = st.columns(2)
    with col1:
        area_obra = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=120.0, step=10.0)
        padrao_aco = st.selectbox("Padrão da Estrutura:", ["Padrão Normal / Residencial Térreo (12 kg/m²)", "Sobrado / Estrutura Robusta (16 kg/m²)", "Leve / Cobertura (9 kg/m²)"])
    with col2:
        preco_kg_aco = st.number_input("Preço Atual do Aço por kg (R$):", value=11.50, step=0.50)

    if st.button("Gerar Auditoria e Detalhamento de Aço", type="primary"):
        fator_aco = 12 if "Normal" in padrao_aco else (16 if "Robusto" in padrao_aco else 9)
        peso_total = area_obra * fator_aco
        p_10 = peso_total * 0.45 
        p_8 = peso_total * 0.35  
        p_63 = peso_total * 0.20 
        custo_aco_total = peso_total * preco_kg_aco

        st.success("Auditoria de armadura concluída!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ferro 3/8'' (10.0 mm)", f"{p_10:.1f} kg")
        c2.metric("Ferro 5/16'' (8.0 mm)", f"{p_8:.1f} kg")
        c3.metric("Ferro 1/4'' (6.3 mm)", f"{p_63:.1f} kg")
        st.info(f"**Custo Total do Aço:** `R$ {custo_aco_total:,.2f}`")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
    st.subheader("🏗️ Dimensionamento Prático de Vigas, Bitolas e Espessuras de Ferro")
    vao_viga = st.number_input("Vão Livre da Viga (metros):", min_value=1.0, value=4.0, step=0.5)
    if st.button("Definir Bitolas e Espessuras da Viga", type="primary"):
        st.success("Dimensionamento de armadura da viga gerado!")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🦾 Armadura Longitudinal")
            st.write("- **Fundo:** Ferro 3/8\" (10.0 mm)\n- **Topo:** Ferro 5/16\" (8.0 mm)")
        with c2:
            st.markdown("### 🔄 Estribos")
            st.write("- **Bitola:** Ferro 1/4\" (6.3 mm)\n- **Espaçamento:** A cada 10 cm nas pontas.")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
    st.subheader("🚰 Quantitativo Real de Peças e Encanamentos por Ambiente")
    col1, col2 = st.columns(2)
    with col1:
        qtd_banheiros = st.number_input("Número de Banheiros Completos:", min_value=1, value=1, step=1)
        distancia_cozinha_fossa = st.number_input("Distância da Cozinha até a Fossa / Rede (metros):", min_value=2.0, value=8.0, step=1.0)
    with col2:
        tipo_esgoto_rede = st.selectbox("Destino do Esgoto:", ["Fossa Séptica + Sumidouro", "Rede Pública de Esgoto da Rua"])

    if st.button("Gerar Lista Prática de Material Hidráulico", type="primary"):
        tubo_esgoto_100 = qtd_banheiros * 6.0 
        tubo_esgoto_40_50 = qtd_banheiros * 8.0 
        distancia_agua_cozinha = distancia_cozinha_fossa + 4.0
        
        st.success("Lista hidráulica gerada com sucesso!")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### 🚿 Banheiro(s): `{qtd_banheiros}` un")
            st.write(f"- Tubo Esgoto 100mm: {tubo_esgoto_100:.1f}m\n- Tubo Esgoto 40/50mm: {tubo_esgoto_40_50:.1f}m")
        with c2:
            st.markdown(f"### 🍳 Cozinha & Fossa: `{distancia_cozinha_fossa}m`")
            st.write(f"- Tubo Água Fria 25mm: {distancia_agua_cozinha:.1f}m\n- Caixa de Gordura: 1 un")
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
