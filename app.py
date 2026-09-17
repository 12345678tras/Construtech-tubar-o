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
        "⚙️ Projeto de Aço com Alerta de Segurança",
        "🏗️ Estrutural, Vigas e Validação Técnica",
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
        
        # Alerta prático de mestre de obras
        if area_paredes > 150 and tipo_material == "Bloco Cerâmico 9x19x19 cm":
            st.markdown('<div class="alerta-atencao">⚠️ Alerta de Prática: Para paredes longas com bloco de 9cm, certifique-se de prever pilaretes de encunhamento/amarração a cada 3m para evitar trincas e fissuras.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">✅ Traço e consumo dimensionados dentro dos padrões usuais de mercado e perda de obra de 5%.</div>', unsafe_allow_html=True)

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
        volume_concreto_capa = area_laje * (espessura_capa / 100.0)
        metros_vigotas = area_laje * 1.7
        pecas_enchimento_m2 = 8 if "Cerâmica" in tipo_enchimento else 3.3
        total_pecas_enchimento = area_laje * pecas_enchimento_m2

        st.success("Dimensionamento de laje realizado com sucesso!")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Vigotas Treliçadas", f"{metros_vigotas:.1f} m")
        c2.metric("Enchimento Necessário", f"{total_pecas_enchimento:.0f} un", f"({tipo_enchimento})")
        c3.metric("Concreto para Capa", f"{volume_concreto_capa:.2f} m³")

        st.markdown(f"### 💰 Custo Estimado do Kit Laje: **R$ {custo_total_laje:,.2f}**")

        # Alerta técnico de laje
        if "H8" in altura_laje and area_laje > 40:
            st.markdown('<div class="alerta-perigo">🚨 ALERTA TÉCNICO: Lajes do tipo H8 para áreas maiores que 40m² exigem cuidados rigorosos com contraflecha e escoramento intermediário para evitar deformações excessivas ("barrigas"). Considere H12 ou superior caso haja tráfego ou paredes em cima.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">✅ Altura de laje compatível com o dimensionamento padrão de boa estabilidade.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "⚙️ Projeto de Aço com Alerta de Segurança":
    st.subheader("Especificação, Custo e Auditoria de Armadura (CA-50 / CA-60)")
    col1, col2 = st.columns(2)
    with col1:
        area_construida = st.number_input("Área Construída da Obra (m²):", min_value=10.0, value=100.0)
        consumo_medio_aco = st.selectbox(
            "Padrão de Armadura Desejado:", 
            ["Leve / Residencial Padrão (8 kg/m² - ATENÇÃO)", "Ideal / Residencial Comum (12 kg/m²)", "Robusto / Sobrado Estruturado (16 kg/m²)"]
        )
    with col2:
        preco_kg = st.number_input("Preço Médio do Aço por kg (R$):", value=11.50, step=0.50)

    if st.button("Gerar Detalhamento e Auditoria de Aço", type="primary"):
        fator = 8 if "8 kg" in consumo_medio_aco else (12 if "12 kg" in consumo_medio_aco else 16)
        peso_total_kg = area_construida * fator
        
        peso_10mm = peso_total_kg * 0.45
        peso_8mm = peso_total_kg * 0.35
        peso_63mm = peso_total_kg * 0.20
        custo_total_aco = peso_total_kg * preco_kg

        st.success("Detalhamento e verificação de ferragens concluídos!")
        st.write(f"**Peso Total Estimado de Aço:** `{peso_total_kg:.1f} kg` | **Custo Total:** `R$ {custo_total_aco:,.2f}`")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Aço 10.0 mm (3/8'')", f"{peso_10mm:.1f} kg")
        c2.metric("Aço 8.0 mm (5/16'')", f"{peso_8mm:.1f} kg")
        c3.metric("Aço 6.3 mm (1/4'')", f"{peso_63mm:.1f} kg")

        # Alerta de engenharia para aço subdimensionado
        if fator <= 8:
            st.markdown('<div class="alerta-perigo">🚨 ALERTA DE ENGENHARIA: 8 kg/m² é uma taxa considerada MUITO FRACA e subdimensionada para construções convencionais. Risco alto de fissuração excessiva nas vigas e lajes, além de flechas acentuadas. Recomenda-se elevar para no mínimo 12 kg/m².</div>', unsafe_allow_html=True)
        elif fator == 12:
            st.markdown('<div class="alerta-sucesso">✅ Taxa de aço adequada e segura para residências térreas ou sobrados de padrão comum.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alerta-sucesso">✅ Armadura robusta, excelente margem de segurança estrutural.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🏗️ Estrutural, Vigas e Validação Técnica":
    st.subheader("Dimensionamento, Verificação de Vãos e Alerta de Viga Fraca")
    col1, col2 = st.columns(2)
    with col1:
        vao_viga = st.number_input("Vão Livre da Viga (m):", min_value=1.0, value=4.5)
        altura_escolhida_cm = st.number_input("Altura da Viga Adotada na Obra (cm):", min_value=10.0, value=30.0)
    with col2:
        fck = st.selectbox("Resistência do Concreto (fck):", [20, 25, 30, 35])
        tipo_apoio = st.selectbox("Condição do Apoio:", ["Viga Biapoiada Comum", "Viga com Extremo Contínuo"])

    if st.button("Validar Segurança da Viga", type="primary"):
        # Regra prática de engenharia: altura mínima L/10 ou L/12
        altura_minima_tecnica = (vao_viga * 100) / 12
        base_sugerida = altura_escolhida_cm / 2.5

        st.success("Análise estrutural processada!")
        c1, c2 = st.columns(2)
        c1.metric("Altura Mínima Requerida (L/12)", f"{altura_minima_tecnica:.1f} cm")
        c2.metric("Base Recomendada", f"{base_sugerida:.0f} cm")

        # Alertas detalhados de engenharia
        if altura_escolhida_cm < altura_minima_tecnica:
            st.markdown(f'<div class="alerta-perigo">🚨 ALERTA DE VIGA FRACA: A altura de {altura_escolhida_cm} cm escolhida para um vão de {vao_viga}m é INSUFICIENTE (abaixo do limite técnico de {altura_minima_tecnica:.1f} cm). Isso pode gerar deformações severas, flechas indesejadas e trincas nas paredes superiores. Aumente a altura da viga!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="alerta-sucesso">✅ Viga estruturalmente segura! A altura de {altura_escolhida_cm} cm atende aos critérios de rigidez para o vão de {vao_viga}m.</div>', unsafe_allow_html=True)

        st.session_state.ja_fez_calculo_gratis = True

elif modulo == "🚰 Sistema Hidráulico Profissional":
    st.subheader("Dimensionamento de Consumo, Reservatório e Tubulações")
    col1, col2 = st.columns(2)
    with col1:
        moradores = st.number_input("Número de Habitantes / Usuários:", min_value=1, value=4)
        consumo_diario = st.number_input("Consumo por Pessoa (Litros/dia - NBR 5626):", value=200.0)
    with col2:
        dias_reserva = st.number_input("Autonomia de Reserva Técnica (Dias):", value=2)

    if st.button("Calcular Sistema Hidráulico", type="primary"):
        volume_necessario = moradores * consumo_diario * dias_reserva
        st.success("Dimensionamento hidráulico concluído!")
        
        c1, c2 = st.columns(2)
        c1.metric("Volume Mínimo do Reservatório", f"{volume_necessario:,.0f} Litros")
        
        # Sugestão comercial de caixas d'água no Brasil (500L, 1000L, 1500L, 2000L)
        if volume_necessario <= 500:
            sugestao_caixa = "Caixa d'água de 500 Litros"
        elif volume_necessario <= 1000:
            sugestao_caixa = "Caixa d'água de 1.000 Litros"
        elif volume_necessario <= 1500:
            sugestao_caixa = "Caixa d'água de 1.500 Litros (ou duas de 1.000L)"
        else:
            sugestao_caixa = f"Bateria de reservatórios totalizando {max(2000, int(volume_necessario))} Litros"

        c2.metric("Comercialização Sugerida", sugestao_caixa)
        
        st.markdown(f'<div class="alerta-sucesso">✅ Dimensionamento hidráulico calculado conforme diretrizes de consumo residencial. Recomendado utilizar tubulação principal de PVC marrom de 25mm (3/4\') para alimentação dos banheiros e cozinha.</div>', unsafe_allow_html=True)
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
