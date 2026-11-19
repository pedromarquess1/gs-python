LIMITES_AUTONOMIA_H = (12.0, 3.0)  # 12h para Atenção, 3h para Crítica
JANELA_PRESSAO_RUA = (19, 5)       # Horário crítico de queda de pressão (19h às 5h)

AUTONOMIA_MINIMA_ATE_5H = 10.0   
NIVEL_CRITICO_PCT = 10.0         
IDADE_MAXIMA_AGUA_H = 48.0       
AREA_BASE_PADRAO_M2 = 1.0        
LITROS_POR_M3 = 1000.0           
CONSUMO_AUSENTE_AUTONOMIA_H = 99.9  


def calcular_volume_litros(altura_agua_m, area_base_m2=AREA_BASE_PADRAO_M2):
    # V = A * h, convertido para litros
    try:
        volume_m3 = area_base_m2 * max(0.0, altura_agua_m)
        return round(volume_m3 * LITROS_POR_M3, 1)
    except (TypeError, ValueError):
        return 0.0


def calcular_autonomia_horas(volume_atual_litros, consumo_medio_lh):
    # Calcula quantas horas a água vai durar com base no consumo médio
    try:
        if consumo_medio_lh <= 0:
            return CONSUMO_AUSENTE_AUTONOMIA_H
        return round(volume_atual_litros / consumo_medio_lh, 1)
    except (TypeError, ValueError):
        return 0.0


def calcular_nivel_pct(altura_agua_m, altura_caixa_m):
    try:
        if altura_caixa_m <= 0:
            return 0.0
        nivel = (altura_agua_m / altura_caixa_m) * 100.0
        return round(max(0.0, min(100.0, nivel)), 1)
    except (TypeError, ValueError):
        return 0.0


def calcular_horas_ate_5h(hora):
    hora_fim_pressao = JANELA_PRESSAO_RUA[1]
    return (hora_fim_pressao - hora) % 24


def verificar_dura_ate_5h(autonomia_h, hora):
    horas_faltantes = calcular_horas_ate_5h(hora)
    return autonomia_h >= horas_faltantes


def classificar_estado_caixa(autonomia_h, nivel_pct, ate_5h_ok):
    # Define se a situação é normal, atenção ou crítica
    if autonomia_h <= LIMITES_AUTONOMIA_H[1] or nivel_pct <= NIVEL_CRITICO_PCT:
        return "CRITICA"
    elif autonomia_h < LIMITES_AUTONOMIA_H[0] or not ate_5h_ok:
        return "ATENCAO"
    else:
        return "NORMAL"