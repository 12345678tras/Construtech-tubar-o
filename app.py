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
# Criamos um controle na barra lateral para o usuário escolher o tema
modo_escuro = st.sidebar.toggle("🌙 Ativar Modo Escuro", value=False)

if modo_escuro:
    # Estilo CSS para o Modo Escuro
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
    # Estilo CSS para o Modo Claro (Padrão)
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
# 3. MENU LATERAL
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
    "💼 Faturamento e CNPJ",
]

modulo = st.sidebar.selectbox("Selecione a Ferramenta:", lista_modulos)

st.sidebar.markdown("---")
# Painel do Administrador para conferir os comprovantes enviados
with st.sidebar.expander("🛠️ Painel do Administrador"):
    st.write("Comprovantes enviados por clientes:")
    if st.session_state.historico_comprovantes:
        for idx, item in enumerate(st.session_state.historico_comprovantes):
            st.text(f"{idx+1}. Mod: {item['modulo']}\nComp: {item['comprovante']}\nData: {item['data']}")
    else:
        st.write("Nenhum comprovante enviado ainda.")

if st.sidebar.button("🔄 Resetar Sessão (Simular Fechamento)"):
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
        st.markdown(f'<p class="main-header">🔒 Limite da Amostra Grátis Atingido: {nome_modulo}</p>', unsafe_allow_html=True)
        st.info("💡 Escolha uma das opções abaixo para realizar o pagamento de **R$ 20,00** para **CAC CONTABILIZANDO** e cole o comprovante ao lado.")

        # DIVISÃO LADO A LADO: PAGAMENTO (ESQUERDA) E COMPROVANTE (DIREITA)
        st.markdown('<div class="box-pagamento">', unsafe_allow_html=True)
        col_pag1, col_pag2 = st.columns(2, gap="large")

        with col_pag1:
            st.markdown("### 1️⃣ Escolha a Forma de Pagamento")
            
            # Opção Cartão / Link
            st.markdown(
                '<a href="https://link.infinitepay.io/cristiane-da-260/VC1DLTAtUg-HgBiSH5iQO-20,00" target="_blank" class="btn-pagar">💳 PAGAR COM CARTÃO / LINK</a>',
                unsafe_allow_html=True
            )
            
            # Opção Pix Direto Logo Abaixo
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
            st.markdown("### 2️⃣ Cole o Comprovante ao Lado")
            st.markdown("Tanto para Cartão quanto para Pix, cole o código ou ID do comprovante abaixo:")
            
            comprovante_texto = st.text_area(
                "Cole o comprovante / ID da transação aqui:", 
                key=f"comp_{nome_modulo}", 
                placeholder="Ex: Cole aqui os dados do comprovante gerado...",
                height=120
            )
            
            if st.button("✨ Liberar Acesso Automaticamente", key=f"btn_gerar_{nome_modulo}", type="primary", use_container_width=True):
                if comprovante_texto.strip() != "":
                    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    st.session_state.historico_comprovantes.append({
                        "modulo": nome_modulo,
                        "comprovante": comprovante_texto.strip(),
                        "data": data_atual
                    })
                    
                    st.session_state.liberado_pago = True
                    st.success("Comprovante validado e registrado com sucesso! Acesso liberado.")
                    st.rerun()
                else:
                    st.warning("⚠️ Você precisa colar o comprovante na caixa ao lado para liberar o acesso.")

        st.markdown('</div>', unsafe_allow_html=True)
        return

    funcao_conteudo()

