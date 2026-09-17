
import math
import streamlit as st

# Configuração inicial da página
st.set_page_config(
    page_title="Construtech Tubarão - Engenharia & Orçamentos",
    page_icon="🏗️",
    layout="centered",
)

# Estilização visual profissional aprimorada
st.markdown(
    """
    <style>
    .main { background-color: #F8FAFC; }
    .main-title { font-size: 28px; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 0px; }
    .sub-title { font-size: 15px; color: #475569; text-align: center; margin-bottom: 25px; }
    .card-resultado { 
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); 
        padding: 20px; 
        border-radius: 12px; 
        margin-top: 15px; 
        margin-bottom: 15px; 
        border-left: 6px solid #2563EB;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        color: #1E293B;
    }
    .card-alerta {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        padding: 15px;
        border-radius: 10px;
        margin-top: 10px;
        margin-bottom: 15px;
        border-left: 6px solid #D97706;
        color: #92400E;
    }
    .stForm {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Cabeçalho do App
st.markdown(
    '<p class="main-title">🏗️ Construtech Tubarão</p>', unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-title">Sistema Inteligente de Orçamentos e Engenharia para'
    " Construtores</p>",
    unsafe_allow_html=True,
)

# Controle de Créditos na Sessão
if "creditos" not in st.session_state:
    st.session_state.creditos = 5

# Menu de Navegação por Abas
aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs([
    "🧱 Alvenaria",
    "⚙️ Vigas & Concreto",
    "🏠 Lajes",
    "🚰 Hidráulica & Elétrica",
    "🏡 Orçamento Global",
    "💳 Ativar Acesso",
])

# ==========================================
# ABA 1: MATERIAIS E ALVENARIA
# ==========================================
with aba1:
  st.markdown("### 🧱 Calculadora Completa de Alvenaria")
  st.write(
      "Insira os dados da parede para calcular tijolos, cimento e areia com"
      " precisão."
  )

  with st.form("form_alvenaria"):
    area_parede = st.number_input(
        "Área da Parede (m²):", min_value=1.0, value=10.0, step=1.0
    )
    tipo_tijolo = st.selectbox(
        "Tipo de Tijolo / Bloco:",
        [
            "Bloco Cerâmico / Concreto 19x19 cm",
            "Tijolo 8 furos (9x19x19 cm)",
            "Tijolo 6 furos (9x14x19 cm)",
        ],
    )
    preco_saco_cimento = st.number_input(
        "Preço do Saco de Cimento 50kg (R$):",
        min_value=10.0,
        value=42.0,
        step=1.0,
    )
    btn_calcular_alvenaria = st.form_submit_button(
        "🚀 Calcular Materiais da Parede"
    )

  if btn_calcular_alvenaria:
    if st.session_state.creditos <= 0:
      st.error(
          "⚠️ Seus créditos grátis acabaram! Vá na aba 'Ativar Acesso'."
      )
    else:
      st.session_state.creditos -= 1
      if "19x19 cm" in tipo_tijolo:
        qtd_tijolos = area_parede * 25 * 1.15
      elif "8 furos" in tipo_tijolo:
        qtd_tijolos = area_parede * 28 * 1.15
      else:
        qtd_tijolos = area_parede * 42 * 1.15

      qtd_cimento = area_parede * 0.12 * 1.15
      custo_cimento = qtd_cimento * preco_saco_cimento
      qtd_areia_m3 = area_parede * 0.03 * 1.15

      st.markdown(
          f"""
            <div class="card-resultado">
            <h4 style="margin-top:0; color:#1E3A8A;">📊 Relatório de Alvenaria ({area_parede} m²)</h4>
            • <b>Tipo Utilizado:</b> {tipo_tijolo}<br>
            • <b>Blocos/Tijolos (c/ 15% de perda):</b> ~<b>{int(qtd_tijolos)}</b> unidades<br>
            • <b>Cimento (50kg) (c/ 15% perda):</b> ~<b>{round(qtd_cimento, 1)}</b> sacos (Custo est.: R$ {round(custo_cimento, 2)})<br>
            • <b>Areia Média (c/ 15% perda):</b> ~<b>{round(qtd_areia_m3, 2)}</b> m³
            </div>
            """,
          unsafe_allow_html=True,
      )
      st.info(f"💡 Créditos de testes restantes: {st.session_state.creditos}")

# ==========================================
# ABA 2: ESTRUTURAL (VIGAS E CONCRETO)
# ==========================================
with aba2:
  st.markdown("### ⚙️ Dimensionamento Técnico e Comportamento de Viga")
  st.write(
      "Análise avançada de vão, risco de deflexão (embocamento), concreto e"
      " aço."
  )

  with st.form("form_estrutural"):
    col1, col2 = st.columns(2)
    with col1:
      vao_viga = st.number_input(
          "Vão Livre da Viga (m):", min_value=1.0, value=4.0, step=0.5
      )
      largura_viga = st.number_input(
          "Largura / Base (cm):", min_value=10.0, value=14.0, step=2.0
      )
    with col2:
      altura_viga = st.number_input(
          "Altura da Viga (cm):", min_value=15.0, value=30.0, step=5.0
      )
      preco_aco_kg = st.number_input(
          "Preço Médio do Aço (R$/kg):", min_value=5.0, value=12.0, step=1.0
      )

    btn_calcular_estrutural = st.form_submit_button(
        "🚀 Analisar Comportamento e Materiais"
    )

  if btn_calcular_estrutural:
    if st.session_state.creditos <= 0:
      st.error("⚠️ Créditos esgotados! Faça a ativação na aba ao lado.")
    else:
      st.session_state.creditos -= 1

      vol_concreto = (
          (largura_viga / 100) * (altura_viga / 100) * vao_viga * 1.15
      )
      sacos_cimento_viga = vol_concreto * 7.5
      areia_viga_m3 = vol_concreto * 0.55
      brita_viga_m3 = vol_concreto * 0.65
      peso_aco_kg = vao_viga * (largura_viga * altura_viga / 100) * 0.14 * 1.15
      custo_aco = peso_aco_kg * preco_aco_kg
      qtd_estribos = math.ceil((vao_viga * 100) / 15) + 1

      if vao_viga <= 4.0:
        status_vao = (
            "<b>Vão Seguro (Baixo Risco de Flecha):</b> Seção adequada para o"
            " vão informado. Mantém boa rigidez."
        )
        bitola_long = "4 barras de 10 mm (CA-50) [Inferior e Superior]"
      elif vao_viga <= 6.0:
        status_vao = (
            "<b>Atenção ao Vão (Alerta de Flexão):</b> Vãos entre 4m e 6m exigem"
            " rigor na cura e contra-flecha de 0,5% no escoramento."
        )
        bitola_long = "4 barras de 12.5 mm (CA-50) [Exige reforço nos apoios]"
      else:
        status_vao = (
            "<b>Vão Longo / Crítico:</b> Vãos acima de 6 metros sofrem forte"
            " solicitação. Obrigatório uso de vigas mais altas."
        )
        bitola_long = (
            "6 barras de 12.5 mm ou 16 mm (CA-50) [Armação dupla obrigatória]"
        )

      st.markdown(
          f"""
            <div class="card-resultado">
            <h4 style="margin-top:0; color:#1E3A8A;">🏗️ Relatório Estrutural da Viga ({largura_viga}x{altura_viga} cm | Vão: {vao_viga}m)</h4>
            <div class="card-alerta"><b>📐 Análise de Rigidez:</b><br>{status_vao}</div>
            <b>1. Insumos de Concreto (c/ 15% perda):</b><br>
            • Volume Total: ~<b>{round(vol_concreto, 2)}</b> m³<br>
            • Cimento: ~<b>{round(sacos_cimento_viga, 1)}</b> sacos | Areia: ~<b>{round(areia_viga_m3, 2)}</b> m³ | Brita: ~<b>{round(brita_viga_m3, 2)}</b> m³<br><br>
            <b>2. Detalhamento do Aço (CA-50) (c/ 15% perda):</b><br>
            • Ferro Longitudinal: <b>{bitola_long}</b><br>
            • Peso de Aço: ~<b>{round(peso_aco_kg, 1)}</b> kg (Est. R$ {round(custo_aco, 2)})<br>
            • Estribos (4.2mm): ~<b>{int(qtd_estribos)}</b> peças a cada 15 cm
            </div>
            """,
          unsafe_allow_html=True,
      )
      st.info(f"💡 Créditos restantes: {st.session_state.creditos}")

# ==========================================
# ABA 3: LAJES PRÉ-MOLDADAS
# ==========================================
with aba3:
  st.markdown("### 🏠 Dimensionamento de Lajes Pré-Moldadas (Treliçadas)")
  st.write(
      "Cálculo estrutural padrão de vigotas, enchimento, capa de concreto e"
      " malha de distribuição."
  )

  with st.form("form_laje"):
    col1, col2 = st.columns(2)
    with col1:
      largura_laje = st.number_input(
          "Largura / Menor Vão da Laje (m):",
          min_value=1.0,
          value=4.0,
          step=0.5,
      )
      comprimento_laje = st.number_input(
          "Comprimento / Maior Vão (m):", min_value=1.0, value=5.0, step=0.5
      )
    with col2:
      tipo_laje = st.selectbox(
          "Altura / Tipo da Laje:",
          [
              "Laje H8 (Forro / Pequena carga)",
              "Laje H12 (Convencional Residencial)",
              "Laje H16 (Sobre-cargas maiores)",
              "Laje H20 (Grandes vãos)",
          ],
      )
      enchimento = st.selectbox(
          "Material de Enchimento:",
          ["Lajota Cerâmica Padrão", "Bloco de EPS (Isopor)"],
      )

    btn_calcular_laje = st.form_submit_button("🚀 Calcular Materiais da Laje")

  if btn_calcular_laje:
    if st.session_state.creditos <= 0:
      st.error("⚠️ Créditos esgotados! Vá na aba 'Ativar Acesso'.")
    else:
      st.session_state.creditos -= 1
      area_laje = largura_laje * comprimento_laje
      espessura_capa = 0.04
      qtd_vigotas = math.ceil((comprimento_laje / 0.42) * 1.15)
      metro_linear_vigotas = qtd_vigotas * largura_laje
      qtd_enchimento = math.ceil(area_laje * 8.5 * 1.15)
      vol_concreto_capa = (area_laje * espessura_capa) * 1.15
      sacos_cimento_laje = vol_concreto_capa * 7.5
      areia_laje_m3 = vol_concreto_capa * 0.55
      brita_laje_m3 = vol_concreto_capa * 0.65
      qtd_malha_pop = math.ceil((area_laje / 5.5) * 1.15)

      st.markdown(
          f"""
            <div class="card-resultado">
            <h4 style="margin-top:0; color:#1E3A8A;">📋 Relatório Técnico da Laje ({area_laje:.1f} m² | {tipo_laje})</h4>
            <b>1. Elementos Pré-Fabricados (c/ 15% perda):</b><br>
            • <b>Vigotas Treliçadas:</b> ~<b>{int(qtd_vigotas)}</b> peças (Total: <b>{round(metro_linear_vigotas, 1)}</b> metros lineares)<br>
            • <b>Enchimento ({enchimento}):</b> ~<b>{int(qtd_enchimento)}</b> unidades<br><br>
            <b>2. Capa de Concreto ({int(espessura_capa*100)}cm c/ 15% perda):</b><br>
            • Volume de Concreto: ~<b>{round(vol_concreto_capa, 2)}</b> m³<br>
            • Cimento: ~<b>{round(sacos_cimento_laje, 1)}</b> sacos | Areia: ~<b>{round(areia_laje_m3, 2)}</b> m³ | Brita: ~<b>{round(brita_laje_m3, 2)}</b> m³<br><br>
            <b>3. Armadura de Distribuição (c/ 15% perda):</b><br>
            • Malha Pop recomendada: ~<b>{int(qtd_malha_pop)}</b> painéis
            </div>
            """,
          unsafe_allow_html=True,
      )
      st.info(f"💡 Créditos restantes: {st.session_state.creditos}")

# ==========================================
# ABA 4: HIDRÁULICA & ELÉTRICA (INFRAESTRUTURA)
# ==========================================
with aba4:
  st.markdown("### 🚰 Orçamento de Infraestrutura (Hidráulica & Elétrica)")
  st.write(
      "Estime a quantidade de tubos de água, esgoto, conexões e"
      " mangueiras/conduítes corrugados com base na metragem da construção."
  )

  with st.form("form_hidro_eletrica"):
    area_infra = st.number_input(
        "Metragem da Área Construída (m²):",
        min_value=15.0,
        value=80.0,
        step=5.0,
    )
    qtd_banheiros = st.number_input(
        "Número de Banheiros / Lavabos:", min_value=1, value=1, step=1
    )
    tem_cozinha_gourmet = st.selectbox(
        "Possui Cozinha / Área de Serviço Completa?", ["Sim", "Não"]
    )

    btn_calcular_infra = st.form_submit_button(
        "🚀 Calcular Tubos, Conduítes e Insumos"
    )

  if btn_calcular_infra:
    if st.session_state.creditos <= 0:
      st.error("⚠️ Créditos esgotados! Vá na aba 'Ativar Acesso'.")
    else:
      st.session_state.creditos -= 1

      fator_banheiro = 1.0 + (qtd_banheiros - 1) * 0.35

      metros_conduite = math.ceil((area_infra * 4.5) * 1.15)
      caixas_luz = math.ceil((area_infra / 3.5) * 1.15)

      tubos_agua_fria = math.ceil(((area_infra * 0.25) * fator_banheiro) * 1.15)
      tubos_esgoto = math.ceil(((area_infra * 0.18) * fator_banheiro) * 1.15)

      custo_est_hidraulica = (
          (tubos_agua_fria * 35)
          + (tubos_esgoto * 48)
          + (qtd_banheiros * 450)
      )
      custo_est_eletrica = (
          (metros_conduite * 2.80) + (caixas_luz * 3.50) + (area_infra * 18)
      )
      custo_total_infra = custo_est_eletrica + custo_est_hidraulica

      st.markdown(
          f"""
            <div class="card-resultado">
            <h4 style="margin-top:0; color:#1E3A8A;">📋 Relatório de Infraestrutura ({area_infra} m² | {qtd_banheiros} Banheiro(s))</h4>
            
            <b>1. Elétrica Básica (Eletrodutos e Caixas) (c/ 15% perda):</b><br>
            • Mangueiras / Conduítes Corrugados: ~<b>{int(metros_conduite)}</b> metros<br>
            • Caixas de Luz (4x2 / 4x4): ~<b>{int(caixas_luz)}</b> unidades<br>
            • Custo Estimado (Conduítes + Caixas + Fios básicos): R$ <b>{custo_est_eletrica:,.2f}</b><br><br>
            
            <b>2. Hidráulica (Água Fria e Esgoto) (c/ 15% perda):</b><br>
            • Tubos de Água Fria (barras 3m): ~<b>{int(tubos_agua_fria)}</b> barras<br>
            • Tubos de Esgoto / Sifões (barras 3m): ~<b>{int(tubos_esgoto)}</b> barras<br>
            • Custo Estimado (Tubos + Conexões + Registros): R$ <b>{custo_est_hidraulica:,.2f}</b><br><br>
            
            <div class="card-alerta">
            <b>💰 Custo Total Parcial de Infraestrutura: R$ {custo_total_infra:,.2f}</b>
            </div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      texto_infra = f"""CONSTRUTECH TUBARÃO - RELATÓRIO DE INFRAESTRUTURA
--------------------------------------------------
Área Construída: {area_infra} m²
Banheiros: {qtd_banheiros}
Cozinha Completa: {tem_cozinha_gourmet}

1. ELÉTRICA BÁSICA:
- Conduítes Corrugados: ~{int(metros_conduite)} metros
- Caixas de Luz: ~{int(caixas_luz)} unidades
- Custo Estimado: R$ {custo_est_eletrica:,.2f}

2. HIDRÁULICA (ÁGUA FRIA E ESGOTO):
- Tubos de Água Fria (3m): ~{int(tubos_agua_fria)} barras
- Tubos de Esgoto / Sifões (3m): ~{int(tubos_esgoto)} barras
- Custo Estimado: R$ {custo_est_hidraulica:,.2f}

VALOR TOTAL DA INFRAESTRUTURA: R$ {custo_total_infra:,.2f}
--------------------------------------------------
Gerado via Construtech Tubarão - Engenharia
"""
      st.download_button(
          label="📥 Baixar Relatório de Infraestrutura (.txt)",
          data=texto_infra,
          file_name="relatorio_infraestrutura.txt",
          mime="text/plain",
          key="dl_infra",
      )

      st.info(f"💡 Créditos restantes: {st.session_state.creditos}")

# ==========================================
# ABA 5: ORÇAMENTO GLOBAL (CASA / EMPRESA)
# ==========================================
with aba5:
  st.markdown("### 🏡 Orçamento Executivo Global (Residencial & Comercial)")
  st.write(
      "Orçamento de ponta a ponta dimensionado para projetos de pequeno,"
      " médio ou grande porte (Casas, Lojas e Empresas)."
  )

  with st.form("form_orcamento_global"):
    col1, col2 = st.columns(2)
    with col1:
      tipo_projeto = st.selectbox(
          "Tipo de Empreendimento:",
          [
              "Residencial (Casa / Sobrado)",
              "Comercial / Empresa (Loja / Galpão / Escritório)",
          ],
      )
      area_total_obra = st.number_input(
          "Área Construída Total (m²):",
          min_value=15.0,
          value=120.0,
          step=10.0,
      )
      padrao_acabamento = st.selectbox(
          "Padrão de Acabamento / Especificação:",
          [
              "Padrão Popular / Econômico",
              "Padrão Médio (Padrão Mercado)",
              "Padrão Alto / Corporativo Fino",
          ],
      )
    with col2:
      custo_medio_material_m2 = st.number_input(
          "Custo de Materiais por m² (R$):",
          min_value=400.0,
          value=1250.0,
          step=50.0,
      )
      custo_mao_obra_m2 = st.number_input(
          "Preço de Mão de Obra por m² (R$):",
          min_value=250.0,
          value=800.0,
          step=50.0,
      )
      margem_lucro_empreiteiro = st.slider(
          "Margem de Lucro / BDI Desejado (%):",
          min_value=5,
          max_value=35,
          value=15,
          step=1,
      )

    btn_calcular_global = st.form_submit_button(
        "🚀 Gerar Proposta Comercial Completa"
    )

  if btn_calcular_global:
    if st.session_state.creditos <= 0:
      st.error("⚠️ Créditos esgotados! Vá na aba 'Ativar Acesso'.")
    else:
      st.session_state.creditos -= 1

      if "Comercial" in tipo_projeto:
        fator_base = 1.15
      else:
        fator_base = 1.0

      if "Econômico" in padrao_acabamento:
        fator_padrao = 0.9
      elif "Alto" in padrao_acabamento:
        fator_padrao = 1.4
      else:
        fator_padrao = 1.0

      fator_total = fator_base * fator_padrao

      total_materiais = (
          area_total_obra * custo_medio_material_m2
      ) * fator_total
      total_mao_obra = (area_total_obra * custo_mao_obra_m2) * fator_total
      custo_direto_total = total_materiais + total_mao_obra

      lucro_valor = custo_direto_total * (margem_lucro_empreiteiro / 100)
      preco_venda_proposta = custo_direto_total + lucro_valor

      est_tijolos = area_total_obra * 27 * 1.15
      est_cimento = area_total_obra * 1.9 * 1.15
      est_aco = area_total_obra * 15 * 1.15

      st.markdown(
          f"""
            <div class="card-resultado">
            <h4 style="margin-top:0; color:#1E3A8A;">📈 Proposta Comercial Fechada: {tipo_projeto} ({area_total_obra} m²)</h4>
            
            <b>1. Custos Diretos Estimados:</b><br>
            • 📦 <b>Insumos / Materiais:</b> R$ <b>{total_materiais:,.2f}</b><br>
            • 🛠️ <b>Mão de Obra Executiva:</b> R$ <b>{total_mao_obra:,.2f}</b><br>
            • 💰 <b>Custo Operacional Total:</b> R$ <b>{custo_direto_total:,.2f}</b><br><br>
            
            <div class="card-alerta">
            <b>💼 Fechamento de Contrato para Lucro ({margem_lucro_empreiteiro}% de BDI):</b><br>
            • <b>Seu Lucro Estimado na Obra:</b> R$ <b>{lucro_valor:,.2f}</b><br>
            • 🎯 <b>VALOR SUGERIDO DA PROPOSTA (CHAVE NA MÃO): R$ {preco_venda_proposta:,.2f}</b>
            </div><br>
            
            <b>2. Dimensionamento Macro de Insumos (c/ 15% perda):</b><br>
            • Blocos / Tijolos totais: ~<b>{int(est_tijolos)}</b> unidades<br>
            • Cimento estrutural e argamassa (50kg): ~<b>{int(est_cimento)}</b> sacos<br>
            • Aço estrutural total: ~<b>{int(est_aco)}</b> kg
            </div>
            """,
          unsafe_allow_html=True,
      )

      texto_proposta = f"""CONSTRUTECH TUBARÃO - PROPOSTA COMERCIAL
--------------------------------------------------
Empreendimento: {tipo_projeto}
Área Total: {area_total_obra} m²
Padrão: {padrao_acabamento}

1. CUSTOS DIRETOS ESTIMADOS:
- Insumos / Materiais: R$ {total_materiais:,.2f}
- Mão de Obra Executiva: R$ {total_mao_obra:,.2f}
- Custo Operacional Total: R$ {custo_direto_total:,.2f}

2. FECHAMENTO DE CONTRATO ({margem_lucro_empreiteiro}% BDI):
- Lucro Estimado: R$ {lucro_valor:,.2f}
- VALOR TOTAL SUGERIDO (CHAVE NA MÃO): R$ {preco_venda_proposta:,.2f}

3. INSUMOS MACRO (c/ 15% perda):
- Blocos / Tijolos: ~{int(est_tijolos)} un
- Cimento (50kg): ~{int(est_cimento)} sacos
- Aço Estrutural: ~{int(est_aco)} kg
--------------------------------------------------
Gerado via Construtech Tubarão - Engenharia
"""
      st.download_button(
          label="📥 Baixar Proposta Comercial em Texto (.txt)",
          data=texto_proposta,
          file_name="proposta_orcamento_obra.txt",
          mime="text/plain",
          key="dl_global",
      )

      st.info(f"💡 Créditos restantes: {st.session_state.creditos}")

# ==========================================
# ABA 6: PAGAMENTO E ATIVAÇÃO
# ==========================================
with aba6:
  st.markdown("### 💳 Ativar Acesso Profissional - R$ 20,00")
  st.write("Garante uso ilimitado de todas as calculadoras por 30 dias.")

  st.markdown(
      """
    <div class="card-resultado">
    <b>Instruções de Ativação:</b><br>
    1. Faça um Pix no valor de <b>R$ 20,00</b> para a chave oficial.<br>
    2. Envie o comprovante no WhatsApp do suporte para liberar o seu acesso instantâneo.
    </div>
    """,
      unsafe_allow_html=True,
  )

  st.text_input(
      "Chave Pix (CPF / CNPJ / Celular):", value="[Sua Chave Pix Aqui]"
  )
  st.text_input(
      "WhatsApp para Envio do Comprovante:", value="[Seu Número com DDD Aqui]"
  )

  if st.button("✅ Já realizei o pagamento"):
    st.session_state.creditos = 50
    st.success(
        "🎉 Acesso liberado com sucesso! Volte às abas de cálculo e aproveite"
        " o sistema."
    )
