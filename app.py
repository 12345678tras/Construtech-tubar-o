import streamlit as st
import datetime

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="Construtech Tubarão - Plataforma de Engenharia",
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

# Controle de sessão e base de dados
if "liberado_pago" not in st.session_state:
    st.session_state.liberado_pago = False

if "uso_modulos" not in st.session_state:
    st.session_state.uso_modulos = {}

if "historico_comprovantes" not in st.session_state:
    st.session_state.historico_comprovantes = []

# ==========================================
# 3. MENU LATERAL E PAINEL DO ADMINISTRADOR
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
]

modulo = st.sidebar.selectbox("Selecione a Ferramenta:", lista_modulos)

st.sidebar.markdown("---")
with st.sidebar.expander("🛠️ Painel do Administrador (Sua Senha)"):
    senha_admin_input = st.text_input("Digite sua chave de liberação:", type="password", key="input_senha_adm")
    if st.button("🔓 Ativar Acesso Mestre"):
        # Aceita a senha independentemente de letras maiúsculas/minúsculas e espaços (ex: "construtech12" ou "CONSTRUTECH12")
        if senha_admin_input.strip().upper() in ["CONSTRUTECH12", "CONSTRUTECH"]:
            st.session_state.liberado_pago = True
            st.success("Acesso Administrador liberado com sucesso!")
            st.rerun()
        else:
            st.error("Chave incorreta!")

    if st.session_state.liberado_pago:
        st.info("Status atual: **MODO MASTER LIBERADO 🔓**")

if st.sidebar.button("🔄 Resetar Sessão (Simular Novo Cliente)"):
    st.session_state.uso_modulos = {}
    st.session_state.liberado_pago = False
    st.rerun()

# ==========================================
# 4. CABEÇALHO DA APLICAÇÃO
# ==========================================
st.markdown(
    '<p class="main-header">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Plataforma Profissional com Inteligência de Canteiro e Engenharia</p>',
    unsafe_allow_html=True,
)
st.markdown("---")

# ==========================================
# FUNÇÃO DE CONTROLE DE AMOSTRA E PAGAMENTO
# ==========================================
def executar_com_controle_amostra(nome_modulo, funcao_conteudo):
    if nome_modulo not in st.session_state.uso_modulos:
        st.session_state.uso_modulos[nome_modulo] = "livre"

    status_atual = st.session_state.uso_modulos[nome_modulo]

    if status_atual == "bloqueado" and not st.session_state.liberado_pago:
        st.markdown(f'<p class="main-header">🔒 Amostra Grátis Utilizada: {nome_modulo}</p>', unsafe_allow_html=True)
        st.info("💡 Você já utilizou sua consulta gratuita neste módulo. Para continuar acessando e desbloquear o uso completo, realize o pagamento de **R$ 20,00** para **CAC CONTABILIZANDO**[span_0](start_span)[span_0](end_span) ou insira sua chave de acesso mestre no painel ao lado.")

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
                    <code style="font-size: 16px; background: rgba(0,0,0,0.1); padding: 3px 8px; border-radius: 4px; font-weight: bold;">+5564993044147</code>[span_1](start_span)[span_1](end_span)
                    <p style="margin: 5px 0 0 0; font-size: 12px;">Favorecido: <b>CAC CONTABILIZANDO</b></p>[span_2](start_span)[span_2](end_span)
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_pag2:
            st.markdown("### 2️⃣ Liberar com Comprovante")
            st.markdown("Cole o comprovante de pagamento abaixo:")
            
            comprovante_texto = st.text_area(
                "Comprovante de Pagamento:", 
                key=f"comp_{nome_modulo}", 
                placeholder="Cole o ID do Pix ou dados da transferência...",
                height=120
            )
            
            if st.button("✨ Validar e Liberar Acesso", key=f"btn_gerar_{nome_modulo}", type="primary", use_container_width=True):
                if comprovante_texto.strip() != "":
                    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
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
# 5. MÓDULOS DA APLICAÇÃO
# ==========================================

