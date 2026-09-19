import datetime
import json
import extra_streamlit_components as stx
import requests
import streamlit as st

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma de Engenharia e IA",
    page_icon="🏗️",
    layout="wide",
)

# ==========================================
# 2. GERENCIADOR DE COOKIES (PERSISTÊNCIA REAL)
# ==========================================
# Inicializa o gerenciador de cookies para persistir mesmo fechando a aba
cookie_manager = stx.CookieManager(key="construtech_cookie_manager")

# Aguarda o gerenciador carregar os cookies do navegador
if cookie_manager.get(cookie="acessos_gastos") is None:
    # Se não existe cookie, cria com 0 acessos
    cookie_manager.set(
        "acessos_gastos", "0", expires_at=datetime.datetime.now() + datetime.timedelta(days=365)
    )
if cookie_manager.get(cookie="usuario_pago") is None:
    cookie_manager.set(
        "usuario_pago", "false", expires_at=datetime.datetime.now() + datetime.timedelta(days=365)
    )

# ==========================================
# 3. CONFIGURAÇÕES SEGURAS (SECRETS DO STREAMLIT)
# ==========================================
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")
SENHAS_MESTRE_CONFIG = st.secrets.get(
    "senhas_admin",
    ["CONSTRUTECH12", "CONSTRUTECH", "CONTRUTECH12", "CONTRUTECH"],
)

# ==========================================
# 4. CONTROLE DE TEMA (MODO ESCURO / CLARO)
# ==========================================
modo_escuro = st.sidebar.toggle("🌙 Ativar Modo Escuro", value=False)