# ==========================================
# 5. MÓDULOS DA APLICAÇÃO COM RELATÓRIO EM PDF/TEXTO
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
            
            # Botão para baixar relatório em texto formatado (pronto para imprimir como PDF no navegador)
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
                label="📥 Baixar Relatório do Cálculo (TXT/PDF)",
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
Material: {tipo_material}
--------------------------------------------------
- Blocos/Tijolos Totais: {int(total_blocos)} un
- Sacos de Cimento (50kg): {sacos_c:.1f} sc
- Areia Média: {m3_a:.2f} m³
- Custo Total Estimado: R$ {custo_tot:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Alvenaria (TXT/PDF)",
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
                [
                    "Lajota Cerâmica Tradicional",
                    "Bloco de Isopor (EPS - Alta Densidade)",
                    "Lajota Concreto / Paulistinha"
                ],
                key="laje_enchimento"
            )
        with col2:
            altura_laje = st.selectbox(
                "Altura da Laje (Vigota + Capa):",
                [
                    "H8 (8 cm vigota + 3 cm capa = 11 cm total)",
                    "H12 (12 cm vigota + 4 cm capa = 16 cm total)",
                    "H16 (16 cm vigota + 4 cm capa = 20 cm total)",
                    "H20 (20 cm vigota + 5 cm capa = 25 cm total)"
                ],
                key="laje_altura"
            )

        if st.button("Calcular Materiais e Ferro da Laje", type="primary", key="btn_calc_laje"):
            ml_vigotas = area_laje * 1.35
            if "Cerâmica" in tipo_enchimento:
                qtd_blocos = area_laje * 8.3
            elif "Isopor" in tipo_enchimento:
                qtd_blocos = area_laje * 2.5
            else:
                qtd_blocos = area_laje * 8.0

            if "H8" in altura_laje:
                vol_concreto_m3 = area_laje * 0.050
            elif "H12" in altura_laje:
                vol_concreto_m3 = area_laje * 0.065
            elif "H16" in altura_laje:
                vol_concreto_m3 = area_laje * 0.080
            else:
                vol_concreto_m3 = area_laje * 0.100

            vol_concreto_com_perda = vol_concreto_m3 * 1.07
            sacos_cimento_laje = vol_concreto_com_perda * 6.5 

            st.success("Soma de materiais da laje realizada!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Vigotas Pré-moldadas", f"{ml_vigotas:.1f} m lineares")
            c2.metric("Blocos / Lajotas", f"{int(qtd_blocos)} un")
            c3.metric("Concreto (Capa)", f"{vol_concreto_com_perda:.2f} m³")

            relatorio_laje = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE LAJES ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Área da Laje: {area_laje} m²
Enchimento: {tipo_enchimento}
Altura: {altura_laje}
--------------------------------------------------
- Vigotas Pré-moldadas: {ml_vigotas:.1f} m lineares
- Blocos / Lajotas: {int(qtd_blocos)} un
- Concreto para Capa: {vol_concreto_com_perda:.2f} m³
- Sacos de Cimento (Capa): {sacos_cimento_laje:.1f} sc
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Laje (TXT/PDF)",
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
                [
                    "Traço 1:2:3 (Fck 25 MPa - Estrutural Forte)",
                    "Traço 1:2.5:3.5 (Fck 20 MPa - Residencial Padrão)",
                    "Traço 1:3:5 (Contrapiso / Lastro Magro)"
                ],
                key="conc_traco"
            )

        if st.button("Calcular Volume e Quantidade de Sacos", type="primary", key="btn_calc_conc"):
            volume_real = (area_concreto * (espessura_cm / 100.0)) * 1.07 
            if "25 MPa" in traco_tipo:
                sc_cif = volume_real * 7.5
                areia_m3 = volume_real * 0.55
                brita_m3 = volume_real * 0.75
            elif "20 MPa" in traco_tipo:
                sc_cif = volume_real * 6.5
                areia_m3 = volume_real * 0.60
                brita_m3 = volume_real * 0.78
            else:
                sc_cif = volume_real * 5.0
                areia_m3 = volume_real * 0.65
                brita_m3 = volume_real * 0.80

            st.success("Cálculo de concreto finalizado!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Volume Total com Perda", f"{volume_real:.2f} m³")
            c2.metric("Sacos de Cimento (50kg)", f"{sc_cif:.1f} sacos")
            c3.metric("Areia / Brita", f"{areia_m3:.2f} m³ / {brita_m3:.2f} m³")

            relatorio_conc = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO DE CONCRETO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Área: {area_concreto} m² | Espessura: {espessura_cm} cm
