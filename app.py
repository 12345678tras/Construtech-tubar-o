pergunta_lower = prompt_usuario.lower()
                        
                        # Motor de IA inteligente para entender a gíria e o jeito simples do pedreiro
                        # Verificamos blocos, tijolos, paredes ou muros
                        if any(p in pergunta_lower for p in ["tijolo", "bloco", "tijolao", "tijolão", "material", "parede", "muro", "erguer", "levantar", "quantos"]):
                            if any(p in pergunta_lower for p in ["cimento", "argamassa", "reboco", "concreto", "chão", "piso", "contrapiso"]):
                                # Se misturou tijolo e cimento, foca na argamassa
                                resposta_ia = (
                                    "📊 **Quanto vai de cimento para assentar os blocos/tijolos:**\n\n"
                                    "Para cada metro quadrado (m²) de parede, você vai gastar em média **metade de um saco até um saco de cimento** misturado com a areia (dependendo se é vedação ou estrutura). "
                                    "No geral, para cada metro cúbico de argamassa de assentamento, vão cerca de **7 a 8 sacos de cimento**."
                                )
                            else:
                                resposta_ia = (
                                    "🧱 **Quantos blocos ou tijolos gastam por metro quadrado (m²):**\n\n"
                                    "- **Tijolo Baiano / Bloco Cerâmico (9x19x19cm):** Gasta uns **25 tijolos por m²** de parede.\n"
                                    "- **Bloco de Concreto (14x19x39cm):** Gasta uns **12,5 blocos por m²**.\n"
                                    "- **Tijolo Maciço (comum de barro):** Gasta uns **90 a 100 tijolos por m²** (assentado em pé).\n\n"
                                    "*(Dica: Sempre compre **5% a mais** para não faltar por causa de quebra!)*"
                                )

                        # Verificamos cimento, saco, pó, cal, argamassa, piso, contrapiso, reboco
                        elif any(p in pergunta_lower for p in ["cimento", "saco", "sacos", "pó", "po", "argamassa", "reboco", "chapisco", "piso", "contrapiso", "concreto"]):
                            if any(p in pergunta_lower for p in ["piso", "contrapiso", "chão", "calcada", "calçada"]):
                                resposta_ia = (
                                    "🏠 **Cimento para Contrapiso ou Piso:**\n\n"
                                    "Para fazer um contrapiso de 5 cm de grossura, você gasta mais ou menos **1,5 a 2 sacos de cimento para cada 10 metros quadrados (m²)** de piso aplicado."
                                )
                            elif any(p in pergunta_lower for p in ["reboco", "mão", "mão de obra", "parede"]):
                                resposta_ia = (
                                    "🎨 **Cimento para Reboco:**\n\n"
                                    "No reboco (com grossura de 2cm), você gasta em média **4 a 5 kg de cimento por m²** de parede rebocada."
                                )
                            else:
                                resposta_ia = (
                                    "📦 **Contas gerais de cimento na obra:**\n\n"
                                    "- **Assentamento de bloco/tijolo:** Cerca de **5 a 6 kg de cimento** por m² de parede.\n"
                                    "- **Reboco (2cm):** Cerca de **4 a 5 kg de cimento** por m².\n"
                                    "- **Contrapiso (5cm):** Cerca de **1,5 a 2 sacos** para cada 10 m²."
                                )

                        # Verificamos ferro, aço, viga, coluna, estribo, bitola
                        elif any(p in pergunta_lower for p in ["ferro", "aço", "aco", "viga", "coluna", "baldrames", "estribo", "bitola"]):
                            resposta_ia = (
                                "⚙️ **Ferro e Aço (Vigas e Colunas):**\n\n"
                                "Para casas térreas comuns, a média de ferro na estrutura fica em torno de **14 kg de aço por metro quadrado (m²) de construção**.\n"
                                "Sempre use ferro de boa procedência nas colunas e vigas baldrame conforme o projeto do engenheiro!"
                            )

                        # Verificamos água, esgoto, cano, banheiro, pia, cozinha
                        elif any(p in pergunta_lower for p in ["agua", "água", "esgoto", "cano", "tubo", "banheiro", "cozinha", "fossa"]):
                            resposta_ia = (
                                "🚰 **Hidráulica (Canos e Saídas):**\n\n"
                                "- Para **água fria**, o padrão nos ramais é usar cano de **25mm**.\n"
                                "- Para **esgoto** (saída de vaso e pia), use cano de **100mm** para o vaso e **40mm/50mm** para pias e ralos."
                            )

                        # Se falar qualquer outra coisa muito fora ou genérica
                        else:
                            resposta_ia = (
                                f"Falei com o sistema aqui sobre **'{prompt_usuario}'**, mas para não errar na sua conta da obra, "
                                "me diz exato: é para **parede (tijolo/bloco)**, **cimento/argamassa**, **piso**, ou **ferro**? "
                                "Assim eu te passo o número exato na lata!"
                            )