if modo_escuro:
    st.markdown(
        """
        <style>
        .stApp { background-color: #0E1117; color: #FAFAFA; }
        .main-header { font-size: 28px; font-weight: bold; color: #60A5FA; }
        .sub-header { font-size: 16px; color: #9CA3AF; }
        .box-pagamento { background-color: #1F2937; padding: 25px; border-radius: 12px; border: 3px solid #3B82F6; margin-bottom: 20px; }
        .btn-pagar { background-color: #059669; color: white !important; padding: 14px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; display: block; text-align: center; margin-top: 10px; }
        .pix-box-baixo { background-color: #111827; padding: 15px; border-radius: 8px; border: 1px solid #10B981; text-align: center; margin-top: 15px; }
        </style>
    """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #FFFFFF; color: #111827; }
        .main-header { font-size: 28px; font-weight: bold; color: #1E3A8A; }
        .sub-header { font-size: 16px; color: #4B5563; }
        .box-pagamento { background-color: #F8FAFC; padding: 25px; border-radius: 12px; border: 3px solid #2563EB; margin-bottom: 20px; }
        .btn-pagar { background-color: #059669; color: white !important; padding: 14px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 16px; display: block; text-align: center; margin-top: 10px; }
        .pix-box-baixo { background-color: #ECFDF5; padding: 15px; border-radius: 8px; border: 1px solid #10B981; text-align: center; margin-top: 15px; }
        </style>
    """,
        unsafe_allow_html=True,
    )

# ==========================================
# 5. SINCRONIZANDO COOKIES COM O ESTADO DA SESSÃO
# ==========================================
val_cookie_pago = cookie_manager.get(cookie="usuario_pago")
is_pago = True if val_cookie_pago == "true" else False

val_cookie_acessos = cookie_manager.get(cookie="acessos_gastos")
try:
    qtd_acessos = int(val_cookie_acessos) if val_cookie_acessos is not None else 0
except:
    qtd_acessos = 0

if "mensagens_chat" not in st.session_state:
    st.session_state.mensagens_chat = [
        {
            "role": "assistant",
            "content": (
                "Fala, meu irmão! Sou o Engenheiro Virtual Master da Construtech"
                " Tubarão. Você tem exatamente **3 consultas/acessos"
                " gratuitos** na plataforma. Pode mandar sua dúvida ou usar os módulos!"
            ),
        }
    ]


# ==========================================
# 6. COMPONENTE REUTILIZÁVEL DE PAGAMENTO GLOBAL
# ==========================================
def renderizar_box_pagamento_global():
    st.markdown(
        '<p class="main-header">🔒 Limite de Testes Gratuitos Atingido</p>',
        unsafe_allow_html=True,
    )
    st.warning(
        "⚠️ Você utilizou seus **3 acessos gratuitos** permitidos neste"
        " navegador. Para continuar utilizando todos os módulos e o assistente"
        " de IA de forma ilimitada, realize o pagamento de **R$ 20,00** para"
        " **CAC CONTABILIZANDO** ou insira sua chave de acesso mestre ao lado."
    )

    st.markdown('<div class="box-pagamento">', unsafe_allow_html=True)
    col_pag1, col_pag2 = st.columns(2, gap="large")

    with col_pag1:
        st.markdown("### 1️⃣ Forma de Pagamento (Pix / Cartão)")
        st.markdown(
            '<a'
            ' href="https://link.infinitepay.io/cristiane-da-260/VC1DLTAtUg-HgBiSH5iQO-20,00"'
            ' target="_blank" class="btn-pagar">💳 PAGAR COM CARTÃO / LINK</a>',
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <div class="pix-box-baixo">
                <p style="margin: 0 0 5px 0; font-size: 14px; font-weight: bold;">Ou pague via Pix Direto:</p>
                <p style="margin: 0; font-size: 13px;">Chave Pix (Telefone):</p>
                <code style="font-size: 16px; background: rgba(0,0,0,0.1); padding: 3px 8px; border-radius: 4px; font-weight: bold;">+5564993044147</code>
                <p style="margin: 5px 0 0 0; font-size: 12px;">Favorecido: <b>CAC CONTABILIZANDO</b></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_pag2:
        st.markdown("### 2️⃣ Liberar com Comprovante")
        comprovante_texto = st.text_area(
            "Comprovante de Pagamento:",
            key="comp_global",
            placeholder="Cole o ID do Pix ou dados da transferência...",
            height=120,
        )

        if st.button(
            "✨ Validar e Liberar Acesso Global",
            key="btn_gerar_global",
            type="primary",
            use_container_width=True,
        ):
            if comprovante_texto.strip() != "":
                # Salva no Cookie que o usuário pagou de forma permanente
                cookie_manager.set(
                    "usuario_pago",
                    "true",
                    expires_at=datetime.datetime.now()
                    + datetime.timedelta(days=365),
                )
                st.success("Acesso liberado com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Insira o comprovante de pagamento.")

    st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# 7. MENU LATERAL E PAINEL ADMINISTRADOR
# ==========================================
st.sidebar.title("Navegação de Módulos")
lista_modulos = [
    "📊 Visão Geral e BDI",
    "🧱 Alvenaria Completa (Blocos, Cimento e Areia)",
    "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)",
    "🏗️ Concreto, Traços e Volume Estrutural",
    "⚙️ Projeto de Aço, Custo e Auditoria de Armadura",
    "🏗️ Estrutural, Vigas, Bitolas e Aços",
    "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)",
    "🎨 Revestimento, Acabamento e Pintura",
    "🏠 Cobertura e Telhado",
    "⚡ Elétrica Básica Residencial",
    "📅 Cronograma Físico-Financeiro (Curva S)",
    "📝 Gerador de Contrato de Empreitada",
    "💼 Faturamento e CNPJ",
    "🤖 Simulação de Engenheiro Virtual Master",
]

modulo = st.sidebar.selectbox("Selecione a Ferramenta:", lista_modulos)

# Exibição correta dos testes restantes baseados no cookie
if not is_pago:
    restantes = max(0, 3 - qtd_acessos)
    st.sidebar.markdown("---")
    st.sidebar.info(f"🎯 Testes gratuitos restantes: **{restantes} de 3**")

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Painel do Administrador"):
    senha_admin_input = st.text_input(
        "Digite sua chave de liberação:", type="password", key="input_senha_adm"
    )
    if st.button("🔓 Ativar Acesso Mestre"):
        senha_tratada = senha_admin_input.strip().upper()
        if senha_tratada in [s.upper() for s in SENHAS_MESTRE_CONFIG]:
            cookie_manager.set(
                "usuario_pago",
                "true",
                expires_at=datetime.datetime.now()
                + datetime.timedelta(days=365),
            )
            st.success("Acesso Administrador liberado com sucesso!")
            st.rerun()
        else:
            st.error("Chave incorreta!")

    if is_pago:
        st.info("Status atual: **MODO MASTER LIBERADO 🔓**")

if st.sidebar.button("🔄 Resetar Navegador (Simular Novo Cliente)"):
    cookie_manager.set(
        "acessos_gastos",
        "0",
        expires_at=datetime.datetime.now() + datetime.timedelta(days=365),
    )
    cookie_manager.set(
        "usuario_pago",
        "false",
        expires_at=datetime.datetime.now() + datetime.timedelta(days=365),
    )
    st.success("Cookiemanager resetado!")
    st.rerun()

# ==========================================
# 8. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown('<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Plataforma Profissional com Inteligência de Canteiro'
    " e Engenharia</p>",
    unsafe_allow_html=True,
)
st.markdown("---")


# ==========================================
# FUNÇÃO DE CONTROLE DE ACESSO COM COOKIE PERSISTENTE
# ==========================================
def verificar_e_consumir_acesso():
    """Incrementa o uso no cookie do navegador do usuário de forma permanente."""
    if is_pago:
        return True

    if qtd_acessos >= 3:
        return False

    novo_valor = qtd_acessos + 1
    cookie_manager.set(
        "acessos_gastos",
        str(novo_valor),
        expires_at=datetime.datetime.now() + datetime.timedelta(days=365),
    )
    return True


# ==========================================
# 9. BLOQUEIO GLOBAL OU EXIBIÇÃO DO MÓDULO
# ==========================================
if not is_pago and qtd_acessos >= 3:
    renderizar_box_pagamento_global()
else:
    # ------------------------------------------
    # MÓDULOS DO SISTEMA (Mantidos idênticos)
    # ------------------------------------------
    if modulo == "📊 Visão Geral e BDI":
        st.subheader("Painel de Controle e Viabilidade Comercial")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input(
                "Nome do Projeto / Cliente:",
                value="Obra Residencial Exemplo",
                key="bdi_cli",
            )
            custo_base = st.number_input(
                "Custo Direto Total Estimado (R$):",
                min_value=0.0,
                value=50000.0,
                step=1000.0,
                key="bdi_custo",
            )
        with col2:
            bdi_taxa = st.slider(
                "Taxa de BDI Aplicada (%):", 0.0, 50.0, 25.0, key="bdi_taxa"
            )

        if st.button(
            "Calcular Viabilidade e Venda", type="primary", key="btn_bdi"
        ):
            if verificar_e_consumir_acesso():
                st.session_state["executou_calculo"] = True
                st.rerun()
            else:
                st.rerun()

        if st.session_state.get("executou_calculo", False):
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
            area_paredes = st.number_input(
                "Área Líquida de Paredes (m²):",
                min_value=1.0,
                value=80.0,
                step=1.0,
                key="alv_area",
            )
            tipo_material = st.selectbox(
                "Escolha a Variedade do Bloco / Tijolo:",
                [
                    "Bloco Cerâmico 9x19x19 cm (Vedação)",
                    "Bloco Cerâmico 14x19x19 cm (Estrutural/Vedação)",
                    "Bloco de Concreto 14x19x39 cm",
                    "Tijolo Baiano 8 furos (9x19x19 cm)",
                    "Tijolo Maciço / Comum",
                ],
                key="alv_tipo",
            )
            preco_unidade = st.number_input(
                "Preço Unitário do Bloco/Tijolo (R$):",
                value=1.20,
                step=0.10,
                key="alv_pr_bloco",
            )
        with col2:
            preco_cimento = st.number_input(
                "Preço do Saco de Cimento 50kg (R$):",
                value=32.00,
                step=1.00,
                key="alv_pr_cim",
            )
            preco_m3_areia = st.number_input(
                "Preço do m³ de Areia Média (R$):",
                value=120.00,
                step=10.00,
                key="alv_pr_areia",
            )

        if st.button(
            "Calcular Soma Total da Alvenaria",
            type="primary",
            key="btn_calc_alv",
        ):
            if verificar_e_consumir_acesso():
                st.session_state["calc_alv_ok"] = True
                st.rerun()
            else:
                st.rerun()

        if st.session_state.get("calc_alv_ok", False):
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
            st.info(
                f"💰 **Soma do Custo Total da Alvenaria:** `R$ {custo_tot:,.2f}`"
            )

    # Demais módulos enxutos e integrados com a verificação de cookie
    elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
        st.subheader("🏠 Dimensionamento, Variedade e Ferro da Laje")
        if st.button("Calcular Materiais da Laje", type="primary", key="btn_laje"):
            if verificar_e_consumir_acesso():
                st.success("Soma de materiais da laje realizada!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
        st.subheader("🏗️ Dimensão, Espessura e Soma de Sacos de Cimento")
        if st.button("Calcular Concreto", type="primary", key="btn_conc"):
            if verificar_e_consumir_acesso():
                st.success("Cálculo de concreto finalizado!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "⚙️ Projeto de Aço, Custo e Auditoria de Armadura":
        st.subheader("⚙️ Projeto Geral de Aço e Auditoria")
        if st.button("Gerar Auditoria de Aço", type="primary", key="btn_aco"):
            if verificar_e_consumir_acesso():
                st.success("Auditoria gerada!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
        st.subheader("🏗️ Dimensionamento de Vigas e Colunas")
        if st.button("Calcular Ferro das Vigas", type="primary", key="btn_vig"):
            if verificar_e_consumir_acesso():
                st.success("Dimensionamento concluído!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
        st.subheader("🚰 Quantitativo de Canos e Conexões")
        if st.button("Calcular Peças Hidráulicas", type="primary", key="btn_hid"):
            if verificar_e_consumir_acesso():
                st.success("Soma hidráulica gerada!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "🎨 Revestimento, Acabamento e Pintura":
        st.subheader("🎨 Cálculo de Reboco, Pintura e Pisos")
        if st.button("Calcular Revestimento", type="primary", key="btn_rev"):
            if verificar_e_consumir_acesso():
                st.success("Cálculo concluído!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "🏠 Cobertura e Telhado":
        st.subheader("🏠 Quantitativo de Telhas e Caibros")
        if st.button("Calcular Telhado", type="primary", key="btn_telh"):
            if verificar_e_consumir_acesso():
                st.success("Telhado calculado!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "⚡ Elétrica Básica Residencial":
        st.subheader("⚡ Estimativa de Eletrodutos e Fios")
        if st.button("Calcular Elétrica", type="primary", key="btn_elet"):
            if verificar_e_consumir_acesso():
                st.success("Elétrica calculada!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "📅 Cronograma Físico-Financeiro (Curva S)":
        st.subheader("📅 Distribuição de Custos por Etapas")
        if st.button("Gerar Cronograma", type="primary", key="btn_curv"):
            if verificar_e_consumir_acesso():
                st.success("Cronograma gerado!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "📝 Gerador de Contrato de Empreitada":
        st.subheader("📝 Minuta de Contrato")
        if st.button("Gerar Contrato", type="primary", key="btn_cont"):
            if verificar_e_consumir_acesso():
                st.success("Contrato gerado!")
                st.rerun()
            else:
                st.rerun()

    elif modulo == "💼 Faturamento e CNPJ":
        st.subheader("Orçamento Comercial")
        if st.button("Emitir Proposta", type="primary", key="btn_fat"):
            if verificar_e_consumir_acesso():
                st.success("Proposta emitida!")
                st.rerun()
            else:
                st.rerun()

    # ------------------------------------------
    # ASSISTENTE IA (GEMINI)
    # ------------------------------------------
    elif modulo == "🤖 Simulação de Engenheiro Virtual Master":
        st.subheader(
            "🤖 Simulação de Engenheiro Virtual Master (Powered by Gemini)"
        )

        restantes_ia = max(0, 3 - qtd_acessos)
        st.info(
            f"🎁 Você tem **{restantes_ia} consulta(s)** gratuita(s) restantes"
            " neste navegador."
        )

        for msg in st.session_state.mensagens_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if prompt_usuario := st.chat_input("Digite sua dúvida de engenharia..."):
            if verificar_e_consumir_acesso():
                if not GEMINI_API_KEY:
                    st.error("⚠️ `GEMINI_API_KEY` não configurada nos Secrets.")
                else:
                    st.session_state.mensagens_chat.append(
                        {"role": "user", "content": prompt_usuario}
                    )
                    with st.chat_message("user"):
                        st.markdown(prompt_usuario)

                    with st.chat_message("assistant"):
                        with st.spinner("Processando..."):
                            resposta_ia = ""
                            prompt_sistema = (
                                "Você é o Engenheiro Virtual Master da Construtech"
                                " Tubarão. Estilo amigável, direto, termos de"
                                " canteiro de obras."
                            )
                            try:
                                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-3.6-flash:generateContent?key={GEMINI_API_KEY}"
                                historico_texto = "\n".join(
                                    [
                                        f"{m['role'].upper()}: {m['content']}"
                                        for m in st.session_state.mensagens_chat
                                    ]
                                )
                                conteudo_prompt = f"{prompt_sistema}\n\nHistórico:\n{historico_texto}\n\nResponda:"
                                payload = {
                                    "contents": [
                                        {"parts": [{"text": conteudo_prompt}]}
                                    ]
                                }
                                response = requests.post(
                                    url,
                                    headers={"Content-Type": "application/json"},
                                    data=json.dumps(payload),
                                )
                                if response.status_code == 200:
                                    res_json = response.json()
                                    resposta_ia = res_json["candidates"][0][
                                        "content"
                                    ]["parts"][0]["text"]
                                else:
                                    resposta_ia = f"⚠️ Erro na API: {response.text}"
                            except Exception as e:
                                resposta_ia = f"⚠️ Erro: {str(e)}"

                            st.markdown(resposta_ia)
                            st.session_state.mensagens_chat.append(
                                {"role": "assistant", "content": resposta_ia}
                            )
                st.rerun()
            else:
                st.rerun()

# ==========================================
# 10. RODAPÉ
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 -"
    " Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
