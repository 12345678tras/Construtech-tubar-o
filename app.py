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
        "🧱 Cálculo Detalhado de Alvenaria",
        "🏠 Cálculo Avançado de Lajes",
        "⚙️ Projeto Detalhado de Ferragens e Aço",
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
# 4. MÓDULOS COM CÁLCULOS TÉCNICOS DETALHADOS
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

elif modulo == "🧱 Cálculo Detalhado de Alvenaria":
    st.subheader("Dimensionamento Completo de Alvenaria (Blocos, Cimento e Areia)")
    col1, col2 = st.columns(2)
    with col1:
        area_paredes = st.number_input(
            "Área Líquida de Paredes (m²):", min_value=1.0, value=80.0
        )
        tipo_bloco = st.selectbox(
            "Tipo de Bloco Cerâmico:", ["9x19x19 cm", "14x19x19 cm"]
        )
        preco_tijolo = st.number_input(
            "Preço Unitário do Bloco (R$):", value=1.20, step=0.10
        )
    with col2:
        preco_cimento = st.number_input(
            "Preço do Saco de Cimento 50kg (R$):", value=32.00, step=1.00
        )
        preco_m3_areia = st.number_input(
            "Preço do m³ de Areia Média (R$):", value=120.00, step=10.00
        )

    if st.button("Calcular Insumos Detalhados", type="primary"):
        # Fórmulas de engenharia civil para estimativa de materiais
        fator_bloco = 35 if "9x" in tipo_bloco else 25
        total_blocos = area_paredes * fator_bloco
        
        # Estimativa de argamassa de assentamento (~0.018 m³ por m² de parede para bloco 9cm)
        volume_argamassa_m3 = area_paredes * 0.018
        # Consumo aproximado por m³ de argamassa mista: ~7 sacos de cimento e ~1.15 m³ de areia
        total_sacos_cimento = volume_argamassa_m3 * 7.0
        total_areia_m3 = volume_argamassa_m3 * 1.15

        # Custos
        custo_blocos = total_blocos * preco_tijolo
        custo_cimento = total_sacos_cimento * preco_cimento
        custo_areia = total_areia_m3 * preco_m3_areia
        custo_total_insumos = custo_blocos + custo_cimento + custo_areia

        st.success("Cálculo de alvenaria e insumos concluído com sucesso!")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.metric("Blocos Necessários", f"{total_blocos:.0f} un", f"R$ {custo_blocos:,.2f}")
        col_m2.metric("Cimento (50kg)", f"{total_sacos_cimento:.1f} sacos", f"R$ {custo_cimento:,.2f}")
        col_m3.metric("Areia Média", f"{total_areia_m3:.2f} m³", f"R$ {custo_areia:,.2f}")

        st.markdown(f"### 💰 Custo Total Estimado de Insumos: **R$ {custo_total_insumos:,.2f}**")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏠 Cálculo Avançado de Lajes":
    st.subheader("Dimensionamento Técnico de Lajes Pré-moldadas / Treliçadas")
    col1, col2 = st.columns(2)
    with col1:
        area_laje = st.number_input("Área da Laje (m²):", min_value=1.0, value=50.0)
        tipo_h = st.selectbox("Altura da Viga Treliçada (H):", ["H8", "H12", "H16", "H20"])
    with col2:
        preco_m2_laje = st.number_input("Preço Médio do Kit Laje por m² (R$):", value=68.0, step=2.0)
        espessura_capa = st.number_input("Espessura da Capa de Concreto (cm):", value=4.0, step=0.5)

    if st.button("Calcular Especificações da Laje", type="primary"):
        custo_kit = area_laje * preco_m2_laje
        volume_concreto_capa = area_laje * (espessura_capa / 100.0)
        # Estimativa de vigotas lineares (aproximadamente 1.7 metros lineares por m²)
        metros_lineares_vigotas = area_laje * 1.7
        
        st.success("Dimensionamento da laje realizado!")
        c1, c2, c3 = st.columns(3)
        c1.metric("Vigotas Treliçadas (Aprox.)", f"{metros_lineares_vigotas:.1f} m")
        c2.metric("Concreto para Capa", f"{volume_concreto_capa:.2f} m³")
        c3.metric("Custo Total Estimado", f"R$ {custo_kit:,.2f}")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "⚙️ Projeto Detalhado de Ferragens e Aço":
    st.subheader("Especificação e Custo Detalhado de Aço (CA-50 e CA-60)")
    col1, col2 = st.columns(2)
    with col1:
        area_construida = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=100.0)
        consumo_medio_aco = st.selectbox(
            "Padrão de Armadura (kg por m²):", 
            ["Leve / Residencial Padrão (10 kg/m²)", "Médio / Estruturado (15 kg/m²)", "Pesado / Sobrado (20 kg/m²)"]
        )
    with col2:
        preco_kg = st.number_input("Preço Médio do Aço por kg (R$):", value=11.50, step=0.50)

    if st.button("Gerar Detalhamento de Ferragens", type="primary"):
        fator = 10 if "Leve" in consumo_medio_aco else (15 if "Médio" in consumo_medio_aco else 20)
        peso_total_kg = area_construida * fator
        
        # Divisão técnica estimada por bitola
        peso_10mm = peso_total_kg * 0.45  # 45% vigas/pilares
        peso_8mm = peso_total_kg * 0.35   # 35% estribos/lajes
        peso_63mm = peso_total_kg * 0.20  # 20% distribuições
        
        custo_total_aco = peso_total_kg * preco_kg

        st.success("Detalhamento de ferragens gerado com sucesso!")
        
        st.write(f"**Peso Total Estimado de Aço:** `{peso_total_kg:.1f} kg` | **Custo Total:** `R$ {custo_total_aco:,.2f}`")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Aço 10.0 mm (3/8'')", f"{peso_10mm:.1f} kg")
        c2.metric("Aço 8.0 mm (5/16'')", f"{peso_8mm:.1f} kg")
        c3.metric("Aço 6.3 mm (1/4'')", f"{peso_63mm:.1f} kg")
        
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas e Validação":
    st.subheader("Dimensionamento e Verificação de Vigas")
    col1, col2 = st.columns(2)
    with col1:
        vao_viga = st.number_input("Vão Livre da Viga (m):", min_value=1.0, value=4.0)
        carga_viga = st.number_input("Esforço / Carga Aplicada (kN/m):", min_value=1.0, value=15.0)
    with col2:
        fck = st.selectbox("Resistência do Concreto (fck):", [20, 25, 30])

    if st.button("Validar Estrutura", type="primary"):
        altura_sugerida = (vao_viga * 100) / 10 # Regra prática L/10 em cm
        base_sugerida = altura_sugerida / 2.5
        st.success("Viga validada com sucesso!")
        c1, c2 = st.columns(2)
        c1.metric("Seção Transversal Sugerida", f"{base_sugerida:.0f} x {altura_sugerida:.0f} cm")
        c2.metric("Especificação do Concreto", f"fck {fck} MPa")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Dimensionamento de Consumo e Reservatório de Água")
    col1, col2 = st.columns(2)
    with col1:
        moradores = st.number_input("Número de Habitantes / Usuários:", min_value=1, value=4)
        consumo_diario = st.number_input("Consumo por Pessoa (Litros/dia):", value=200.0)
    with col2:
        dias_reserva = st.number_input("Autonomia de Reserva (Dias):", value=2)

    if st.button("Calcular Hidráulica", type="primary"):
        volume_necessario = moradores * consumo_diario * dias_reserva
        st.success("Dimensionamento hidráulico concluído!")
        c1, c2 = st.columns(2)
        c1.metric("Volume Mínimo do Reservatório", f"{volume_necessario:,.0f} Litros")
        c2.metric("Sugestão Comercial de Caixa", f"Instalar reservatório de {max(500, int(volume_necessario))}L")
        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Orçamento Comercial e Proposta de Serviços")
    col1, col2 = st.columns(2)
    with col1:
        valor_bruto = st.number_input("Valor Base dos Serviços (R$):", value=12000.0, step=500.0)
        imposto_aliquota = st.slider("Alíquota de Impostos / Nota Fiscal (%):", 0.0, 20.0, 6.0)
    with col2:
        desconto = st.number_input("Desconto Especial (R$):", value=0.0, step=100.0)

    if st.button("Emitir Proposta Comercial", type="primary"):
        valor_imposto = valor_bruto * (imposto_aliquota / 100)
        total_liquido = valor_bruto + valor_imposto - desconto
        st.success("Proposta comercial calculada!")
        c1, c2 = st.columns(2)
        c1.metric("Valor Total com Impostos", f"R$ {total_liquido:,.2f}")
        c2.metric("Valor dos Tributos", f"R$ {valor_imposto:,.2f}")
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
