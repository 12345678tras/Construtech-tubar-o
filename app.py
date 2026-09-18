elif modulo == "🤖 Assistente IA (Engenheiro Virtual Inteligente)":
    def conteudo_ia():
        st.subheader("🤖 Engenheiro Virtual Inteligente (Powered by Gemini) - Construtech Tubarão")
        
        api_key = ""
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
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
            # [Mantém a caixa de pagamento igual já estava]
            pass
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
                            "(como 'fala, meu irmão', 'na lata'). Especialista em construção civil brasileira."
                        )

                        try:
                            # Mudança crítica: Usando o modelo 'gemini-pro' na versão 'v1' que é amplamente compatível
                            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={api_key}"
                            
                            historico_texto = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in st.session_state.mensagens_chat])
                            conteudo_prompt = f"{prompt_sistema}\n\nHistórico:\n{historico_texto}\n\nResponda à última mensagem:"
                            
                            payload = {
                                "contents": [{
                                    "parts": [{"text": conteudo_prompt}]
                                }]
                            }
                            headers = {'Content-Type': 'application/json'}
                            
                            response = requests.post(url, headers=headers, data=json.dumps(payload))
                            
                            if response.status_code == 200:
                                res_json = response.json()
                                resposta_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                            else:
                                resposta_ia = f"⚠️ Opa, meu irmão! Erro na API (Código {response.status_code}): {response.text}"
                                
                        except Exception as e:
                            resposta_ia = f"⚠️ Opa, meu irmão! Erro de conexão com a IA: {str(e)}"
                        
                        st.markdown(resposta_ia)
                        st.session_state.mensagens_chat.append({"role": "assistant", "content": resposta_ia})
                
                st.rerun()

    executar_com_controle_amostra("Assistente IA (Engenheiro Virtual Inteligente)", conteudo_ia)
