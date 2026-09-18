# ==========================================
# 7. ASSISTENTE IA INTEGRADO COM O GEMINI (CORRIGIDO DEFINITIVO)
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

                        try:
                            # Utilizando o modelo padrão atual da API do Google de forma direta
                            model = genai.GenerativeModel("gemini-1.5-flash")
                            
                            # Monta o contexto conversacional unindo a persona, o histórico e a nova pergunta
                            historico_texto = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.mensagens_chat])
                            prompt_completo = f"{prompt_sistema}\n\nHistórico da conversa:\n{historico_texto}\n\nResponda à última mensagem do usuário mantendo o personagem."
                            
                            response = model.generate_content(prompt_completo)
                            resposta_ia = response.text
                        except Exception as e:
                            resposta_ia = f"⚠️ Opa, meu irmão! Erro de conexão com a IA: {str(e)}"
                        
                        st.markdown(resposta_ia)
                        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
                
                st.rerun()

    executar_com_controle_amostra("Assistente IA (Engenheiro Virtual Inteligente)", conteudo_ia)
