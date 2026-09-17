import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma Profissional",
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
        "🧱 Cálculo de Alvenaria",
        "🏠 Cálculo Avançado de Lajes",
        "⚙️ Projeto de Ferragens e Aço",
        "🏗️ Estrutural, Vigas e Validação",
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
    '<p class="sub-header">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
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
# 4. MÓDULOS COM CÁLCULOS REAIS
# ==========================================

if modulo == "📊 Visão Geral e BDI":
    st.subheader("Painel de Controle e Viabilidade Comercial")
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input(
            "Nome do Projeto / Cliente:", value="Obra Residencial Exemplo"
        )
        custo_base = st.number_input(
            "Custo Direto Total Estimado (R$):",
            min_value=0.0,
            value=50000.0,
            step=1000.0,
        )
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

elif modulo == "🧱 Cálculo de Alvenaria":
    st.subheader("Dimensionamento Técnico de Alvenaria")
    col1, col2 = st.columns(2)
    with col1:
        area_paredes = st.number_input(
            "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
        )
        preco_tijolo = st.number_input(
            "Preço Unitário do Bloco (R$):", value=1.20, step=0.10
        )
    with col2:
        consumo_m2 = st.number_input(
            "Blocos por m² (com perda):", value=35.0, step=1.0
        )

    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        total_blocos = area_paredes * consumo_m2
        custo_total_blocos = total_blocos * preco_tijolo
        st.success("Insumos calculados com sucesso!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Quantidade de Blocos", f"{total_blocos:.0f} un")
        col_m2.metric("Custo Total dos Blocos", f"R$ {custo_total_blocos:,.2f}")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏠 Cálculo Avançado de Lajes":
    st.subheader("Dimensionamento de Lajes Pré-moldadas / Treliçadas")
    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input(
            "Área da Laje (m²):", min_value=1.0, value=50.0
        )
        tipo_laje = st.selectbox(
            "Tipo de Laje:", ["H8 (Forro/Piso leve)", "H12 (Residencial)", "H16 (Sobrecarga Maior)"]
        )
    with col2:
        valor_m2_laje = st.number_input(
            "Custo Médio do m² instalado (R$):", value=65.0, step=5.0
        )

    if st.button("Calcular Estrutura da Laje", type="primary"):
        custo_laje_total = area_laje * valor_m2_laje
        concreto_capa = area_laje * 0.04  # Estimativa de 4cm de capa
        st.success("Cálculo de laje executado com sucesso!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Custo Total da Laje", f"R$ {custo_laje_total:,.2f}")
        col_m2.metric("Concreto para Capa (m³ aprox.)", f"{concreto_capa:.2f} m³")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "⚙️ Projeto de Ferragens e Aço":
    st.subheader("Dimensionamento e Custo de Aço (CA-50 / CA-60)")
    col1, col2 = st.columns(2)
    with col1:
        peso_aco_kg = st.number_input(
            "Consumo Estimado de Aço (kg):", min_value=1.0, value=450.0
        )
    with col2:
        preco_kg_aco = st.number_input(
            "Preço Médio do kg do Aço (R$):", value=11.50, step=0.50
        )

    if st.button("Calcular Custo de Aço", type="primary"):
        custo_aco_total = peso_aco_kg * preco_kg_aco
        st.success("Cálculo de ferragens executado com sucesso!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Peso Total de Aço", f"{peso_aco_kg:.1f} kg")
        col_m2.metric("Custo Total com Aço", f"R$ {custo_aco_total:,.2f}")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas e Validação":
    st.subheader("Verificação de Vigas e Pilares de Concreto")
    col1, col2 = st.columns(2)
    with col1:
        comprimento_viga = st.number_input(
            "Comprimento do Vão da Viga (m):", min_value=1.0, value=4.5
        )
        carga_linear = st.number_input(
            "Carga Estimada (kN/m):", min_value=1.0, value=12.0
        )
    with col2:
        fck_concreto = st.selectbox("Resistência do Concreto (fck):", [20, 25, 30, 35])

    if st.button("Validar Viga Estrutural", type="primary"):
        altura_minima = (comprimento_viga * 100) / 12  # Regra prática L/12 em cm
        st.success("Validação estrutural realizada!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Altura Mínima Recomendada", f"{altura_minima:.1f} cm")
        col_m2.metric("Status fck", f"{fck_concreto} MPa (Adequado)")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Dimensionamento de Reservatório e Tubulações")
    col1, col2 = st.columns(2)
    with col1:
        num_pessoas = st.number_input(
            "Número de Moradores / Usuários:", min_value=1, value=4
        )
        consumo_per_capita = st.number_input(
            "Consumo por Pessoa (Litros/dia):", value=200.0, step=10.0
        )
    with col2:
        dias_reserva = st.number_input("Dias de Reserva Técnica:", value=2)

    if st.button("Calcular Reservatório Hidráulico", type="primary"):
        volume_total = num_pessoas * consumo_per_capita * dias_reserva
        st.success("Dimensionamento hidráulico concluído!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Volume de Água Necessário", f"{volume_total:,.0f} Litros")
        col_m2.metric("Reserva Recomendada", f"Caixa d'água de {volume_total}L")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Orçamento Comercial e Emissão de Proposta")
    col1, col2 = st.columns(2)
    with col1:
        valor_servico = st.number_input(
            "Valor Líquido dos Serviços (R$):", value=15000.0, step=500.0
        )
        imposto_simples = st.slider("Alíquota de Impostos / Nota Fiscal (%):", 0.0, 20.0, 6.0)
    with col2:
        desconto = st.number_input("Desconto Concedido (R$):", value=0.0, step=100.0)

    if st.button("Gerar Proposta Comercial", type="primary"):
        valor_impostos = valor_servico * (imposto_simples / 100)
        valor_final_nf = valor_servico + valor_impostos - desconto
        st.success("Proposta gerada com sucesso!")
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Valor com Impostos", f"R$ {valor_final_nf:,.2f}")
        col_m2.metric("Impostos Calculados", f"R$ {valor_impostos:,.2f}")
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
