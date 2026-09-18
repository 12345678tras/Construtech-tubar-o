import streamlit as datetime
import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma de Engenharia e IA",
    page_icon="🏗️",
    layout="wide",
)

# ==========================================
# 2. CONTROLE DE TEMA (MODO ESCURO / CLARO)
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
# 3. GERENCIAMENTO DE ESTADO (SESSION STATE)
# ==========================================
if "liberado_pago" not in st.session_state:
    st.session_state.liberado_pago = False

if "uso_modulos" not in st.session_state:
    st.session_state.uso_modulos = {}

if "historico_comprovantes" not in st.session_state:
    st.session_state.historico_comprovantes = []

if "contador_ia_gratis" not in st.session_state:
    st.session_state.contador_ia_gratis = 0

if "mensagens_chat" not in st.session_state:
    st.session_state.mensagens_chat = [
        {
            "role": "assistant",
            "content": (
                "Fala, meu irmão! Sou o engenheiro virtual da Construtech Tubarão. "
                "Você tem **4 consultas gratuitas** para testar. "
                "Pode mandar sua dúvida do seu jeito, que eu te ajudo na obra!"
            ),
        }
    ]

# ==========================================
# 4. MENU LATERAL E PAINEL ADMINISTRADOR
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
    "🤖 Assistente IA (Engenheiro Virtual Inteligente)",
]

modulo = st.sidebar.selectbox("Selecione a Ferramenta:", lista_modulos)

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Painel do Administrador"):
    senha_admin_input = st.text_input("Digite sua chave de liberação:", type="password", key="input_senha_adm")
    if st.button("🔓 Ativar Acesso Mestre"):
        senha_tratada = senha_admin_input.strip().upper()
        if senha_tratada in ["CONSTRUTECH12", "CONSTRUTECH", "CONTRUTECH12", "CONTRUTECH"]:
            st.session_state.liberado_pago = True
            st.success("Acesso Administrador liberado com sucesso!")
            st.rerun()
        else:
            st.error("Chave incorreta!")

    if st.session_state.liberado_pago:
        st.info("Status atual: **MODO MASTER LIBERADO 🔓**")

if st.sidebar.button("🔄 Resetar Sessão (Simular Novo Cliente)"):
    st.session_state.uso_modulos = {}
    st.session_state.contador_ia_gratis = 0
    st.session_state.liberado_pago = False
    st.rerun()

# ==========================================
# 5. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown('<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Plataforma Profissional com Inteligência de Canteiro e Engenharia</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ==========================================
# FUNÇÃO DE BLOQUEIO DE MÓDULOS APÓS AMOSTRA
# ==========================================
def executar_com_controle_amostra(nome_modulo, funcao_conteudo):
    if nome_modulo not in st.session_state.uso_modulos:
        st.session_state.uso_modulos[nome_modulo] = "livre"

    status_atual = st.session_state.uso_modulos[nome_modulo]

    if status_atual == "bloqueado" and not st.session_state.liberado_pago:
        st.markdown(f'<p class="main-header">🔒 Amostra Grátis Utilizada: {nome_modulo}</p>', unsafe_allow_html=True)
        st.info("💡 Você já utilizou sua consulta gratuita neste módulo. Para continuar acessando, realize o pagamento de **R$ 20,00** para **CAC CONTABILIZANDO** ou insira sua chave de acesso mestre ao lado.")

        st.markdown('<div class="box-pagamento">', unsafe_allow_html=True)
        col_pag1, col_pag2 = st.columns(2, gap="large")

        with col_pag1:
            st.markdown("### 1️⃣ Forma de Pagamento (Pix / Cartão)")
            st.markdown(
                '<a href="https://link.infinitepay.io/cristiane-da-260/VC1DLTAtUg-HgBiSH5iQO-20,00" target="_blank" class="btn-pagar">💳 PAGAR COM CARTÃO / LINK</a>',
                unsafe_allow_html=True
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
                unsafe_allow_html=True
            )

        with col_pag2:
            st.markdown("### 2️⃣ Liberar com Comprovante")
            comprovante_texto = st.text_area(
                "Comprovante de Pagamento:", 
                key=f"comp_{nome_modulo}", 
                placeholder="Cole o ID do Pix ou dados da transferência...",
                height=120
            )
            
            if st.button("✨ Validar e Liberar Acesso", key=f"btn_gerar_{nome_modulo}", type="primary", use_container_width=True):
                import datetime as dt_lib
                if comprovante_texto.strip() != "":
                    data_atual = dt_lib.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    st.session_state.historico_comprovantes.append({
                        "modulo": nome_modulo,
                        "comprovante": comprovante_texto.strip(),
                        "data": data_atual
                    })
                    st.session_state.liberado_pago = True
                    st.success("Acesso liberado com sucesso!")
                    st.rerun()
                else:
                    st.warning("⚠️ Insira o comprovante de pagamento.")

        st.markdown('</div>', unsafe_allow_html=True)
        return

    funcao_conteudo()

# ==========================================
# 6. MÓDULOS DO SISTEMA (EXEMPLOS INICIAIS)
# ==========================================
if modulo == "📊 Visão Geral e BDI":
    def conteudo():
        st.subheader("Painel de Controle e Viabilidade Comercial")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Nome do Projeto / Cliente:", value="Obra Residencial Exemplo", key="bdi_cli")
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
            st.session_state.uso_modulos[modulo] = "bloqueado"
    executar_com_controle_amostra(modulo, conteudo)

# (Demais módulos mantêm suas estruturas normais...)

