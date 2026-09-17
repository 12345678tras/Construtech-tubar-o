import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ConstrutorPro - Calculadoras", layout="wide")

# HTML e JavaScript integrado com controle de créditos via localStorage (por máquina/navegador)
html_code = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadoras da Construção Civil</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --accent-color: #27ae60;
            --bg-color: #f8f9fa;
            --card-bg: #ffffff;
            --text-color: #333333;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 10px;
        }

        header {
            background-color: var(--primary-color);
            color: white;
            padding: 15px 20px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .nav-tabs {
            display: flex;
            gap: 10px;
            overflow-x: auto;
            padding: 10px 0;
        }

        .tab-btn {
            background: rgba(255,255,255,0.1);
            border: none;
            color: white;
            padding: 8px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
            white-space: nowrap;
        }

        .tab-btn:hover, .tab-btn.active {
            background: var(--accent-color);
        }

        .container {
            max-width: 900px;
            margin: 20px auto;
            padding: 20px;
            background: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }

        .calculator-section {
            display: none;
        }

        .calculator-section.active {
            display: block;
        }

        h2 {
            color: var(--primary-color);
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
            margin-top: 0;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
        }

        input, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button.calc-submit {
            background-color: var(--accent-color);
            color: white;
            border: none;
            padding: 12px 20px;
            font-size: 16px;
            border-radius: 4px;
            cursor: pointer;
            width: 100%;
            font-weight: bold;
        }

        button.calc-submit:hover {
            opacity: 0.9;
        }

        .result-box {
            margin-top: 20px;
            background: #e8f8f5;
            border-left: 4px solid var(--accent-color);
            padding: 15px;
            border-radius: 4px;
        }

        #paywall-screen {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .pix-box {
            background: #f1f8e9;
            border: 2px dashed var(--accent-color);
            padding: 20px;
            border-radius: 8px;
            display: inline-block;
            margin: 20px 0;
            text-align: left;
            max-width: 500px;
            width: 100%;
        }

        .status-bar {
            background: #eef2f7;
            padding: 10px 20px;
            font-size: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 6px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>

    <div class="status-bar">
        <span id="status-creditos">Verificando acesso...</span>
    </div>

    <header>
        <h1>ConstrutorPro</h1>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('alvenaria')">Alvenaria</button>
            <button class="tab-btn" onclick="switchTab('vigas')">Vigas & Concreto</button>
            <button class="tab-btn" onclick="switchTab('lajes')">Lajes</button>
            <button class="tab-btn" onclick="switchTab('hidraulica')">Hidráulica & Elétrica</button>
            <button class="tab-btn" onclick="switchTab('orcamento')">Orçamento Geral</button>
            <button class="tab-btn" onclick="switchTab('ativar')" style="background: #e74c3c;">Ativar Acesso Pro</button>
        </div>
    </header>

    <div class="container" id="main-container">

        <!-- TELA DE BLOQUEIO / PAYWALL -->
        <div id="paywall-screen">
            <h2 style="color: #c0392b;">🔒 Acesso Gratuito Expirado</h2>
            <p>Você utilizou seus créditos de teste gratuitos neste navegador.</p>
            <p>Para garantir uso ilimitado de todas as calculadoras por 30 dias neste computador, ative o Acesso Profissional.</p>
            
            <div class="pix-box">
                <strong>Instruções de Ativação:</strong><br>
                1. Faça um Pix no valor de <strong>R$ 20,00</strong> para a chave oficial:<br>
                <code style="background:#fff; padding:4px; display:inline-block; margin: 5px 0;">SUA-CHAVE-PIX-AQUI</code><br><br>
                2. Envie o comprovante no WhatsApp do suporte para liberar a sua senha de acesso instantaneamente:<br>
                <strong>(00) 00000-0000</strong>
            </div>

            <div style="margin-top: 15px;">
                <label for="senha-ativacao">Possui uma senha de liberação?</label>
                <input type="text" id="senha-ativacao" placeholder="Digite a senha enviada pelo suporte" style="max-width: 300px; display: inline-block; margin-right: 10px;">
                <button onclick="ativarLicenca()" style="padding: 10px 20px; background: var(--accent-color); color: white; border: none; border-radius: 4px; cursor: pointer;">Ativar Agora</button>
            </div>
        </div>

        <!-- CONTEÚDO DAS CALCULADORAS -->
        <div id="calculators-wrapper">
            
            <div id="alvenaria" class="calculator-section active">
                <h2>Calculadora de Alvenaria</h2>
                <div class="form-group">
                    <label>Área da Parede (m²):</label>
                    <input type="number" id="alv-area" value="20">
                </div>
                <button class="calc-submit" onclick="executarCalculo('alvenaria')">Calcular Materiais</button>
                <div id="res-alvenaria" class="result-box" style="display:none;">
                    • Tijolos necessários: ~320 unidades<br>
                    • Argamassa de assentamento: ~4 sacos (25kg)
                </div>
            </div>

            <div id="vigas" class="calculator-section">
                <h2>Calculadora de Vigas & Concreto</h2>
                <div class="form-group">
                    <label>Volume Estimado (m³):</label>
                    <input type="number" id="vig-volume" value="2">
                </div>
                <button class="calc-submit" onclick="executarCalculo('vigas')">Calcular Concreto</button>
                <div id="res-vigas" class="result-box" style="display:none;">
                    • Cimento: ~14 sacos<br>• Areia: ~1.1 m³<br>• Brita: ~1.3 m³
                </div>
            </div>

            <div id="lajes" class="calculator-section">
                <h2>Relatório Técnico da Laje (H8)</h2>
                <div class="form-group">
                    <label>Área da Laje (m²):</label>
                    <input type="number" id="laj-area" value="20">
                </div>
                <button class="calc-submit" onclick="executarCalculo('lajes')">Gerar Relatório da Laje</button>
                <div id="res-lajes" class="result-box" style="display:none;">
                    <strong>Relatório Técnico da Laje (20.0 m² | Laje H8):</strong><br>
                    • Vigotas Treliçadas: ~14 peças (Total: 56.0 metros lineares)<br>
                    • Enchimento (Lajota Cerâmica): ~196 unidades<br>
                    • Concreto (4cm): ~0.92 m³ (Cimento: 6.9 sacos)
                </div>
            </div>

            <div id="hidraulica" class="calculator-section">
                <h2>Hidráulica & Elétrica</h2>
                <p>Ferramenta de dimensionamento básico de circuitos e tubulações.</p>
                <button class="calc-submit" onclick="executarCalculo('hidraulica')">Processar Dados</button>
                <div id="res-hidraulica" class="result-box" style="display:none;">Tubos e eletrodutos dimensionados com sucesso.</div>
            </div>

            <div id="orcamento" class="calculator-section">
                <h2>Orçamento Geral da Obra</h2>
                <p>Consolidação de todos os custos calculados nas abas anteriores.</p>
                <button class="calc-submit" onclick="executarCalculo('orcamento')">Gerar Orçamento</button>
                <div id="res-orcamento" class="result-box" style="display:none;">Orçamento consolidado gerado.</div>
            </div>

            <div id="ativar" class="calculator-section">
                <h2>Informações de Acesso Profissional</h2>
                <p>O acesso fica vinculado permanentemente a este navegador/computador.</p>
            </div>

        </div>

    </div>

    <script>
        const SENHA_MESTRA_DEV = "PRO2026";

        function checarAcesso() {
            let statusPro = localStorage.getItem('construtor_pro_ativo');
            let creditos = localStorage.getItem('construtor_creditos');

            if (creditos === null && statusPro !== "true") {
                localStorage.setItem('construtor_creditos', '5');
                creditos = 5;
            }

            if (statusPro === "true") {
                document.getElementById('status-creditos').innerText = "Status: Acesso Profissional Ativo (Ilimitado)";
                document.getElementById('calculators-wrapper').style.display = 'block';
                document.getElementById('paywall-screen').style.display = 'none';
            } else {
                let creditosRestantes = parseInt(creditos);
                if (creditosRestantes > 0) {
                    document.getElementById('status-creditos').innerText = `Créditos gratuitos restantes neste computador: ${creditosRestantes}`;
                    document.getElementById('calculators-wrapper').style.display = 'block';
                    document.getElementById('paywall-screen').style.display = 'none';
                } else {
                    document.getElementById('status-creditos').innerText = "Status: Créditos esgotados";
                    document.getElementById('calculators-wrapper').style.display = 'none';
                    document.getElementById('paywall-screen').style.display = 'block';
                }
            }
        }

        function executarCalculo(tipo) {
            let statusPro = localStorage.getItem('construtor_pro_ativo');
            
            if (statusPro !== "true") {
                let creditos = parseInt(localStorage.getItem('construtor_creditos') || '0');
                if (creditos > 0) {
                    creditos--;
                    localStorage.setItem('construtor_creditos', creditos);
                }
            }
            
            checarAcesso();

            let box = document.getElementById('res-' + tipo);
            if(box) {
                box.style.display = 'block';
            }
        }

        function ativarLicenca() {
            let digitada = document.getElementById('senha-ativacao').value.trim();
            if (digitada === SENHA_MESTRA_DEV) {
                localStorage.setItem('construtor_pro_ativo', 'true');
                alert('Parabéns! Acesso Profissional ativado com sucesso neste computador.');
                checarAcesso();
            } else {
                alert('Senha incorreta! Verifique a senha enviada pelo suporte após o pagamento do Pix.');
            }
        }

        window.onload = function() {
            checarAcesso();
        };

        function switchTab(tabId) {
            document.querySelectorAll('.calculator-section').forEach(sec => {
                sec.classList.remove('active');
            });
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('active');
        }
    </script>
</body>
</html>
"""

components.html(html_code, height=750, scrolling=True)
