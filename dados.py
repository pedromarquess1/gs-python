import json
import os
from datetime import datetime
from metricas import (
    calcular_autonomia_horas,
    classificar_estado_caixa,
    verificar_dura_ate_5h,
)

ARQUIVO_DADOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leituras.json")
CAMPOS_OBRIGATORIOS = ("casa", "caixa", "rua_id", "nivel_pct", "volume_l", "taxa_lh", "autonomia_h", "estado")

def obter_dados_iniciais():
    return [
        {
            "casa": "c07",
            "caixa": "cx-1",
            "rua_id": "r12",
            "ts": "2026-11-12T17:00:00",
            "nivel_pct": 25.0,
            "volume_l": 250.0,
            "taxa_lh": 41.0,
            "autonomia_h": 6.6,
            "ate_5h": False,
            "temp_agua": 24.5,
            "tampa": "FECHADA",
            "idade_agua_h": 9.5,
            "estado": "ATENCAO",
            "alertas": ["SEM_ENTRADA"]
        },
        {
            "casa": "c03",
            "caixa": "cx-1",
            "rua_id": "r05",
            "ts": "2026-11-12T17:05:00",
            "nivel_pct": 80.0,
            "volume_l": 800.0,
            "taxa_lh": 15.0,
            "autonomia_h": 53.3,
            "ate_5h": True,
            "temp_agua": 22.0,
            "tampa": "FECHADA",
            "idade_agua_h": 4.0,
            "estado": "NORMAL",
            "alertas": []
        }
    ]


def validar_e_extrair_json_agua(conteudo_str):
    try:
        dados_carregados = json.loads(conteudo_str)

        if isinstance(dados_carregados, dict):
            dados_carregados = [dados_carregados]
        elif not isinstance(dados_carregados, list):
            return False, [], "Formato inválido: o JSON precisa ser um objeto ou lista."

        registros_validos = []
        descartados = 0
        for idx, item in enumerate(dados_carregados):
            if not isinstance(item, dict):
                descartados += 1
                continue

            faltantes = [c for c in CAMPOS_OBRIGATORIOS if c not in item]
            if faltantes:
                descartados += 1
                continue

            campos_invalidos = []
            for campo in ("nivel_pct", "volume_l", "taxa_lh", "autonomia_h"):
                valor = item[campo]
                if isinstance(valor, bool) or not isinstance(valor, (int, float)):
                    campos_invalidos.append(campo)
            if campos_invalidos or item["estado"] not in ("NORMAL", "ATENCAO", "CRITICA"):
                descartados += 1
                continue

            item.setdefault("ts", "2026-11-15T12:00:00")
            item.setdefault("temp_agua", 23.0)
            item.setdefault("tampa", "FECHADA")
            item.setdefault("idade_agua_h", 5.0)
            item.setdefault("alertas", [])

            try:
                hora = datetime.fromisoformat(str(item["ts"])).hour
            except (TypeError, ValueError):
                hora = 12

            item["ate_5h"] = verificar_dura_ate_5h(float(item["autonomia_h"]), hora)
            item["estado"] = classificar_estado_caixa(
                float(item["autonomia_h"]),
                float(item["nivel_pct"]),
                item["ate_5h"],
            )
            registros_validos.append(item)

        mensagem = f"{len(registros_validos)} registro(s) importado(s) com sucesso!"
        if descartados:
            mensagem += f" {descartados} registro(s) inválido(s) descartado(s)."
        return True, registros_validos, mensagem

    except json.JSONDecodeError as e:
        return False, [], f"Erro na sintaxe do JSON: {e}"
    except Exception as e:
        return False, [], f"Erro inesperado: {e}"


def salvar_leituras(leituras, caminho=ARQUIVO_DADOS):
    try:
        with open(caminho, "w", encoding="utf-8") as arq:
            json.dump(leituras, arq, ensure_ascii=False, indent=2)
        return True
    except (OSError, TypeError):
        return False


def carregar_leituras(caminho=ARQUIVO_DADOS):
    if not os.path.exists(caminho):
        leituras = obter_dados_iniciais()
        salvar_leituras(leituras, caminho)
        return leituras

    try:
        with open(caminho, "r", encoding="utf-8") as arq:
            conteudo = arq.read()
    except OSError:
        return obter_dados_iniciais()

    sucesso, registros, mensagem = validar_e_extrair_json_agua(conteudo)
    if sucesso:
        if "descartado" in mensagem:
            print(f"[AVISO] {mensagem}")
        return registros
    return obter_dados_iniciais()


def obter_leituras_por_caixa(leituras):
    mais_recentes = {}
    for item in leituras:
        chave = (item.get("casa"), item.get("caixa"))
        ts = str(item.get("ts", ""))
        if chave not in mais_recentes or ts > str(mais_recentes[chave].get("ts", "")):
            mais_recentes[chave] = item
    return list(mais_recentes.values())