# ==========================================
# 7. ASSISTENTE IA INTEGRADO COM O GEMINI
# ==========================================
elif modulo == "🤖 Assistente IA (Engenheiro Virtual Inteligente)":
    def conteudo_ia():
        st.subheader("🤖 Engenheiro Virtual Inteligente (Powered by Gemini) - Construtech Tubarão")
        
        # Configuração da Chave do Gemini usando as Secrets do Streamlit
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
            genai.configure(api_key=api_key)
        except Exception:
            pass

        consultas_restantes = max(0, 4 - st.session_state.contador_ia_gratis)
        if not st.session_state.liberado_pago:
            if consultas_restantes > 0:
                st.info(f"🎁 Você tem **{consultas_restantes} consulta(s) gratuita(s)** restantes com o Engenheiro Virtual.")
            else:
                st.warning("⚠️ Suas 4 consultas gratuitas da IA acabaram. Realize o pagamento abaixo para liberar o acesso ilimitado.")

        for msg in st.session_state.mensagens_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        if st.session_state.contador_ia_gratis >= 4 and not st.session_state.liberado_pago:
            st.markdown("---")
            st.markdown("### 🔒 Desbloqueie o Assistente IA Ilimitado")
            st.markdown('<div class="box-pagamento">', unsafe_allow_html=True)
            col_pag1, col_pag2 = st.columns(2, gap="large")

            with col_pag1:
                st.markdown("### 1️⃣ Forma de Pagamento (Pix / Cartão)")
                st.markdown(
                    '<a href="https://link.infinitepay.io/cristiane-da-260/VC1DLTAtUg-HgBiSH5iQO-20,00" target="_blank" class="btn-pagar">💳 PAGAR COM CARTÃO / LINK</a>',
                    unsafe_allow_html=True
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
                    unsafe_allow_html=True
                )

            with col_pag2:
                st.markdown("### 2️⃣ Liberar com Comprovante")
                comprovante_texto = st.text_area(
                    "Comprovante de Pagamento:", 
                    key="comp_ia_chat", 
                    placeholder="Cole o ID do Pix ou dados da transferência...",
                    height=120
                )
                
                if st.button("✨ Validar e Liberar Acesso da IA", key="btn_gerar_ia_chat", type="primary", use_container_width=True):
                    import datetime as dt_lib
                    if comprovante_texto.strip() != "":
                        data_atual = dt_lib.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        st.session_state.historico_comprovantes.append({
                            "modulo": "Assistente IA Completo",
                            "comprovante": comprovante_texto.strip(),
                            "data": data_atual
                        })
                        st.session_state.liberado_pago = True
                        st.success("Acesso liberado com sucesso!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Insira o comprovante de pagamento.")

            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            if prompt_usuario := st.chat_input("Ex: 'Quantos blocos gastam no muro?' ou 'Qual o traço de concreto ideal?'"):
                if not st.session_state.liberado_pago:
                    st.session_state.contador_ia_gratis += 1

                st.session_state.mensagens_chat.append({"role": "user", "content": prompt_usuario})
                with st.chat_message("user"):
                    st.markdown(prompt_usuario)

                with st.chat_message("assistant"):
                    with st.spinner("O Engenheiro Virtual está calculando os parâmetros da obra..."):
                        resposta_ia = ""
                        
                        prompt_sistema = (
                            "Você é o Engenheiro Virtual Inteligente da plataforma 'Construtech Tubarão'. "
                            "Seu estilo de comunicação é amigável, direto, usando expressões de canteiro de obras "
                            "(como 'fala, meu irmão', 'na lata', 'comprar margem de segurança'). "
                            "Você é especialista em construção civil brasileira (alvenaria, blocos, cimento, lajes, "
                            "concreto, traços, hidráulica, elétrica e orçamento). Responda com dados práticos, "
                            "cálculos rápidos e orientações técnicas precisas."
                        )

                        # Modelos seguros testados com a biblioteca atualizada do SDK
                        modelos_para_tentar = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
                        
                        sucesso = False
                        last_error = ""
                        for nome_modelo in modelos_para_tentar:
                            try:
                                model = genai.GenerativeModel(
                                    model_name=nome_modelo,
                                    system_instruction=prompt_sistema
                                )
                                
                                historico_formatado = []
                                for m in st.session_state.mensagens_chat[:-1]:
                                    role_gemini = "user" if m["role"] == "user" else "model"
                                    historico_formatado.append({"role": role_gemini, "parts": [m["content"]]})

                                chat = model.start_chat(history=historico_formatado)
                                response = chat.send_message(prompt_usuario)
                                resposta_ia = response.text
                                sucesso = True
                                break
                            except Exception as e:
                                last_error = str(e)
                                continue
                        
                        # Fallback por segurança caso o system_instruction rejeite
                        if not sucesso:
                            for nome_modelo in modelos_para_tentar:
                                try:
                                    model = genai.GenerativeModel(nome_modelo)
                                    prompt_completo = f"{prompt_sistema}\n\nDúvida do usuário: {prompt_usuario}"
                                    response = model.generate_content(prompt_completo)
                                    resposta_ia = response.text
                                    sucesso = True
                                    break
                                except Exception as e:
                                    last_error = str(e)
                                    continue

                        if not sucesso:
                            resposta_ia = f"⚠️ Opa, meu irmão! Houve um problema na conexão com o motor da IA. Erro retornado: {last_error}"
                        
                        st.markdown(resposta_ia)
                        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
                
                st.rerun()

    executar_com_controle_amostra("Assistente IA (Engenheiro Virtual Inteligente)", conteudo_ia)

# ==========================================
# 8. RODAPÉ DA APLICAÇÃO
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
