with st.sidebar.expander("🛠️ Painel do Administrador (Sua Senha)"):
    senha_admin_input = st.text_input("Digite sua chave de liberação:", type="password", key="input_senha_adm")
    if st.button("🔓 Ativar Acesso Mestre"):
        # Aceita a senha independentemente de letras maiúsculas/minúsculas e espaços
        if senha_admin_input.strip().upper() == "CONSTRUTECH12":
            st.session_state.liberado_pago = True
            st.success("Acesso Administrador liberado com sucesso!")
            st.rerun()
        else:
            st.error("Chave incorreta!")

    if st.session_state.liberado_pago:
        st.info("Status atual: **MODO MASTER LIBERADO 🔓**")
