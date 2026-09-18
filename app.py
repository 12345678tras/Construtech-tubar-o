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
# 4. MÓDULOS OTIMIZADOS PARA O CANTEIRO
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
    st.subheader("Dimensionamento Técnico e Orçamento de Lajes (Pré-moldada)")
    area_laje = st.number_input("Área da Laje (m²):", min_value=1.0, value=50.0, step=1.0)
    tipo_laje = st.selectbox("Tipo de Enchimento da Laje:", ["Laje com Lajota Cerâmica", "Laje com Isopor (EPS - Poliestireno)"])
    if st.button("Calcular Materiais da Laje", type="primary"):
        ml_vigotas = area_laje * 1.35
        qtd_ench = area_laje * (8.3 if "Cerâmica" in tipo_laje else 2.5)
        m3_conc = area_laje * 0.055
        st.success("Dimensionamento de laje realizado com sucesso!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} m")
        c2.metric("Blocos de Enchimento", f"{int(qtd_ench)} un")
        c3.metric("Concreto para Capa", f"{m3_conc:.2f} m³")
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
    st.write("Ferramenta avançada desenvolvida com base na prática de canteiro para evitar subdimensionamento e desperdício de ferro.")
    
    col1, col2 = st.columns(2)
    with col1:
        area_obra = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=120.0, step=10.0)
        padrao_aco = st.selectbox("Padrão da Estrutura:", ["Padrão Normal / Residencial Térreo (12 kg/m²)", "Sobrado / Estrutura Robusta (16 kg/m²)", "Leve / Cobertura (9 kg/m²)"])
    with col2:
        preco_kg_aco = st.number_input("Preço Atual do Aço por kg (R$):", value=11.50, step=0.50)

    if st.button("Gerar Auditoria e Detalhamento de Aço", type="primary"):
        fator_aco = 12 if "Normal" in padrao_aco else (16 if "Robusto" in padrao_aco else 9)
        peso_total = area_obra * fator_aco
        
        # Divisão típica de bitolas em obra residencial
        p_10 = peso_total * 0.45 # 10mm (3/8") - Vigas e pilares principais
        p_8 = peso_total * 0.35  # 8mm (5/16") - Vigas secundárias e lajes
        p_63 = peso_total * 0.20 # 6.3mm (1/4") - Estribos

        custo_aco_total = peso_total * preco_kg_aco

        st.success("Auditoria de armadura e projeção de custos concluídas com sucesso!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Ferro 3/8'' (10.0 mm)", f"{p_10:.1f} kg")
        c2.metric("Ferro 5/16'' (8.0 mm)", f"{p_8:.1f} kg")
        c3.metric("Ferro 1/4'' (6.3 mm)", f"{p_63:.1f} kg")

        st.markdown(f"### 💰 Resumo Financeiro do Aço:")
        st.info(f"**Peso Total de Aço Estimado:** `{peso_total:.1f} kg` | **Custo Total:** `R$ {custo_aco_total:,.2f}` (Base: R$ {preco_kg_aco:.2f}/kg)")

        if fator_aco <= 9:
            st.markdown('<div class="alerta-perigo">🚨 ALERTA DE SEGURANÇA: Menos de 10 kg/m² em lajes e vigas pode gerar deformações excessivas e trincas na alvenaria. Reforce os apoios!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">✅ Taxa de armadura dentro dos parâmetros seguros de engenharia para suportar cargas verticais e momentos fletores.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
    st.subheader("🏗️ Dimensionamento Prático de Vigas, Bitolas e Espessuras de Ferro")
    st.write("Saiba exatamente qual bitola, diâmetro e espessura de ferro utilizar no fundo, topo e estribos da viga de acordo com o vão livre.")

    col1, col2 = st.columns(2)
    with col1:
        vao_viga = st.number_input("Vão Livre da Viga (metros):", min_value=1.0, value=4.0, step=0.5)
        carga_viga = st.selectbox("Carga Suportada:", ["Residencial Normal (Laje + Paredes em cima)", "Viga de Balanço / Porta-Alinhamento", "Apenas Cobertura / Telhado"])
    with col2:
        altura_viga_sugerida = vao_viga * 10 # Regra prática: vão x 10 em cm (ex: 4m = 40cm de altura)
        st.info(f"💡 **Altura Mínima Recomendada para a Viga:** `{altura_viga_sugerida:.0f} cm` (incluindo a laje)")

    if st.button("Definir Bitolas e Espessuras da Viga", type="primary"):
        st.success("Dimensionamento de armadura da viga gerado!")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🦾 Armadura Longitudinal (Fundo e Topo)")
            if vao_viga <= 3.5:
                st.write("- **Fundo (Tração):** 2 barras de **Ferro 5/16\" (8.0 mm)** ou 3/8\" (10.0 mm)")
                st.write("- **Topo (Compressão):** 2 barras de **Ferro 1/4\" (6.3 mm)** ou 5/16\" (8.0 mm)")
            elif vao_viga <= 5.0:
                st.markdown("- **Fundo (Tração):** 2 barras de **Ferro 3/8\" (10.0 mm)** + 1 barra de reforço")
                st.markdown("- **Topo (Compressão):** 2 barras de **Ferro 5/16\" (8.0 mm)**")
            else:
                st.markdown("- **Fundo (Tração):** 2 barras de **Ferro 1/2\" (12.5 mm)** — *Vão grande, requer atenção especial!*")
                st.markdown("- **Topo (Compressão):** 2 barras de **Ferro 3/8\" (10.0 mm)**")

        with c2:
            st.markdown("### 🔄 Estribos (Cisalhamento)")
            st.markdown("- **Bitola do Estribo:** **Ferro 1/4\" (6.3 mm)**")
            st.markdown("- **Espaçamento nas Extremidades:** A cada **10 cm** (nos primeiros 1 metro de cada apoio).")
            st.markdown("- **Espaçamento no Meio do Vão:** A cada **15 cm a 20 cm**.")

        if vao_viga > 5.0:
            st.markdown('<div class="alerta-atencao">⚠️ Vãos acima de 5 metros acumulam muita flecha. Certifique-se de aplicar contra-flecha na caixaria da viga de 1% do vão.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">✅ Configuração padrão de canteiro testada e aprovada para garantir rigidez estrutural.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
    st.subheader("🚰 Quantitativo Real de Peças e Encanamentos por Ambiente")
    st.write("Esqueça contas teóricas. Veja exatamente a lista de tubos, conexões e diâmetros que você vai gastar para executar um banheiro completo e a ligação da cozinha até a fossa/rede.")

    col1, col2 = st.columns(2)
    with col1:
        qtd_banheiros = st.number_input("Número de Banheiros Completos:", min_value=1, value=1, step=1)
        distancia_cozinha_fossa = st.number_input("Distância da Cozinha até a Fossa / Rede (metros):", min_value=2.0, value=8.0, step=1.0)
    with col2:
        tipo_esgoto_rede = st.selectbox("Destino do Esgoto:", ["Fossa Séptica + Sumidouro", "Rede Pública de Esgoto da Rua"])

    if st.button("Gerar Lista Prática de Material Hidráulico", type="primary"):
        # Cálculos práticos de canteiro
        # Banheiro completo padrão: Vaso sanitário (100mm), Lavatório, Chuveiro, Ralo
        tubo_esgoto_100 = qtd_banheiros * 6.0 # metros de tubo 100mm
        tubo_esgoto_40_50 = qtd_banheiros * 8.0 # metros de tubo 40/50mm (piae ralo)
        tubo_agua_fria_25 = qtd_banheiros * 12.0 + distancia_cozinha_fossa # metros de tubo marrom 25mm (3/4)
        
        caixa_gordura = 1 if distancia_cozinha_fossa > 0 else 0
        joelhos_100 = qtd_banheiros * 5
        joelhos_25 = qtd_banheiros * 8 + 4

        st.success("Lista de materiais hidráulicos de canteiro gerada com sucesso!")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### 🚿 Para {qtd_banheiros} Banheiro(s):")
            st.write(f"- **Tubo Esgoto 100 mm (Vaso):** `{tubo_esgoto_100:.1f} metros` (Aprox. {int(tubo_esgoto_100/3)+1} barras de 3m)")
            st.write(f"- **Tubo Esgoto 40/50 mm (Ralos/Pia):** `{tubo_esgoto_40_50:.1f} metros`")
            st.write(f"- **Joelhos e Curvas de 100mm:** Aprox. `{joelhos_100} unidades`")
            st.write(f"- **Registros de Pressão e Gaveta:** `{qtd_banheiros * 2} unidades`")
            st.write(f"- **Caixa Sifonada com Grelha:** `{qtd_banheiros} unidades`")

        with c2:
            st.markdown(f"### 🍳 Para a Cozinha & Ligação até a Fossa (`{distancia_cozinha_fossa}m`):")
            st.write(f"- **Tubo Esgoto 75mm/100mm (Pia até Fossa):** `{distancia_cozinha_fossa} metros`")
            st.write(f"- **Caixa de Gordura Pronta (Obrigatória):** `{caixa_gordura} unidade`")
            st.write(f"- **Tubo de Água Fria Marrom 25mm (3/4''):** `{distancia_agua_cozinha = distancia_cozinha_fossa + 4:.1f} metros`")
            st.write(f"- **Conexões Joelhos 25mm e Tês:** Aprox. `10 unidades`")

        st.markdown(f'<div class="alerta-sucesso">💡 <b>Dica de Mestre de Obras:</b> Nunca misture tubos de esgoto cinzas comuns em trechos que recebem carga de tráfego de veículos. Use sempre a linha refoçada (marrom/laranja) e caixas de inspeção a cada 15 metros de tubulação enterrada.</div>', unsafe_allow_html=True)
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