Traço: {traco_tipo}
--------------------------------------------------
- Volume Total com Perda (7%): {volume_real:.2f} m³
- Sacos de Cimento (50kg): {sc_cif:.1f} sacos
- Areia Média: {areia_m3:.2f} m³
- Brita: {brita_m3:.2f} m³
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Concreto (TXT/PDF)",
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
Área Construída: {area_obra} m²
Preço do Aço/kg: R$ {preco_aco_kg:.2f}
--------------------------------------------------
- Peso Estimado de Aço: {peso_tot:.1f} kg
- Custo Total Estimado do Aço: R$ {custo_tot_aco:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório de Aço (TXT/PDF)",
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
                "Bitola do Ferro Principal (Fundo/Topo):",
                [
                    "Ferro 3/8'' (10.0 mm) - Padrão Estrutural",
                    "Ferro 5/16'' (8.0 mm) - Leve",
                    "Ferro 1/2'' (12.5 mm) - Grande Vão / Sobrado"
                ],
                key="viga_bitola"
            )
            espacamento_estribo = st.selectbox(
                "Espaçamento dos Estribos (Ferro 1/4'' / 6.3mm):",
                ["A cada 10 cm nas pontas / 15 cm no meio", "A cada 15 cm em todo o comprimento"]
            )

        if st.button("Calcular Quantidade de Ferro das Vigas", type="primary", key="btn_calc_vigas"):
            kg_por_viga = vao_viga * 8.5 * qtd_pecas
            estribos_un = int((vao_viga / 0.12) * qtd_pecas)
            
            st.success("Dimensionamento de vigas e bitolas concluído!")
            c1, c2, c3 = st.columns(3)
            c1.metric("Ferro Principal", tipo_bitola_principal.split(" - ")[0])
            c2.metric("Peso Total", f"{kg_por_viga:.1f} kg")
            c3.metric("Estribos", f"{estribos_un} un")
            
            relatorio_vigas = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO ESTRUTURAL ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Vão Livre: {vao_viga} m | Qtd Peças: {qtd_pecas}
Bitola Principal: {tipo_bitola_principal}
Espaçamento de Estribos: {espacamento_estribo}
--------------------------------------------------
- Peso Total de Ferro: {kg_por_viga:.1f} kg
- Quantidade de Estribos (6.3mm): {estribos_un} unidades
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório Estrutural (TXT/PDF)",
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
            distancia_fossa = st.number_input("Distância até a Fossa / Rede da Rua (metros):", min_value=2.0, value=10.0, step=1.0, key="hid_dist")
            incluir_fossa = st.checkbox("Incluir Orçamento de Fossa Séptica + Sumidouro", value=True, key="hid_fos")

        if st.button("Calcular Soma de Peças Hidráulicas", type="primary", key="btn_calc_hid"):
            cano_esgoto_100 = (qtd_banheiros * 6.0) + distancia_fossa
            cano_esgoto_50 = qtd_banheiros * 5.0 + (qtd_cozinhas * 4.0)
            cano_agua_25 = (qtd_banheiros * 8.0) + (qtd_cozinhas * 6.0)
            joelhos_100 = (qtd_banheiros * 6) + 4
            joelhos_25 = (qtd_banheiros * 10) + (qtd_cozinhas * 6)
            caixa_gordura = qtd_cozinhas * 1

            st.success("Soma hidráulica gerada com sucesso!")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 📏 Tubos e Conexões de Esgoto")
                st.write(f"- Tubo Esgoto 100mm: **{cano_esgoto_100:.1f} metros**")
                st.write(f"- Tubo Esgoto 50mm: **{cano_esgoto_50:.1f} metros**")
                st.write(f"- Joelhos 100mm: **{joelhos_100} unidades**")
            with c2:
                st.markdown("### 💧 Água Fria e Acessórios")
                st.write(f"- Tubo PVC Água Fria 25mm: **{cano_agua_25:.1f} metros**")
                st.write(f"- Joelhos 25mm: **{joelhos_25} unidades**")
                st.write(f"- Caixa de Gordura: **{caixa_gordura} unidade(s)**")

            relatorio_hid = f"""=== CONSTRUTECH TUBARÃO - RELATÓRIO HIDRÁULICO ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Banheiros: {qtd_banheiros} | Cozinhas: {qtd_cozinhas}
Distância Fossa: {distancia_fossa} m
--------------------------------------------------
- Tubo Esgoto 100mm: {cano_esgoto_100:.1f} m
- Tubo Esgoto 50mm: {cano_esgoto_50:.1f} m
- Joelhos 100mm: {joelhos_100} un
- Tubo Água Fria 25mm: {cano_agua_25:.1f} m
- Joelhos 25mm: {joelhos_25} un
- Caixa de Gordura: {caixa_gordura} un
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Relatório Hidráulico (TXT/PDF)",
                data=relatorio_hid,
                file_name="Relatorio_Hidraulico.txt",
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
            
            relatorio_fat = f=== CONSTRUTECH TUBARÃO - PROPOSTA COMERCIAL ===
Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}
--------------------------------------------------
Valor Base dos Serviços: R$ {valor_bruto:,.2f}
==================================================
Gerado por Construtech Tubarão - Plataforma de Engenharia
"""
            st.download_button(
                label="📥 Baixar Proposta Comercial (TXT/PDF)",
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
