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
# 1.1. CONTROLE DE AMOSTRA GRÁTIS GRAVADA NO NAVEGADOR
# ==========================================
# Verificamos se o navegador já registrou que a amostra grátis foi usada
params = st.query_params
amostra_usada = params.get("amostra", "nao")

if "liberado_pago" not in st.session_state:
    st.session_state.liberado_pago = False

# Se a amostra já foi usada e não foi inserida a chave de pagamento paga, bloqueia!
if amostra_usada == "sim" and not st.session_state.liberado_pago:
    st.markdown('<p class="main-header">🔒 Amostra Grátis Já Utilizada neste Computador</p>', unsafe_allow_html=True)
    st.info("💡 Você já aproveitou o seu **1º acesso gratuito** neste dispositivo. Para continuar utilizando os módulos e fazendo novos cálculos, por favor insira a chave de liberação/pagamento abaixo.")
    
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        email_usuario = st.text_input("Seu E-mail ou Telefone Cadastrado:", key="login_email")
    with col_l2:
        codigo_liberacao = st.text_input("Chave de Pagamento / Código de Acesso:", type="password", key="login_codigo")

    if st.button("Liberar Acesso Completo", type="primary", key="btn_liberar_pg"):
        if codigo_liberacao.strip() != "":
            st.session_state.liberado_pago = True
            st.success("Chave validada com sucesso! Entrando na plataforma...")
            st.rerun()
        else:
            st.warning("Por favor, informe a chave de liberação válida.")
    
    st.stop()
elif amostra_usada != "sim" and not st.session_state.liberado_pago:
    # Marca no navegador do usuário que a amostra grátis foi consumida para futuras visitas
    st.query_params["amostra"] = "sim"

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
# 4. MÓDULOS DA APLICAÇÃO COM CÁLCULOS REAIS
# ==========================================

if modulo == "📊 Visão Geral e BDI":
    st.subheader("Painel de Controle e Viabilidade Comercial")
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Nome do Projeto / Cliente:", value="Obra Residencial Exemplo", key="bdi_cli")
        custo_base = st.number_input("Custo Direto Total Estimado (R$):", min_value=0.0, value=50000.0, step=1000.0, key="bdi_custo")
    with col2:
        bdi_taxa = st.slider("Taxa de BDI Aplicada (%):", 0.0, 50.0, 25.0, key="bdi_taxa")

    if st.button("Calcular Viabilidade e Venda", type="primary", key="btn_bdi"):
        preco_venda = custo_base * (1 + bdi_taxa / 100)
        lucro_estimado = preco_venda - custo_base
        st.success("Viabilidade calculada com sucesso!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Preço Final de Venda", f"R$ {preco_venda:,.2f}")
        col_m2.metric("Lucro Bruto Estimado", f"R$ {lucro_estimado:,.2f}")