if modulo == "📊 Visão Geral e BDI":
    def conteudo():
        st.subheader("Painel de Controle e Viabilidade Comercial")
        col1, col2 = st.columns(2)
        with col1:
            cliente = st.text_input("Nome do Projeto / Cliente:", value="Obra Residencial Exemplo", key="bdi_cli")
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
            
            relatorio_texto = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE BDI ===
Projeto/Cliente: {cliente}
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Custo Direto Total: R$ {custo_base:,.2f}
Taxa de BDI Aplicada: {bdi_taxa}%
Preço Final de Venda: R$ {preco_venda:,.2f}
Lucro Bruto Estimado: R$ {lucro_estimado:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório do Cálculo (TXT)",
                data=relatorio_texto,
                file_name=f"Relatorio_BDI_{cliente.replace(' ', '_')}.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🧱 Alvenaria Completa (Blocos, Cimento e Areia)":
    def conteudo():
        st.subheader("🧱 Dimensionamento e Soma de Insumos de Alvenaria")
        col1, col2 = st.columns(2)
        with col1:
            area_paredes = st.number_input("Área Líquida de Paredes (m²):", min_value=1.0, value=80.0, step=1.0, key="alv_area")
            tipo_material = st.selectbox(
                "Escolha a Variedade do Bloco / Tijolo:", 
                [
                    "Bloco Cerâmico 9x19x19 cm (Vedação)", 
                    "Bloco Cerâmico 14x19x19 cm (Estrutural/Vedação)", 
                    "Bloco de Concreto 14x19x39 cm", 
                    "Tijolo Baiano 8 furos (9x19x19 cm)", 
                    "Tijolo Maciço / Comum"
                ],
                key="alv_tipo"
            )
            preco_unidade = st.number_input("Preço Unitário do Bloco/Tijolo (R$):", value=1.20, step=0.10, key="alv_pr_bloco")
        with col2:
            preco_cimento = st.number_input("Preço do Saco de Cimento 50kg (R$):", value=32.00, step=1.00, key="alv_pr_cim")
            preco_m3_areia = st.number_input("Preço do m³ de Areia Média (R$):", value=120.00, step=10.00, key="alv_pr_areia")

        if st.button("Calcular Soma Total da Alvenaria", type="primary", key="btn_calc_alv"):
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
            st.info(f"💰 **Soma do Custo Total da Alvenaria:** `R$ {custo_tot:,.2f}`")

            relatorio_alv = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE ALVENARIA ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Área de Paredes: {area_paredes} m²
Custo Total Estimado: R$ {custo_tot:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Alvenaria (TXT)",
                data=relatorio_alv,
                file_name="Relatorio_Alvenaria.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏠 Lajes Avançadas (Cerâmica e Isopor/EPS)":
    def conteudo():
        st.subheader("🏠 Dimensionamento, Variedade e Ferro da Laje")
        col1, col2 = st.columns(2)
        with col1:
            area_laje = st.number_input("Área Total da Laje (m²):", min_value=1.0, value=50.0, step=1.0, key="laje_area")
            tipo_enchimento = st.selectbox(
                "Variedade de Enchimento da Laje:",
                ["Lajota Cerâmica Tradicional", "Bloco de Isopor (EPS - Alta Densidade)", "Lajota Concreto / Paulistinha"],
                key="laje_enchimento"
            )
        with col2:
            altura_laje = st.selectbox(
                "Altura da Laje (Vigota + Capa):",
                ["H8 (11 cm total)", "H12 (16 cm total)", "H16 (20 cm total)", "H20 (25 cm total)"],
                key="laje_altura"
            )

        if st.button("Calcular Materiais e Ferro da Laje", type="primary", key="btn_calc_laje"):
            ml_vigotas = area_laje * 1.35
            qtd_blocos = area_laje * 8.3 if "Cerâmica" in tipo_enchimento else area_laje * 2.5
            vol_concreto_m3 = area_laje * 0.070 * 1.07
            sacos_cimento_laje = vol_concreto_m3 * 6.5 

            st.success("Soma de materiais da laje realizada!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} m")
            c2.metric("Blocos / Lajotas", f"{int(qtd_blocos)} un")
            c3.metric("Concreto (Capa)", f"{vol_concreto_m3:.2f} m³")

            relatorio_laje = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE LAJES ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Área da Laje: {area_laje} m²
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Laje (TXT)",
                data=relatorio_laje,
                file_name="Relatorio_Laje.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏗️ Concreto, Traços e Volume Estrutural":
    def conteudo():
        st.subheader("🏗️ Dimensão, Espessura e Soma de Sacos de Cimento (Traço)")
        col1, col2 = st.columns(2)
        with col1:
            area_concreto = st.number_input("Metragem da Área / Piso (m²):", min_value=1.0, value=50.0, key="conc_area")
            espessura_cm = st.number_input("Espessura da Camada/Laje (cm):", min_value=1.0, value=7.0, key="conc_esp")
        with col2:
            traco_tipo = st.selectbox(
                "Variedade do Traço de Concreto:",
                ["Traço 1:2:3 (Fck 25 MPa)", "Traço 1:2.5:3.5 (Fck 20 MPa)", "Traço 1:3:5 (Contrapiso)"],
                key="conc_traco"
            )

        if st.button("Calcular Volume e Quantidade de Sacos", type="primary", key="btn_calc_conc"):
            volume_real = (area_concreto * (espessura_cm / 100.0)) * 1.07 
            sc_cif = volume_real * 7.5
            areia_m3 = volume_real * 0.55
            brita_m3 = volume_real * 0.75

            st.success("Cálculo de concreto finalizado!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Volume Total com Perda", f"{volume_real:.2f} m³")
            c2.metric("Sacos de Cimento", f"{sc_cif:.1f} sacos")
            c3.metric("Areia / Brita", f"{areia_m3:.2f} m³ / {brita_m3:.2f} m³")

            relatorio_conc = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE CONCRETO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Volume Total: {volume_real:.2f} m³
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Concreto (TXT)",
                data=relatorio_conc,
                file_name="Relatorio_Concreto.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "⚙️ Projeto de Aço, Custo e Auditoria de Armadura":
    def conteudo():
        st.subheader("⚙️ Projeto Geral de Aço e Auditoria")
        area_obra = st.number_input("Área Construída Total (m²):", min_value=10.0, value=120.0, key="aco_geral_area")
        preco_aco_kg = st.number_input("Preço Médio do Aço por kg (R$):", value=11.50, key="aco_geral_pr")
        if st.button("Gerar Auditoria de Aço", type="primary", key="btn_calc_aco_geral"):
            peso_tot = area_obra * 14.0 
            custo_tot_aco = peso_tot * preco_aco_kg
            st.success("Auditoria gerada!")
            c1, c2 = st.columns(2)
            c1.metric("Peso Estimado de Aço", f"{peso_tot:.1f} kg")
            c2.metric("Custo Total do Aço", f"R$ {custo_tot_aco:,.2f}")

            relatorio_aco = f"""=== CONSTRUTECH TUBARÃO - AUDITORIA DE AÇO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Custo Total: R$ {custo_tot_aco:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Aço (TXT)",
                data=relatorio_aco,
                file_name="Relatorio_Aco.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏗️ Estrutural, Vigas, Bitolas e Aços":
    def conteudo():
        st.subheader("🏗️ Dimensionamento de Vigas, Colunas e Bitolas de Ferro")
        col1, col2 = st.columns(2)
        with col1:
            vao_viga = st.number_input("Vão Livre da Viga ou Coluna (metros):", min_value=1.0, value=4.0, key="viga_vao")
            qtd_pecas = st.number_input("Quantidade de Vigas/Colunas iguais:", min_value=1, value=4, key="viga_qtd")
        with col2:
            tipo_bitola_principal = st.selectbox(
                "Bitola do Ferro Principal:",
                ["Ferro 3/8'' (10.0 mm)", "Ferro 5/16'' (8.0 mm)", "Ferro 1/2'' (12.5 mm)"],
                key="viga_bitola"
            )

        if st.button("Calcular Quantidade de Ferro das Vigas", type="primary", key="btn_calc_vigas"):
            kg_por_viga = vao_viga * 8.5 * qtd_pecas
            estribos_un = int((vao_viga / 0.12) * qtd_pecas)
            
            st.success("Dimensionamento de vigas concluído!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Ferro Principal", tipo_bitola_principal)
            c2.metric("Peso Total", f"{kg_por_viga:.1f} kg")
            c3.metric("Estribos", f"{estribos_un} un")
            
            relatorio_vigas = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO ESTRUTURAL ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Peso Total: {kg_por_viga:.1f} kg
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório Estrutural (TXT)",
                data=relatorio_vigas,
                file_name="Relatorio_Estrutural.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🚰 Sistema Hidráulico Prático (Banheiro e Cozinha)":
    def conteudo():
        st.subheader("🚰 Quantitativo de Canos, Conexões e Fossa para Banheiro e Cozinha")
        col1, col2 = st.columns(2)
        with col1:
            qtd_banheiros = st.number_input("Número de Banheiros Completos:", min_value=1, value=1, step=1, key="hid_banh")
            qtd_cozinhas = st.number_input("Número de Cozinhas:", min_value=1, value=1, step=1, key="hid_coz")
        with col2:
            distancia_fossa = st.number_input("Distância até a Fossa (metros):", min_value=2.0, value=10.0, step=1.0, key="hid_dist")

        if st.button("Calcular Soma de Peças Hidráulicas", type="primary", key="btn_calc_hid"):
            cano_esgoto_100 = (qtd_banheiros * 6.0) + distancia_fossa
            cano_agua_25 = (qtd_banheiros * 8.0) + (qtd_cozinhas * 6.0)

            st.success("Soma hidráulica gerada com sucesso!")
            st.write(f"- Tubo Esgoto 100mm: **{cano_esgoto_100:.1f} metros**")
            st.write(f"- Tubo Água Fria 25mm: **{cano_agua_25:.1f} metros**")

            relatorio_hid = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO HIDRÁULICO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Tubo Esgoto 100mm: {cano_esgoto_100:.1f} m
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório Hidráulico (TXT)",
                data=relatorio_hid,
                file_name="Relatorio_Hidraulico.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🎨 Revestimento, Acabamento e Pintura":
    def conteudo():
        st.subheader("🎨 Cálculo de Reboco, Pintura e Pisos/Porcelanatos")
        col1, col2 = st.columns(2)
        with col1:
            area_rev = st.number_input("Área de Paredes para Reboco/Pintura (m²):", min_value=1.0, value=100.0, key="rev_parede")
            demãos_tinta = st.slider("Número de Demãos de Tinta:", 1, 4, 2, key="rev_demaos")
        with col2:
            area_piso = st.number_input("Área de Piso para Revestimento (m²):", min_value=1.0, value=60.0, key="rev_piso")
            taxa_perda_piso = st.slider("Taxa de Perda de Recorte de Piso (%):", 5, 20, 10, key="rev_perda")

        if st.button("Calcular Revestimento e Acabamento", type="primary", key="btn_calc_rev"):
            sacos_arg_reboco = (area_rev * 0.025) * 18 # base 2.5cm espessura
            litros_tinta = (area_rev * demãos_tinta) / 10 # rendimento médio 10m²/litro por demão
            piso_com_perda = area_piso * (1 + taxa_perda_piso / 100.0)

            st.success("Cálculo de acabamento concluído!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Argamassa Reboco", f"{sacos_arg_reboco:.1f} sc (20kg)")
            c2.metric("Tinta Estimada", f"{litros_tinta:.1f} litros")
            c3.metric("Piso c/ Recorte", f"{piso_com_perda:.1f} m²")

            relatorio_rev = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE ACABAMENTO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Área Reboco/Pintura: {area_rev} m² | Litros Tinta: {litros_tinta:.1f} L
Área Piso c/ Recorte ({taxa_perda_piso}%): {piso_com_perda:.1f} m²
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Acabamento (TXT)",
                data=relatorio_rev,
                file_name="Relatorio_Acabamento.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "🏠 Cobertura e Telhado":
    def conteudo():
        st.subheader("🏠 Quantitativo de Telhas, Caibros e Ripas")
        col1, col2 = st.columns(2)
        with col1:
            proj_chao = st.number_input("Área de Projeção em Planta do Telhado (m²):", min_value=1.0, value=80.0, key="telh_proj")
            tipo_telha = st.selectbox("Modelo de Telha:", ["Telha Colonial / Cerâmica", "Telha de Fibrocimento", "Telha Metálica / Sanduíche"], key="telh_tipo")
        with col2:
            inclinacao = st.slider("Inclinação Estimada (%):", 10, 45, 30, key="telh_inc")

        if st.button("Calcular Estrutura do Telhado", type="primary", key="btn_calc_telh"):
            area_real = proj_chao * (1 + (inclinacao / 100.0) * 0.3)
            if "Colonial" in tipo_telha:
                qtd_telhas = area_real * 16
            elif "Fibrocimento" in tipo_telha:
                qtd_telhas = area_real * 0.55
            else:
                qtd_telhas = area_real * 1.1

            ml_caibros = area_real * 3.5
            ml_ripas = area_real * 7.0

            st.success("Dimensionamento de telhado finalizado!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Área Real do Telhado", f"{area_real:.1f} m²")
            c2.metric("Quantidade de Telhas", f"{int(qtd_telhas)} un")
            c3.metric("Madeiramento (Caibros/Ripas)", f"{ml_caibros:.0f}m / {ml_ripas:.0f}m")

            relatorio_telh = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE TELHADO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Área Real: {area_real:.1f} m² | Telhas: {int(qtd_telhas)} un
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Telhado (TXT)",
                data=relatorio_telh,
                file_name="Relatorio_Telhado.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "⚡ Elétrica Básica Residencial":
    def conteudo():
        st.subheader("⚡ Estimativa de Eletrodutos, Caixas e Fios")
        col1, col2 = st.columns(2)
        with col1:
            area_casa = st.number_input("Área Construída para Elétrica (m²):", min_value=10.0, value=90.0, key="el_area")
            qtd_comodos = st.number_input("Número de Cômodos / Quartos / Salas:", min_value=1, value=6, key="el_com")
        with col2:
            st.write("Parâmetros automáticos baseados na NBR 5410 para residências.")

        if st.button("Calcular Insumos Elétricos", type="primary", key="btn_calc_eletrica"):
            m_conduite = area_casa * 2.2
            caixas_4x2 = qtd_comodos * 5
            caixas_4x4 = qtd_comodos * 1
            m_fio_25 = area_casa * 4.5 # tomadas/iluminação
            m_fio_40 = area_casa * 1.5 # chuveiro/fornos

            st.success("Orçamento elétrico calculado com sucesso!")
            c1, c2 = st.columns(2)
            c1.metric("Eletrodutos Corrugados", f"{m_conduite:.1f} metros")
            c2.metric("Caixas 4x2 / 4x4", f"{caixas_4x2} / {caixas_4x4} un")
            st.write(f"- Metragem Fio 2,5mm² (Geral): **{m_fio_25:.1f} m**")
            st.write(f"- Metragem Fio 4,0mm² (Potência): **{m_fio_40:.1f} m**")

            relatorio_el = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO ELÉTRICO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Eletrodutos: {m_conduite:.1f} m | Caixas 4x2: {caixas_4x2} un
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório Elétrico (TXT)",
                data=relatorio_el,
                file_name="Relatorio_Eletrico.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "📅 Cronograma Físico-Financeiro (Curva S)":
    def conteudo():
        st.subheader("📅 Distribuição de Custos por Etapas da Obra")
        custo_total_obra = st.number_input("Custo Total Estimado da Obra (R$):", value=150000.0, key="curva_val")
        
        if st.button("Gerar Cronograma de Gastos", type="primary", key="btn_calc_curvas"):
            fase_fundacao = custo_total_obra * 0.15
            fase_estrutura = custo_total_obra * 0.25
            fase_alvenaria = custo_total_obra * 0.15
            fase_cobertura = custo_total_obra * 0.10
            fase_instalacoes = custo_total_obra * 0.15
            fase_acabamento = custo_total_obra * 0.20

            st.success("Curva S e Cronograma gerados!")
            st.write(f"- **1. Fundação (Terraplanagem/Baldrames):** R$ {fase_fundacao:,.2f} (15%)")
            st.write(f"- **2. Estrutura (Pilares/Vigas/Lajes):** R$ {fase_estrutura:,.2f} (25%)")
            st.write(f"- **3. Alvenaria e Fechamentos:** R$ {fase_alvenaria:,.2f} (15%)")
            st.write(f"- **4. Cobertura e Telhado:** R$ {fase_cobertura:,.2f} (10%)")
            st.write(f"- **5. Instalações (Hidro/Elétrica):** R$ {fase_instalacoes:,.2f} (15%)")
            st.write(f"- **6. Acabamentos e Pintura:** R$ {fase_acabamento:,.2f} (20%)")

            relatorio_cs = f"""=== CONSTRUTECH TUBARÃO - CRONOGRAMA FINANCEIRO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Custo Total: R$ {custo_total_obra:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Cronograma (TXT)",
                data=relatorio_cs,
                file_name="Cronograma_Obra.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "📝 Gerador de Contrato de Empreitada":
    def conteudo():
        st.subheader("📝 Emissor de Minuta de Contrato de Prestação de Serviços")
        col1, col2 = st.columns(2)
        with col1:
            contratante = st.text_input("Nome do Contratante (Cliente):", value="João da Silva", key="ct_cli")
            engenheiro_resp = st.text_input("Nome do Engenheiro / Construtor:", value="Futuro Engenheiro", key="ct_eng")
        with col2:
            valor_contrato = st.number_input("Valor Total do Contrato (R$):", value=80000.0, key="ct_val")
            prazo_meses = st.number_input("Prazo de Execução (meses):", min_value=1, value=6, key="ct_mes")

        if st.button("Gerar Contrato Completo", type="primary", key="btn_calc_contrato"):
            st.success("Contrato gerado com sucesso!")
            
            minuta_texto = f"""CONTRATO PARTICULAR DE PRESTAÇÃO DE SERVIÇOS DE ENGENHARIA E CONSTRUÇÃO
CONSTRUTECH TUBARÃO

CONTRATANTE: {contratante}
CONSTRUTOR / ENGENHEIRO: {engenheiro_resp}

CLÁUSULA PRIMEIRA - DO OBJETO:
O presente contrato tem por objeto a execução de serviços de construção civil sob a responsabilidade técnica e operacional da plataforma Construtech Tubarão.

CLÁUSULA SEGUNDA - DO VALOR E FORMA DE PAGAMENTO:
Pela execução dos serviços, o Contratante pagará o valor global de R$ {valor_contrato:,.2f}, divididos conforme o cronograma físico-finaceiro da obra.

CLÁUSULA TERCEIRA - DO PRAZO:
O prazo estimado para conclusão total dos serviços é de {prazo_meses} meses, contados a partir da ordem de início.

Data de emissão: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
Assinatura das Partes: _____________________________________
"""
            st.text_area("Visualização do Contrato:", value=minuta_texto, height=250)
            
            st.download_button(
                label="📥 Baixar Minuta do Contrato (TXT)",
                data=minuta_texto,
                file_name=f"Contrato_{contratante.replace(' ', '_')}.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

elif modulo == "💼 Faturamento e CNPJ":
    def conteudo():
        st.subheader("Orçamento Comercial e Proposta de Serviços")
        valor_bruto = st.number_input("Valor Base dos Serviços (R$):", value=12000.0, key="fat_val")
        if st.button("Emitir Proposta", type="primary", key="btn_calc_fat"):
            st.success(f"Proposta emitida no valor de R$ {valor_bruto:,.2f}!")
            
            relatorio_fat = f"""=== CONSTRUTECH TUBARÃO - PROPOSTA COMERCIAL ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Valor Base dos Serviços: R$ {valor_bruto:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Proposta Comercial (TXT)",
                data=relatorio_fat,
                file_name="Proposta_Comercial.txt",
                mime="text/plain"
            )

            st.session_state.uso_modulos[modulo] = "bloqueado"

    executar_com_controle_amostra(modulo, conteudo)

# Rodapé
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Construtech Tubarão © 2026 - Todos os direitos reservados</p>",
    unsafe_allow_html=True,
)
