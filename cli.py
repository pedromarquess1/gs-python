import os
import datetime
from dados import carregar_leituras, salvar_leituras, validar_e_extrair_json_agua
from metricas import (
    calcular_volume_litros, calcular_autonomia_horas, classificar_estado_caixa,
    AUTONOMIA_MINIMA_ATE_5H, IDADE_MAXIMA_AGUA_H,
)


def limpar_tela():
    """Limpa o terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def pausar_retorno():
    """Aguarda o usuario pressionar Enter antes de redesenhar o menu principal."""
    input("\nPressione ENTER para voltar ao menu...")


def obter_criticas(par_rua):
    """Recebe um par (rua, dados) e devolve a quantidade de caixas criticas, usada para ordenar o ranking."""
    return par_rua[1]["criticas"]


def exibir_explicacao_projeto():
    print("=" * 65)
    print("SOBRE O PROJETO: TEM AGUA? (GS CITIZENTECH)")
    print("=" * 65)
    print("- PROBLEMA: Milhoes de residencias sofrem com a reducao noturna")
    print("  de pressao na rede (das 19h as 5h). Como a caixa d'agua fica")
    print("  na laje, a falta pega o morador de surpresa e sem registros.")
    print("\n- SOLUCAO: Um modulo IoT (ESP32 + sensor ultrassonico HC-SR04 + RTC)")
    print("  mede o nivel da agua, calcula a autonomia em horas ate as 5h")
    print("  da manha e detecta problemas como tampa aberta ou agua parada.")
    print("\n- CENTRAL PYTHON: Consolida os dados JSON enviados pelo hardware,")
    print("  calcula metricas de autonomia e gera um ranking das ruas mais")
    print("  afetadas para servir de evidencia coletiva do bairro.")
    print("=" * 65)


def executar_cli():
    leituras = carregar_leituras()

    while True:
        limpar_tela()
        print("-" * 55)
        print("TEM AGUA? | CENTRAL DO BAIRRO (TERMINAL)")
        print("-" * 55)
        print("1 - Visao Geral das Caixas d'Agua")
        print("2 - Importar Leituras de Arquivo JSON (Wokwi)")
        print("3 - Registrar Leitura Manualmente")
        print("4 - Alertas de Qualidade (Tampa Aberta / Agua Parada)")
        print("5 - Ranking de Ruas (Mapa Coletivo de Faltas)")
        print("6 - Explicacao do Projeto")
        print("0 - Sair")
        print("-" * 55)

        opcao = input("Escolha uma opcao: ").strip()
        limpar_tela()

        match opcao:
            case "1":
                print("--- PAINEL GERAL DE CAIXAS ---\n")
                if not leituras:
                    print("Nenhuma leitura registrada no momento.")
                else:
                    for item in leituras:
                        status_5h = "Sim" if item["ate_5h"] else "NAO"
                        print(
                            f"[{item['estado']:8}] Casa: {item['casa']} | Rua: {item['rua_id']} | "
                            f"Nivel: {item['nivel_pct']}% ({item['volume_l']} L) | "
                            f"Autonomia: {item['autonomia_h']}h | Dura ate 5h: {status_5h}"
                        )
                pausar_retorno()

            case "2":
                print("--- IMPORTAR LEITURAS JSON (WOKWI) ---\n")
                caminho = input("Digite o caminho do arquivo .json: ").strip()
                try:
                    with open(caminho, "r", encoding="utf-8") as arq:
                        conteudo = arq.read()
                    sucesso, novos, msg = validar_e_extrair_json_agua(conteudo)
                    if sucesso:
                        leituras.extend(novos)
                        print(f"\n[OK] {msg}")
                        if not salvar_leituras(leituras):
                            print("[AVISO] Nao foi possivel gravar no arquivo leituras.json.")
                    else:
                        print(f"\n[ERRO] {msg}")
                except FileNotFoundError:
                    print("\n[ERRO] Arquivo nao encontrado. Verifique o caminho informado.")
                except Exception as e:
                    print(f"\n[ERRO] Falha ao ler o arquivo: {e}")
                pausar_retorno()

            case "3":
                print("--- REGISTRAR LEITURA MANUAL ---\n")
                try:
                    casa = input("Codigo da casa (ex: c07): ").strip() or "c07"
                    caixa = input("ID da caixa (ex: cx-1): ").strip() or "cx-1"
                    rua = input("ID da rua (ex: r12): ").strip() or "r12"
                    nivel = float(input("Nivel percentual (%) [ex: 60.0]: "))
                    altura = float(input("Altura da agua em metros (ex: 0.6): "))
                    taxa = float(input("Consumo medio (L/h) [ex: 20.0]: "))

                    volume = calcular_volume_litros(altura)
                    autonomia = calcular_autonomia_horas(volume, taxa)
                    ate_5h = autonomia >= AUTONOMIA_MINIMA_ATE_5H
                    estado = classificar_estado_caixa(autonomia, nivel, ate_5h)

                    leituras.append({
                        "casa": casa,
                        "caixa": caixa,
                        "rua_id": rua,
                        "ts": datetime.datetime.now().isoformat(),
                        "nivel_pct": nivel,
                        "volume_l": volume,
                        "taxa_lh": taxa,
                        "autonomia_h": autonomia,
                        "ate_5h": ate_5h,
                        "temp_agua": 24.0,
                        "tampa": "FECHADA",
                        "idade_agua_h": 6.0,
                        "estado": estado,
                        "alertas": []
                    })
                    print(f"\n[OK] Leitura salva! Estado: {estado} | Autonomia: {autonomia}h")
                    if not salvar_leituras(leituras):
                        print("[AVISO] Nao foi possivel gravar no arquivo leituras.json.")
                except ValueError:
                    print("\n[ERRO] Entrada invalida. Digite apenas numeros nos campos numericos.")
                pausar_retorno()

            case "4":
                print("--- ALERTAS DE QUALIDADE DA AGUA ---\n")
                encontrou = False
                for item in leituras:
                    if item.get("tampa") == "ABERTA" or item.get("idade_agua_h", 0) > IDADE_MAXIMA_AGUA_H or item.get("alertas"):
                        encontrou = True
                        print(
                            f"[ALERTA] Casa: {item['casa']} | Tampa: {item['tampa']} | "
                            f"Idade da Agua: {item['idade_agua_h']}h | Ocorrencias: {item['alertas']}"
                        )
                if not encontrou:
                    print("[OK] Nenhuma irregularidade de qualidade detectada.")
                pausar_retorno()

            case "5":
                print("--- RANKING DE RUAS (MAIOR CRITICIDADE) ---\n")
                ruas_resumo = {}
                for item in leituras:
                    r = item["rua_id"]
                    if r not in ruas_resumo:
                        ruas_resumo[r] = {"caixas": 0, "criticas": 0}
                    ruas_resumo[r]["caixas"] += 1
                    if item["estado"] in ["CRITICA", "ATENCAO"]:
                        ruas_resumo[r]["criticas"] += 1

                ranking = sorted(ruas_resumo.items(), key=obter_criticas, reverse=True)
                for pos, (rua, dados) in enumerate(ranking, start=1):
                    print(
                        f"{pos}o. Rua {rua} -> Caixas monitoradas: {dados['caixas']} | "
                        f"Caixas em Alerta/Critica: {dados['criticas']}"
                    )
                pausar_retorno()

            case "6":
                exibir_explicacao_projeto()
                pausar_retorno()

            case "0":
                print("Encerrando a Central de Abastecimento. Ate logo!")
                break

            case _:
                print("[AVISO] Opcao invalida. Tente novamente.")
                pausar_retorno()