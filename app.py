import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="Construtech Tubarão",
    page_icon="🏗️",
    layout="wide"
)

# Inicialização de variáveis de controle no session_state
if "liberado_pago" not in st.session_state:
    st.session_state.liberado_pago = False

# Função de controle de acesso para módulos pagos/protegidos
def executar_com_controle_amostra(nome_modulo, funcao_conteudo):
    st.markdown(f"## Módulo: {nome_modulo}")
    if st.session_state.liberado_pago:
        funcao_conteudo()
    else:
        st.warning("⚠️ Este é um recurso avançado. Insira a chave de liberação na barra lateral para desbloquear o acesso completo.")
        # Exibe uma versão resumida ou bloqueada
        with st.container():
            st.info("Modo de Demonstração / Amostra Ativo.")
            if st.button(f"Testar versão de demonstração de {nome_modulo}", key=f"btn_demo_{nome_modulo}"):
                funcao_conteudo()

# Menu lateral com Painel do Administrador e Módulos
st.sidebar.title("🏗️ Construtech Tubarão")
st.sidebar.markdown("---")

# Painel do Administrador (Com correção flexível da senha que ajustamos)
with st.sidebar.expander("🛠️ Painel do Administrador (Sua Senha)"):
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

st.sidebar.markdown("---")
modulo = st.sidebar.selectbox(
    "Selecione o Módulo",
    [
        "🏠 Início",
        "🧮 Orçamento de Materiais",
        "📊 Curva S e Cronograma",
        "🤖 Assistente IA (Engenheiro Virtual)"
    ]
)

# ---------------------------------------------------------
# MÓDULO 1: INÍCIO
# ---------------------------------------------------------
if modulo == "🏠 Início":
    st.title("Bem-vindo à Construtech Tubarão 🚀")
    st.markdown("""
    O seu sistema inteligente para gestão, cálculo de materiais e controle de obras na palma da mão. 
    Utilize o menu lateral para navegar entre os módulos ou acessar o painel de liberação.
    """)
    st.image("https://images.unsplash.com/photo-1541888946425-d0fbb18f4357?q=80&w=1200&auto=format&fit=crop", use_container_width=True)

# ---------------------------------------------------------
# MÓDULO 2: ORÇAMENTO DE MATERIAIS
# ---------------------------------------------------------
elif modulo == "🧮 Orçamento de Materiais":
    def conteudo_orcamento():
        st.subheader("Calculadora de Insumos para Canteiro de Obras")
        col1, col2 = st.columns(2)
        with col1:
            area = st.number_input("Área da Construção (m²)", min_value=1.0, value=50.0)
        with col2:
            tipo_obra = st.selectbox("Padrão da Obra", ["Popular", "Médio", "Alto Padrão"])
        
        if st.button("Calcular Insumos"):
            cimento = area * 3.5  # Exemplo de cálculo básico
            areia = area * 0.25
            st.success(f"Estimativa para {area}m² ({tipo_obra}):")
            st.metric("Sacos de Cimento (50kg)", f"{cimento:.1f} sc")
            st.metric("Areia Média (m³)", f"{areia:.2f} m³")

    executar_com_controle_amostra("Orçamento de Materiais", conteudo_orcamento)

# ---------------------------------------------------------
# MÓDULO 3: CURVA S E CRONOGRAMA
# ---------------------------------------------------------
elif modulo == "📊 Curva S e Cronograma":
    def conteudo_curva_s():
        st.subheader("Planejamento Físico-Financeiro (Curva S)")
        st.markdown("Acompanhe o avanço planejado versus o realizado da sua obra ao longo dos meses.")
        # Simulação de dados visuais
        dados_exemplo = [10, 25, 45, 70, 90, 100]
        st.line_chart(dados_exemplo)

    executar_com_controle_amostra("Curva S e Cronograma", conteudo_curva_s)

# ---------------------------------------------------------
# MÓDULO 4: ASSISTENTE IA (NOVO!)
# ---------------------------------------------------------
elif modulo == "🤖 Assistente IA (Engenheiro Virtual)":
    def conteudo_ia():
        st.subheader("🤖 Assistente Virtual - Construtech Tubarão")
        st.markdown("Tire dúvidas sobre traços de concreto, normas técnicas, etapas de obra ou otimização de custos diretamente com nossa inteligência artificial.")

        # Inicializa o histórico de mensagens do chat na sessão
        if "mensagens_chat" not in st.session_state:
            st.session_state.mensagens_chat = [
                {"role": "assistant", "content": "Olá, meu irmão! Sou o engenheiro virtual da Construtech Tubarão. Qual é a dúvida sobre a obra de hoje?"}
            ]

        # Exibe o histórico de mensagens na tela
        for msg in st.session_state.mensagens_chat:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # Entrada de texto do usuário (Chat interativo)
        if prompt_usuario := st.chat_input("Digite sua dúvida sobre construção, materiais ou orçamento..."):
            # Adiciona a mensagem do usuário ao histórico
            st.session_state.mensagens_chat.append({"role": "user", "content": prompt_usuario})
            with st.chat_message("user"):
                st.markdown(prompt_usuario)

            # Resposta da IA
            with st.chat_message("assistant"):
                with st.spinner("Analisando os parâmetros da obra..."):
                    # Aqui você pode plugar a chamada real da API do Gemini se desejar conectar o backend puro de IA.
                    # Exemplo de resposta inteligente simulada com base no contexto:
                    resposta_ia = f"Analisando sua solicitação sobre **'{prompt_usuario}'**: para garantir a segurança estrutural e evitar desperdícios no canteiro, recomendo seguir rigorosamente o traço recomendado no módulo de insumos e consultar as diretrizes da ABNT pertinentes."
                    
                    st.markdown(resposta_ia)
                    st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})

    executar_com_controle_amostra("Assistente IA (Engenheiro Virtual)", conteudo_ia)
