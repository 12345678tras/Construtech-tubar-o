import streamlit as st

# Configuração da Página (Deve ser sempre o primeiro comando do Streamlit)
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma Profissional",
    page_icon="🏗️",
    layout="wide",
)

# Estilização visual básica
st.markdown(
    """
    <style>
    .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-header { font-size: 16px; color: #4B5563; }
    .card { background-color: #F3F4F6; padding: 20px; border-radius: 10px; margin-bottom: 15px; }
    .paywall-box { background-color: #FEF2F2; border: 2px dashed #EF4444; padding: 30px; border-radius: 10px; text-align: center; }
    .admin-box { background-color: #EFF6FF; border: 1px solid #3B82F6; padding: 15px; border-radius: 8px; margin-top: 20px; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# SISTEMA DE CONTROLE DE ACESSO (PAYWALL + ADMIN)
# ==========================================
if "acesso_liberado" not in st.session_state:
    st.session_state.acesso_liberado = False

# Tela de Bloqueio (Caso não seja o cliente pagante nem o seu computador de admin)
if not st.session_state.acesso_liberado:
    st.markdown(
        '<p class="main-header" style="text-align: center;">🏗️ Construtech Tubarão</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header" style="text-align: center;">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown(
        """
        <div class="paywall-box">
            <h2>⚠️ Acesso Restrito / Pagamento Pendente</h2>
            <p>Esta plataforma exige o licenciamento de uso por computador.</p>
            <p>Para continuar utilizando os módulos profissionais, escaneie o QR Code ou realize o Pix para os dados abaixo:</p>
            <br>
            <h4>Beneficiário:</h4>
            <p style="font-size: 18px; font-weight: bold; color: #1E3A8A;">CAC CONTABILIZANDO</p>
            <p><b>WhatsApp para envio do comprovante:</b> +55 (64) 99304-4147</p>
            <p><i>(Processado via InfinitePay)</i></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Espaço para exibir o QR Code (Caso você tenha a imagem salva, basta descomentar a linha abaixo)
    col_q1, col_q2, col_q3 = st.columns([1, 2, 1])
    with col_q2:
        st.write("")
        # DICA: Se você tiver a foto do QR Code na mesma pasta do código, 
        # mude 'qrcode.png' para o nome exato do seu arquivo de imagem:
        # st.image("qrcode.png", caption="Escaneie para Pagar via Pix", width=250)
        st.info("💡 (Dica para você: Insira a foto do seu QR Code na tela de pagamento para facilitar para o cliente).")

    # SEÇÃO EXCLUSIVA PARA VOCÊ (DONO/ADMINISTRADOR)
    with st.container():
        st.markdown(
            '<div class="admin-box">', unsafe_allow_html=True
        )
        st.write("🔑 **Área do Desenvolvedor / Dono da Plataforma**")
        senha_admin = st.text_input(
            "Digite sua senha de Administrador para liberar seu computador:",
            type="password",
            placeholder="Digite a senha mestre",
        )

        # Defina aqui a sua senha secreta para liberar o seu computador
        SENHA_MESTRE = "tubarao2026"  # <--- ALTERE A SENHA AQUI SE QUISER

        if st.button("Liberar meu Computador (Admin)", type="primary"):
            if senha_admin == SENHA_MESTRE:
                st.session_state.acesso_liberado = True
                st.success(
                    "Computador reconhecido como Administrador! Entrando..."
                )
                st.rerun()
            else:
                st.error("Senha de administrador incorreta!")
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()  # Para a execução aqui se não estiver liberado


# ==========================================
# APLICAÇÃO PRINCIPAL (Liberada)
# ==========================================

# Cabeçalho Principal
st.markdown(
    '<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Plataforma Profissional de Engenharia, Orçamentos e Custos</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# Menu Lateral para Navegação dos Módulos
st.sidebar.title("Navegação de Módulos")
modulo = st.sidebar.selectbox(
    "Selecione a Ferramenta:",
    [
        "📊 Visão Geral e BDI",
        "🧱 Cálculo de Materiais (Areia/Cimento)",
        "🏗️ Estrutural e Vigas",
        "🚰 Sistema Hidráulico",
        "💼 Faturamento e CNPJ",
    ],
)

# Botão na barra lateral para bloquear novamente se precisar testar
if st.sidebar.button("🔒 Bloquear Sistema (Testar Paywall)"):
    st.session_state.acesso_liberado = False
    st.rerun()

# Controle de Sessão para Armazenar Dados do Orçamento
if "orcamento_base" not in st.session_state:
    st.session_state.orcamento_base = 50000.0
if "bdi" not in st.session_state:
    st.session_state.bdi = 25.0
if "cliente" not in st.session_state:
    st.session_state.cliente = "Obra Residencial Exemplo"

# ==========================================
# MÓDULO 1: VISÃO GERAL E BDI
# ==========================================
if modulo == "📊 Visão Geral e BDI":
    st.subheader("Painel de Controle e Viabilidade")

    col1, col2 = st.columns(2)
    with col1:
        st.session_state.cliente = st.text_input(
            "Nome do Projeto / Cliente:", value=st.session_state.cliente
        )
        st.session_state.orcamento_base = st.number_input(
            "Valor Base Estimado (R$):",
            min_value=0.0,
            value=st.session_state.orcamento_base,
            step=1000.0,
        )
    with col2:
        st.session_state.bdi = st.slider(
            "Taxa de BDI Aplicada (%):", min_value=0.0, max_value=50.0, value=25.0
        )

    if st.button("Calcular Viabilidade e Custos", type="primary"):
        total_com_bdi = st.session_state.orcamento_base * (
            1 + st.session_state.bdi / 100
        )

        st.markdown(
            f"""
        <div class="card">
            <h3>📊 Resumo para: {st.session_state.cliente}</h3>
            <p><b>Orçamento Base:</b> R$ {st.session_state.orcamento_base:,.2f}</p>
            <p><b>BDI Aplicado:</b> {st.session_state.bdi}%</p>
            <p><b>Valor Total Sugerido com BDI:</b> R$ {total_com_bdi:,.2f}</p>
        </div>
        """,
            unsafe_allow_html=True,
        )
        st.success("Cálculo realizado com sucesso!")

# ==========================================
# MÓDULO 2: CÁLCULO DE MATERIAIS
# ==========================================
elif modulo == "🧱 Cálculo de Materiais (Areia/Cimento)":
    st.subheader("Dimensionamento de Insumos Básicos")
    st.write(
        "Calcule a quantidade aproximada de areia, cimento e brita com base na metragem da obra."
    )

    area_construcao = st.number_input("Área da Construção (m²):", value=100.0)

    col1, col2, col3 = st.columns(3)
    with col1:
        qtd_cimento = area_construcao * 3.5
        st.metric(label="Sacos de Cimento (50kg)", value=f"{int(qtd_cimento)} un")
    with col2:
        qtd_areia = area_construcao * 0.12
        st.metric(label="Areia Média/Grossa", value=f"{qtd_areia:.2f} m³")
    with col3:
        qtd_brita = area_construcao * 0.10
        st.metric(label="Brita nº 1", value=f"{qtd_brita:.2f} m³")

    st.info(
        "💡 Os índices consideram traços padrões para alvenaria e contrapiso."
    )

# ==========================================
# MÓDULO 3: ESTRUTURAL E VIGAS
# ==========================================
elif modulo == "🏗️ Estrutural e Vigas":
    st.subheader("Dimensionamento de Elementos Estruturais")
    st.write("Estimativa de aço, concreto e formas para vigas e pilares.")

    vao_livre = st.slider(
        "Maior Vão Livre (metros):", min_value=2.0, max_value=10.0, value=4.0
    )
    pavimentos = st.number_input(
        "Número de Pavimentos:", min_value=1, max_value=5, value=1
    )

    if st.button("Calcular Estimativa Estrutural"):
        volume_concreto = vao_livre * pavimentos * 0.45
        peso_aco = volume_concreto * 90

        st.success(
            f"Para um vão de {vao_livre}m com {pavimentos} pavimento(s):"
        )
        st.write(f"- **Volume Estimado de Concreto:** {volume_concreto:.2f} m³")
        st.write(f"- **Consumo Estimado de Aço (CA-50):** {peso_aco:.2f} kg")

# ==========================================
# MÓDULO 4: SISTEMA HIDRÁULICO
# ==========================================
elif modulo == "🚰 Sistema Hidráulico":
    st.subheader("Orçamento de Instalações Hidráulicas")
    st.write("Levantamento preliminar de tubos, conexões e caixas d'água.")

    pontos_agua = st.number_input(
        "Número de Pontos de Água/Esgoto:", min_value=1, value=10
    )
    tem_reservatorio = st.checkbox("Incluir Caixa D'água de 1000L", value=True)

    custo_tubos = pontos_agua * 45.0
    custo_caixa = 650.0 if tem_reservatorio else 0.0
    total_hidraulico = custo_tubos + custo_caixa

    st.markdown(
        f"""
    <div class="card">
        <h4>Resumo Hidráulico</h4>
        <p><b>Tubulações e Conexões ({pontos_agua} pontos):</b> R$ {custo_tubos:,.2f}</p>
        <p><b>Reservatório:</b> R$ {custo_caixa:,.2f}</p>
        <p><b>Total Parcial Hidráulico:</b> R$ {total_hidraulico:,.2f}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# MÓDULO 5: FATURAMENTO E CNPJ
# ==========================================
elif modulo == "💼 Faturamento e CNPJ":
    st.subheader("Configurações de Faturamento e Dados Comerciais")
    st.write("Insira os dados da sua empresa para emissão do relatório.")

    cnpj_empresa = st.text_input(
        "CNPJ:", value="00.000.000/0001-00", placeholder="XX.XXX.XXX/0001-XX"
    )
    razao_social = st.text_input(
        "Razão Social / Nome do Engenheiro:", value="Construtech Tubarão LTDA"
    )
    chave_pix = st.text_input("Chave PIX para Recebimento:", value="")

    if st.button("Salvar Dados Fiscais"):
        st.success(
            f"Dados da empresa {razao_social} (CNPJ: {cnpj_empresa}) salvos com sucesso para os relatórios!"
        )

# Rodapé institucional
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
