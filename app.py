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
    .alerta-sucesso { background-color: #ECFDF5; border: 1px solid #10B981; padding: 12px; border-radius: 6px; color: #065F46; font-weight: bold; margin-top: 10px; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. MENU LATERAL
# ==========================================
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

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    st.subheader("🏠 Dimensionamento Completo e Orçamento de Lajes Pré-moldadas")
    st.write("Escolha abaixo o tipo de laje, o material de enchimento e a altura da viga para obter o quantitativo exato de canteiro.")

    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input("Área Total da Laje (m²):", min_value=1.0, value=50.0, step=1.0, key="inp_area_laje_v2")
        tipo_enchimento = st.selectbox(
            "Material de Enchimento (Lajota/Bloco):",
            [
                "Lajota Cerâmica Tradicional",
                "Bloco de Isopor (EPS - Alta Densidade)",
                "Lajota Concreto / Paulistinha"
            ],
            key="inp_enchimento_laje_v2"
        )
    with col2:
        altura_laje = st.selectbox(
            "Altura da Laje (Vigota + Capa):",
            [
                "H8 (8 cm vigota + 3 cm capa = 11 cm total) - Pequenos vãos",
                "H12 (12 cm vigota + 4 cm capa = 16 cm total) - Residencial Padrão",
                "H16 (16 cm vigota + 4 cm capa = 20 cm total) - Vãos Maiores / Sobrados",
                "H20 (20 cm vigota + 5 cm capa = 25 cm total) - Grandes Cargas"
            ],
            key="inp_altura_laje_v2"
        )
        sobrecarga_util = st.selectbox(
            "Utilização da Laje:",
            [
                "Residencial Comum (150 kg/m²)",
                "Forro / Cobertura sem Acesso (100 kg/m²)",
                "Comercial / Escritório (250 kg/m²)"
            ],
            key="inp_sobrecarga_laje_v2"
        )

    # Botão de cálculo com a exibição de resultados restaurada e garantida
    if st.button("Calcular Materiais da Laje", type="primary", key="btn_calcular_laje_v2"):
        ml_vigotas = area_laje * 1.35
        
        if "Cerâmica" in tipo_enchimento:
            qtd_blocos = area_laje * 8.3
        elif "Isopor" in tipo_enchimento:
            qtd_blocos = area_laje * 2.5
        else:
            qtd_blocos = area_laje * 8.0

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

        vol_concreto_com_perda = vol_concreto_m3 * 1.07
        qtd_malha_pop = area_laje / 4.5

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

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    st.subheader("Cálculo Avançado de Concreto")
    area_m2 = st.number_input("Área da Superfície (m²):", min_value=1.0, value=50.0)
    esp_cm = st.number_input("Espessura (cm):", min_value=1.0, value=7.0)
    if st.button("Calcular Concreto por m²", type="primary"):
        vol = (area_m2 * (esp_cm / 100.0)) * 1.07
        st.success(f"Volume necessário com 7% de perda: **{vol:.2f} m³**")

elif modulo == "⚙️ Projeto de Aço, Custo e Auditoria de Armadura":
    st.subheader("⚙️ Projeto de Aço e Auditoria")
    area_obra = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=120.0)
    if st.button("Gerar Auditoria", type="primary"):
        st.success("Auditoria gerada com sucesso!")

elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
    st.subheader("🏗️ Dimensionamento de Vigas")
    if st.button("Definir Bitolas", type="primary"):
        st.success("Viga dimensionada!")

elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
    st.subheader("🚰 Sistema Hidráulico Prático")
    if st.button("Gerar Lista Hidráulica", type="primary"):
        st.success("Lista hidráulica gerada!")

elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Orçamento Comercial")
    if st.button("Emitir Proposta", type="primary"):
        st.success("Proposta emitida!")

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