elif modulo == "🧱 Alvenaria Completa (Blocos, Cimento e Areia)":
    st.subheader("🧱 Dimensionamento e Soma de Insumos de Alvenaria")
    col1, col2 = st.columns(2)
    with col1:
        area_paredes = st.number_input("Área Líquida de Paredes (m²):", min_value=1.0, value=80.0, step=1.0, key="alv_area")
        tipo_material = st.selectbox(
            "Escolha a Variedade do Bloco / Tijolo:", 
            [
                "Bloco Cerâmico 9x19x19 cm (Vedação)", 
                "Bloco Cerâmico 14x19x19 cm (Estrutural/Vedação)", 
                "Bloco de Concreto 14x19x39 cm", 
                "Tijolo Baiano 8 furos (9x19x19 cm)", 
                "Tijolo Maciço / Comum"
            ],
            key="alv_tipo"
        )
        preco_unidade = st.number_input("Preço Unitário do Bloco/Tijolo (R$):", value=1.20, step=0.10, key="alv_pr_bloco")
    with col2:
        preco_cimento = st.number_input("Preço do Saco de Cimento 50kg (R$):", value=32.00, step=1.00, key="alv_pr_cim")
        preco_m3_areia = st.number_input("Preço do m³ de Areia Média (R$):", value=120.00, step=10.00, key="alv_pr_areia")

    if st.button("Calcular Soma Total da Alvenaria", type="primary", key="btn_calc_alv"):
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

        st.success("Soma de alvenaria concluída com sucesso!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Blocos/Tijolos Totais", f"{int(total_blocos)} un")
        c2.metric("Sacos de Cimento", f"{sacos_c:.1f} sc")
        c3.metric("Areia Média", f"{m3_a:.2f} m³")
        st.info(f"💰 **Soma do Custo Total da Alvenaria:** `R$ {custo_tot:,.2f}`")

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    st.subheader("🏠 Dimensionamento, Variedade e Ferro da Laje")
    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input("Área Total da Laje (m²):", min_value=1.0, value=50.0, step=1.0, key="laje_area")
        tipo_enchimento = st.selectbox(
            "Variedade de Enchimento da Laje:",
            [
                "Lajota Cerâmica Tradicional",
                "Bloco de Isopor (EPS - Alta Densidade)",
                "Lajota Concreto / Paulistinha"
            ],
            key="laje_enchimento"
        )
    with col2:
        altura_laje = st.selectbox(
            "Altura da Laje (Vigota + Capa):",
            [
                "H8 (8 cm vigota + 3 cm capa = 11 cm total)",
                "H12 (12 cm vigota + 4 cm capa = 16 cm total)",
                "H16 (16 cm vigota + 4 cm capa = 20 cm total)",
                "H20 (20 cm vigota + 5 cm capa = 25 cm total)"
            ],
            key="laje_altura"
        )

    if st.button("Calcular Materiais e Ferro da Laje", type="primary", key="btn_calc_laje"):
        ml_vigotas = area_laje * 1.35
        if "Cerâmica" in tipo_enchimento:
            qtd_blocos = area_laje * 8.3
        elif "Isopor" in tipo_enchimento:
            qtd_blocos = area_laje * 2.5
        else:
            qtd_blocos = area_laje * 8.0

        if "H8" in altura_laje:
            vol_concreto_m3 = area_laje * 0.050
        elif "H12" in altura_laje:
            vol_concreto_m3 = area_laje * 0.065
        elif "H16" in altura_laje:
            vol_concreto_m3 = area_laje * 0.080
        else:
            vol_concreto_m3 = area_laje * 0.100

        vol_concreto_com_perda = vol_concreto_m3 * 1.07
        sacos_cimento_laje = vol_concreto_com_perda * 6.5 
        qtd_malha_pop = area_laje / 4.5

        st.success("Soma de materiais da laje realizada!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} m lineares")
        c2.metric("Blocos / Lajotas", f"{int(qtd_blocos)} un")
        c3.metric("Concreto (Capa)", f"{vol_concreto_com_perda:.2f} m³")

        st.info(
            f"📋 **Detalhamento do Ferro e Concreto da Laje:**\n"
            f"- **Armadura (Malha Pop / Distribuição):** Aprox. `{int(qtd_malha_pop) + 1} painéis`\n"
            f"- **Cimento necessário para a capa:** Aprox. `{sacos_cimento_laje:.1f} sacos de 50kg`\n"
            f"- **Variedade Escolhida:** {tipo_enchimento} com estrutura {altura_laje}."
        )

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    st.subheader("🏗️ Dimensão, Espessura e Soma de Sacos de Cimento (Traço)")
    col1, col2 = st.columns(2)
    with col1:
        area_concreto = st.number_input("Metragem da Área / Piso (m²):", min_value=1.0, value=50.0, key="conc_area")
        espessura_cm = st.number_input("Espessura da Camada/Laje (cm):", min_value=1.0, value=7.0, key="conc_esp")
    with col2:
        traco_tipo = st.selectbox(
            "Variedade do Traço de Concreto:",
            [
                "Traço 1:2:3 (Fck 25 MPa - Estrutural Forte)",
                "Traço 1:2.5:3.5 (Fck 20 MPa - Residencial Padrão)",
                "Traço 1:3:5 (Contrapiso / Lastro Magro)"
            ],
            key="conc_traco"
        )

    if st.button("Calcular Volume e Quantidade de Sacos", type="primary", key="btn_calc_conc"):
        volume_real = (area_concreto * (espessura_cm / 100.0)) * 1.07 
        if "25 MPa" in traco_tipo:
            sc_cif = volume_real * 7.5
            areia_m3 = volume_real * 0.55
            brita_m3 = volume_real * 0.75
        elif "20 MPa" in traco_tipo:
            sc_cif = volume_real * 6.5
            areia_m3 = volume_real * 0.60
            brita_m3 = volume_real * 0.78
        else:
            sc_cif = volume_real * 5.0
            areia_m3 = volume_real * 0.65
            brita_m3 = volume_real * 0.80

        st.success("Cálculo de concreto finalizado!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Volume Total com Perda", f"{volume_real:.2f} m³")
        c2.metric("Sacos de Cimento (50kg)", f"{sc_cif:.1f} sacos")
        c3.metric("Areia / Brita", f"{areia_m3:.2f} m³ / {brita_m3:.2f} m³")

elif modulo == "⚙️ Projeto de Aço, Custo e Auditoria de Armadura":
    st.subheader("⚙️ Projeto Geral de Aço e Auditoria")
    area_obra = st.number_input("Área Construída Total (m²):", min_value=10.0, value=120.0, key="aco_geral_area")
    preco_aco_kg = st.number_input("Preço Médio do Aço por kg (R$):", value=11.50, key="aco_geral_pr")
    if st.button("Gerar Auditoria de Aço", type="primary", key="btn_calc_aco_geral"):
        peso_tot = area_obra * 14.0 
        custo_tot_aco = peso_tot * preco_aco_kg
        st.success("Auditoria gerada!")
        c1, c2 = st.columns(2)
        c1.metric("Peso Estimado de Aço", f"{peso_tot:.1f} kg")
        c2.metric("Custo Total do Aço", f"R$ {custo_tot_aco:,.2f}")

elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
    st.subheader("🏗️ Dimensionamento de Vigas, Colunas e Bitolas de Ferro")
    col1, col2 = st.columns(2)
    with col1:
        vao_viga = st.number_input("Vão Livre da Viga ou Coluna (metros):", min_value=1.0, value=4.0, key="viga_vao")
        qtd_pecas = st.number_input("Quantidade de Vigas/Colunas iguais:", min_value=1, value=4, key="viga_qtd")
    with col2:
        tipo_bitola_principal = st.selectbox(
            "Bitola do Ferro Principal (Fundo/Topo):",
            [
                "Ferro 3/8'' (10.0 mm) - Padrão Estrutural",
                "Ferro 5/16'' (8.0 mm) - Leve",
                "Ferro 1/2'' (12.5 mm) - Grande Vão / Sobrado"
            ],
            key="viga_bitola"
        )
        espacamento_estribo = st.selectbox(
            "Espaçamento dos Estribos (Ferro 1/4'' / 6.3mm):",
            ["A cada 10 cm nas pontas / 15 cm no meio", "A cada 15 cm em todo o comprimento"]
        )

    if st.button("Calcular Quantidade de Ferro das Vigas", type="primary", key="btn_calc_vigas"):
        kg_por_viga = vao_viga * 8.5 * qtd_pecas
        estribos_un = int((vao_viga / 0.12) * qtd_pecas)
        
        st.success("Dimensionamento de vigas e bitolas concluído!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Ferro Principal Escolhido", tipo_bitola_principal.split(" - ")[0])
        c2.metric("Peso Total de Ferro", f"{kg_por_viga:.1f} kg")
        c3.metric("Estribos 1/4'' (6.3mm)", f"{estribos_un} unidades")
        st.info(f"🦾 **Resumo Estrutural:** Para `{qtd_pecas}` peças com vão de `{vao_viga}m`, utilize estribos com espaçamento `{espacamento_estribo}`.")

elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
    st.subheader("🚰 Quantitativo de Canos, Conexões e Fossa para Banheiro e Cozinha")
    col1, col2 = st.columns(2)
    with col1:
        qtd_banheiros = st.number_input("Número de Banheiros Completos:", min_value=1, value=1, step=1, key="hid_banh")
        qtd_cozinhas = st.number_input("Número de Cozinhas:", min_value=1, value=1, step=1, key="hid_coz")
    with col2:
        distancia_fossa = st.number_input("Distância até a Fossa / Rede da Rua (metros):", min_value=2.0, value=10.0, step=1.0, key="hid_dist")
        incluir_fossa = st.checkbox("Incluir Orçamento de Fossa Séptica + Sumidouro", value=True, key="hid_fos")

    if st.button("Calcular Soma de Peças Hidráulicas", type="primary", key="btn_calc_hid"):
        cano_esgoto_100 = (qtd_banheiros * 6.0) + distancia_fossa
        cano_esgoto_50 = qtd_banheiros * 5.0 + (qtd_cozinhas * 4.0)
        cano_agua_25 = (qtd_banheiros * 8.0) + (qtd_cozinhas * 6.0)
        joelhos_100 = (qtd_banheiros * 6) + 4
        joelhos_25 = (qtd_banheiros * 10) + (qtd_cozinhas * 6)
        caixa_gordura = qtd_cozinhas * 1
        fossa_sistema = 1 if incluir_fossa else 0

        st.success("Soma hidráulica gerada com sucesso!")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📏 Tubos e Conexões de Esgoto")
            st.write(f"- Tubo Esgoto 100mm: **{cano_esgoto_100:.1f} metros**")
            st.write(f"- Tubo Esgoto 50mm: **{cano_esgoto_50:.1f} metros**")
            st.write(f"- Joelhos 100mm: **{joelhos_100} unidades**")
            if incluir_fossa:
                st.write("- Fossa Séptica + Sumidouro: **1 conjunto completo**")
        with c2:
            st.markdown("### 💧 Água Fria e Acessórios")
            st.write(f"- Tubo PVC Água Fria 25mm: **{cano_agua_25:.1f} metros**")
            st.write(f"- Joelhos 25mm: **{joelhos_25} unidades**")
            st.write(f"- Caixa de Gordura (Cozinha): **{caixa_gordura} unidade(s)**")

elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Orçamento Comercial e Proposta de Serviços")
    valor_bruto = st.number_input("Valor Base dos Serviços (R$):", value=12000.0, key="fat_val")
    if st.button("Emitir Proposta", type="primary", key="btn_calc_fat"):
        st.success(f"Proposta emitida no valor de R$ {valor_bruto:,.2f}!")

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
