# Tem Água? - CitizenTech

## Ficha do projeto

- **Nome:** Tem Água?
- **Cidade e bairro:** Cidade simulada no projeto, bairro sem identificação pessoal.
- **Cidadão beneficiado:** Moradores de casas que dependem de caixa d'água em áreas com queda de pressão.
- **Problema:** A falta de água pode chegar sem aviso e o morador não tem registro para mostrar a dificuldade da rua.
- **Como funciona:** O projeto recebe leituras da caixa, calcula volume, nível e autonomia, registra o estado e mostra os resultados no terminal ou na interface web.
- **Python:** Central que valida dados, salva leituras em JSON, calcula métricas e organiza os resultados.
- **Wokwi:** Ambiente usado para simular o envio das leituras em formato JSON.
- **React:** Não foi usado nesta versão. A interface extra foi feita com Streamlit.
- **Matemática:** Converte altura em volume e nível, calcula a autonomia e verifica quanto tempo falta até às 5h.
- **Indicador de impacto:** Número de caixas monitoradas, caixas em atenção ou crítica e ruas com maior incidência.
- **ODS:** ODS 10 - Redução das desigualdades, ODS 11 - Cidades e comunidades sustentáveis e, como complemento, ODS 6 - Água potável e saneamento.

Projeto desenvolvido para o desafio **GS - CitizenTech (FIAP)**.

- Disciplina: Computational Thinking with Python
- Turma: Engenharia de Software - 1ESPV
- Integrantes: Pedro - RM 569307, Renan - RM 569077, Evandro - RM 572473, Raphael de Oliveira - RM 571065

## 1. Relação com os ODS

- **ODS 10 - Redução das desigualdades:** ajuda a mostrar quais ruas têm mais dificuldade de abastecimento e oferece dados que podem apoiar pedidos coletivos.
- **ODS 11 - Cidades e comunidades sustentáveis:** melhora o acompanhamento do consumo e do abastecimento local, ajudando o bairro a lidar melhor com falta de água.
- **ODS 6 - Água potável e saneamento:** traz alertas sobre tampa aberta e água parada, que podem ajudar a cuidar da qualidade da água armazenada.

## 2. O problema

Milhões de residências sofrem com a redução na rede de abastecimento durante a noite, principalmente das 19h às 5h. Como a caixa d'água fica em um ponto alto, o morador só percebe a falta quando a água já acabou e normalmente não tem registros do problema.

## 3. A solução

Um módulo IoT mede a altura da água na caixa e envia leituras em formato JSON. Esta central em Python recebe esses dados e:

- calcula o volume e o nível da caixa;
- calcula a autonomia em horas;
- verifica se a água dura até às 5h conforme a hora da leitura;
- classifica cada caixa como NORMAL, ATENCAO ou CRITICA;
- mostra alertas de qualidade e um resumo por rua.

## 4. Funcionalidades

- Visão geral das caixas no terminal e na web.
- Importação de arquivo JSON no terminal e na web.
- Registro manual no terminal e na web.
- Alertas de tampa aberta, água parada e alertas enviados no JSON.
- Histórico de leituras na web.
- Ranking e mapa coletivo de ruas no terminal e na web.
- Salvamento automático das leituras em leituras.json.

## 5. Modos de execução

O modo terminal é a entrega principal deste projeto. Ele foi feito somente com Python puro e usa a biblioteca padrão.

O modo web com Streamlit é um extra. Ele facilita a visualização em tabelas e gráficos, mas exige a instalação das bibliotecas de requirements.txt.

## 6. Regras de cálculo

- Volume (L) = área da base (m²) × altura da água (m) × 1000
- Nível (%) = altura da água (m) ÷ altura da caixa (m) × 100
- Autonomia (h) = quantidade atual (L) ÷ consumo médio (L/h)
- Horas até às 5h = (5 - hora da leitura) % 24
- Dura até às 5h = autonomia maior ou igual às horas calculadas

| Estado | Condição |
|---|---|
| CRITICA | autonomia de 3h ou menos, ou nível de 10% ou menos |
| ATENCAO | autonomia menor que 12h, ou a água não dura até às 5h |
| NORMAL | nenhuma das condições acima |

Os limites estão definidos em metricas.py.

## 7. Como executar

1. Para o modo principal, instale apenas o Python.
2. Execute `python main.py`.
3. Escolha a opção 1 para usar o terminal.
4. Para o modo web , instale as dependências com `pip install -r requirements.txt` e escolha a opção 2 no menu.

## 8. Formato do JSON aceito

O arquivo pode conter um objeto ou uma lista de objetos. Os campos numéricos nivel_pct, volume_l, taxa_lh e autonomia_h precisam ser números. O estado precisa ser NORMAL, ATENCAO ou CRITICA.

Campos obrigatórios:

- casa
- caixa
- rua_id
- nivel_pct
- volume_l
- taxa_lh
- autonomia_h
- estado

Os demais campos recebem valores padrão.

Exemplo:

```json
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
```

Na importação, a autonomia e a hora da leitura são usadas para recalcular ate_5h e estado.

## 9. Persistência de dados

As leituras são salvas em leituras.json após importar um JSON ou registrar uma leitura manual. Na primeira execução, o arquivo é criado com dados simulados. Quando o arquivo tem registros ruins, o sistema ignora apenas esses registros e avisa quantos foram descartados.

Os dados são simulados e não representam pessoas reais. Não existem dados pessoais reais neste projeto.

## 10. Limitações

- Não existe conexão em tempo real com um ESP32 nesta entrega.
- O volume considera uma caixa com área de base fixa de 1 m².
- O mapa da web é uma tabela e um gráfico por rua, não um mapa geográfico.
- A detecção automática de faltas ainda não foi implementada; a tela web mostra o histórico de leituras.
