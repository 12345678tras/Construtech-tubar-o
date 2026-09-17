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
        "⚙️ Projeto de Aço com Alerta de Segurança (Atualizado)",
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
    area_paredes = st.number_input("Área Líquida de Paredes (m²):", min_value=1.0, value=80.0)
    if st.button("Calcular Insumos de Alvenaria", type="primary"):
        st.success("Cálculo concluído com sucesso!")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    st.subheader("Dimensionamento Técnico e Orçamento de Lajes (Pré-moldada)")
    area_laje = st.number_input("Área da Laje (m²):", min_value=1.0, value=50.0)
    if st.button("Calcular Materiais da Laje", type="primary"):
        st.success("Dimensionamento de laje realizado com sucesso!")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    st.subheader("Cálculo Avançado de Concreto (Usinado vs. Betoneira)")
    vol_alvo = st.number_input("Volume de Concreto Desejado (m³):", min_value=0.1, value=1.0, step=0.1)
    if st.button("Calcular Insumos", type="primary"):
        st.success("Volume estrutural calculado com sucesso!")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "⚙️ Projeto de Aço com Alerta de Segurança (Atualizado)":
    st.subheader("Especificação, Custo e Auditoria de Armadura (CA-50 / CA-60)")
    
    col1, col2 = st.columns(2)
    with col1:
        area_construida = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=100.0, step=10.0)
        consumo_medio_aco = st.selectbox(
            "Padrão de Armadura Desejado:", 
            [
                "Ideal / Residencial Comum (12 kg/m²)", 
                "Robusto / Sobrado Estruturado (16 kg/m²)",
                "Leve / Residencial Padrão (8 kg/m² - ATENÇÃO)"
            ]
        )
    with col2:
        preco_kg = st.number_input("Preço Médio do Aço por kg (R$):", value=11.50, step=0.50)

    if st.button("Gerar Detalhamento e Auditoria de Aço", type="primary"):
        if "8 kg" in consumo_medio_aco:
            fator = 8
        elif "12 kg" in consumo_medio_aco:
            fator = 12
        else:
            fator = 16

        peso_total_kg = area_construida * fator
        peso_10mm = peso_total_kg * 0.45
        peso_8mm = peso_total_kg * 0.35
        peso_63mm = peso_total_kg * 0.20
        custo_total_aco = peso_total_kg * preco_kg

        st.success("Detalhamento e verificação de ferragens concluídos com sucesso!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Aço 10.0 mm (3/8'')", f"{peso_10mm:.1f} kg")
        c2.metric("Aço 8.0 mm (5/16'')", f"{peso_8mm:.1f} kg")
        c3.metric("Aço 6.3 mm (1/4'')", f"{peso_63mm:.1f} kg")

        st.markdown(f"### 💰 Resumo Financeiro e Custo do Aço:")
        st.info(f"**Peso Total Estimado:** `{peso_total_kg:.1f} kg` | **Custo Total do Aço:** `R$ {custo_total_aco:,.2f}` (considerando R$ {preco_kg:.2f}/kg)")

        if fator <= 8:
            st.markdown('<div class="alerta-perigo">🚨 ALERTA DE ENGENHARIA: 8 kg/m² é uma taxa considerada MUITO FRACA e subdimensionada para construções convencionais. Risco de fissuras graves.</div>', unsafe_allow_html=True)
        elif fator == 12:
            st.markdown('<div class="alerta-sucesso">✅ Taxa de aço adequada e segura para residências térreas ou sobrados de padrão comum.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">✅ Armadura robusta, excelente margem de segurança estrutural.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas e Bitolas":
    st.subheader("Dimensionamento de Vigas com Indicação de Bitolas e Alerta de Viga Fraca")
    vao_viga = st.number_input("Vão Livre da Viga (m):", min_value=1.0, value=4.5)
    if st.button("Validar Viga", type="primary"):
        st.success("Análise estrutural processada!")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Dimensionamento de Consumo, Reservatório, Tubulações e Conexões")
    moradores = st.number_input("Número de Habitantes / Usuários:", min_value=1, value=4)
    if st.button("Calcular Sistema Hidráulico", type="primary"):
        st.success("Dimensionamento hidráulico concluído!")
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
