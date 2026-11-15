# Tem Água? 

Projeto desenvolvido para o desafio **GS - CitizenTech (FIAP)**.

- Disciplina: Computational Thinking with Python
- Turma: Engenharia de Software - 1SPV
- Integrantes:  Pedro - RM 569307, Renan - RM 569077, Evandro - RM 572473, Raphael de Oliveira- RM 571065

## 1. O problema

Milhões de residências sofrem com a redução na rede de abastecimento durante a noite (das 19h às 5h). Como a caixa d'água fica na laje, o morador só percebe a falta quando a água já acabou, e não existe nenhum registro que comprove o problema para o bairro.

## 2. A solução

Um módulo IoT mede o nível da água na caixa e envia leituras em formato JSON. Esta **central em Python** recebe esses dados e:

- calcula o volume e a autonomia em horas (se a água dura até as 5h da manhã);
- classifica cada caixa como NORMAL, ATENCAO ou CRITICA;
- alerta sobre qualidade da água (tampa aberta ou água parada por muitas horas);
- gera um mapa coletivo por rua, com dados anônimos, que serve de evidência sobre os moradores.

## 3. Funcionalidades

- Visão geral das caixas, com indicadores e gráficos: Terminal e Web
- Importar leituras de arquivo JSON (Wokwi): Terminal e Web (apenas texto colado na web)
- Registrar leitura manualmente: Terminal e Web
- Alertas de qualidade da água: Terminal e Web
- Histórico de faltas: Web
- Ranking / mapa coletivo de ruas: Terminal e Web
- Salvar e carregar dados automaticamente: Terminal e Web

## 4. Regras de cálculo

- Volume (L) = área da base (m²) × altura da água (m) × 1000
- Autonomia (h) = quantidade atual (L) ÷ consumo médio (L/h)
- Dura até as 5h? = autonomia maior ou igual a 10 horas (tempo entre 19h e 5h)

| Estado  | Condição                                                  |
| CRITICA | autonomia de 3h ou menos, **ou** nível de 10% ou menos    |
| ATENCAO | autonomia menor que 12h, **ou** a água não dura até as 5h |
| NORMAL  | nenhuma das condições acima                               |

Todos esses limites estão definidos como constantes em metricas.py.

## 6. Como executar

1. Instale as dependências (necessário apenas para o modo web):
    pip install -r requirements.txt

2. Execute o projeto:
    python main.py

3. Escolha o modo no menu: (1) para o terminal ou (2) para a interface web.

O modo terminal usa apenas a biblioteca padrão do Python e funciona sem instalar nada.

## 7. Formato do JSON aceito

O arquivo pode ter um objeto ou uma lista de objetos. Campos obrigatórios: casa, caixa, rua_id, nivel_pct, volume_l, taxa_lh, autonomia_h e estado. Os demais campos recebem valores padrão se não forem enviados.

Teste com:

{
    "casa": "c10",
    "caixa": "cx-1",
    "rua_id": "r15",
    "nivel_pct": 45,
    "volume_l": 450,
    "taxa_lh": 25,
    "autonomia_h": 18,
    "estado": "NORMAL"
}

## 8. Persistência de dados

As leituras são salvas automaticamente em leituras.json sempre que o usuário importa um JSON ou registra uma leitura manual, nos dois modos. Na primeira execução, o arquivo é criado com dados simulados. Se o arquivo estiver corrompido, o sistema volta para a base inicial em vez de travar.


## 11. Limitações

- Os dados vêm de arquivos JSON simulados, sem conexão em tempo real com o ESP32.
- O volume considera uma caixa com área de base fixa (1 m²).
- O "mapa" é uma tabela com gráfico por rua, sem mapa geográfico.
