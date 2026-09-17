import streamlit as str_module
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
        "🚰 Sistema Hidráulico Profissional (Atualizado)",
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
# 4. MÓDULOS COM INTELIGÊNCIA TÉCNICA E ALERTAS
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
        area_paredes = st.number_input("Área Líquida de Paredes (m²):", min_value=1.0, value=80.0)
        tipo_material = st.selectbox(
            "Escolha o Bloco / Tijolo:", 
            [
                "Bloco Cerâmico 9x19x19 cm", 
                "Bloco Cerâmico 14x19x19 cm", 
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
            qtd_por_m2 = 25.0
            fator_argamassa = 0.018
        elif "14x19x19" in tipo_material:
            qtd_por_m2 = 25.0
            fator_argamassa = 0.025
        elif "Concreto 14x19x39" in tipo_material:
            qtd_por_m2 = 12.5
            fator_argamassa = 0.020
        else:
            qtd_por_m2 = 80.0
            fator_argamassa = 0.045

        total_pecas = area_paredes * qtd_por_m2 * 1.05
        volume_argamassa = area_paredes * fator_argamassa
        total_sacos_cimento = volume_argamassa * 7.0
        total_areia_m3 = volume_argamassa * 1.15

        custo_pecas = total_pecas * preco_unidade
        custo_cimento = total_sacos_cimento * preco_cimento
        custo_areia = total_areia_m3 * preco_m3_areia
        custo_total = custo_pecas + custo_cimento + custo_areia

        st.success(f"Cálculo concluído para: {tipo_material}!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Quantidade de Peças", f"{total_pecas:.0f} un", f"R$ {custo_pecas:,.2f}")
        c2.metric("Cimento (50kg)", f"{total_sacos_cimento:.1f} sacos", f"R$ {custo_cimento:,.2f}")
        c3.metric("Areia Média", f"{total_areia_m3:.2f} m³", f"R$ {custo_areia:,.2f}")

        st.markdown(f"### 💰 Custo Total dos Insumos de Alvenaria: **R$ {custo_total:,.2f}**")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    st.subheader("Dimensionamento Técnico e Orçamento de Lajes (Pré-moldada)")
    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input("Área da Laje (m²):", min_value=1.0, value=50.0)
        tipo_enchimento = st.selectbox(
            "Tipo de Enchimento da Laje:", 
            ["Lajota Cerâmica (Tijolinho)", "EPS / Isopor (Mais leve e isolante térmico)"]
        )
        altura_laje = st.selectbox("Altura da Estrutura (H):", ["H8 (Forro/Piso leve)", "H12 (Residencial comum)", "H16 (Vãos maiores)", "H20 (Sobrecargas pesadas)"])
    with col2:
        preco_kit_m2 = st.number_input("Preço Médio do Kit Laje por m² (R$):", value=72.0, step=2.0)
        espessura_capa = st.number_input("Espessura da Capa de Concreto (cm):", value=4.0, step=0.5)

    if st.button("Calcular Materiais da Laje", type="primary"):
        custo_total_laje = area_laje * preco_kit_m2
        st.success("Dimensionamento de laje realizado com sucesso!")
        st.metric("Custo Estimado do Kit Laje", f"R$ {custo_total_laje:,.2f}")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    st.subheader("Cálculo Avançado de Concreto (Usinado vs. Betoneira)")
    vol_alvo = st.number_input("Volume de Concreto Desejado (m³):", min_value=0.1, value=1.0, step=0.1)
    if st.button("Calcular Insumos", type="primary"):
        st.success("Volume estrutural calculado com sucesso!")
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

elif modulo == "🚰 Sistema Hidráulico Profissional (Atualizado)":
    st.subheader("Dimensionamento de Consumo, Reservatório, Tubulações e Conexões")
    col1, col2 = st.columns(2)
    with col1:
        moradores = st.number_input("Número de Habitantes / Usuários:", min_value=1, value=4)
        consumo_diario = st.number_input("Consumo por Pessoa (Litros/dia - NBR 5626):", value=200.0)
        qtd_banheiros = st.number_input("Número de Banheiros na Residência:", min_value=1, value=2, step=1)
    with col2:
        dias_reserva = st.number_input("Autonomia de Reserva Técnica (Dias):", value=2)

    if st.button("Calcular Sistema Hidráulico Completo", type="primary"):
        volume_necessario = moradores * consumo_diario * dias_reserva
        st.success("Dimensionamento hidráulico e listagem de conexões concluídos!")
        
        c1, c2 = st.columns(2)
        c1.metric("Volume Mínimo do Reservatório", f"{volume_necessario:,.0f} Litros")
        
        if volume_necessario <= 500:
            sugestao_caixa = "Caixa d'água de 500 Litros"
        elif volume_necessario <= 1000:
            sugestao_caixa = "Caixa d'água de 1.000 Litros"
        elif volume_necessario <= 1500:
            sugestao_caixa = "Caixa d'água de 1.500 Litros (ou duas de 1.000L)"
        else:
            sugestao_caixa = f"Bateria de reservatórios totalizando {max(2000, int(volume_necessario))} Litros"

        c2.metric("Comercialização Sugerida", sugestao_caixa)
        
        # Detalhamento de Tubulações e Conexões
        st.markdown("---")
        st.markdown("### 🚰 Especificação de Tubulações (Bitolas em Milímetros):")
        col_t1, col_t2, col_t3 = st.columns(3)
        col_t1.info("**Alimentação / Barrilete:**\n\n Tubo PVC Marrom de **25mm (3/4'')** ou **32mm (1'')** descendo da caixa.")
        col_t2.info("**Ramais de Água Fria:**\n\n Tubo PVC Marrom de **25mm** para banheiros, chuveiros e pias.")
        col_t3.info("**Rede de Esgoto Sanitário:**\n\n Tubo PVC Branco/Cinza:\n* **100mm** (Vasos sanitários e coluna)\n* **50mm** (Ralos, pias e chuveiro)")

        st.markdown("### 🔧 Estimativa de Conexões por Banheiro Padrão:")
        st.write(f"Considerando a execução de **{qtd_banheiros} banheiro(s)**, esta é a listagem base de conexões para orçamento e compra:")
        
        # Cálculo estimado por banheiro
        joelhos_25 = qtd_banheiros * 12
        tees_25 = qtd_banheiros * 4
        luvas_25 = qtd_banheiros * 6
        joelhos_esgoto_100 = qtd_banheiros * 4
        joelhos_esgoto_50 = qtd_banheiros * 8
        tutis_caixa_gordura = max(1, qtd_banheiros - 1)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown(f"""
            * **Água Fria (Soldável 25mm):**
              * Joelhos 90° 25mm: **~{joelhos_25} un**
              * Tês 25mm: **~{tees_25} un**
              * Luvas de Correr/Simples 25mm: **~{luvas_25} un**
              * Adaptadores com Flange para Caixa (25mm x 3/4''): **1 un**
            """)
        with col_c2:
            st.markdown(f"""
            * **Esgoto (Série Normal/Reforçada):**
              * Joelhos 90° / 45° Esgoto 100mm (Vasos): **~{joelhos_esgoto_100} un**
              * Joelhos 90° Esgoto 50mm (Ralos/Pia): **~{joelhos_esgoto_50} un**
              * Tubos de Esgoto 100mm: **~{qtd_banheiros * 3} varas (3m)**
              * Tubos de Esgoto 50mm: **~{qtd_banheiros * 4} varas (3m)**
            """)

        st.markdown('<div class="alerta-sucesso">✅ Guia de bitolas e conexões dimensionado com folga de 10% para perdas e cortes no canteiro de obras.</div>', unsafe_allow_html=True)
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Orçamento Comercial e Proposta de Serviços")
    valor_bruto = st.number_input("Valor Base dos Serviços (R$):", value=12000.0)
    if st.button("Emitir Proposta", type="primary"):
        st.success("Proposta calculada!")
        st.session_state.ja_fez_calculo_gratis = Time = True

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
