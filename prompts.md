# Registro de Uso da IA

Projeto: Tem Água? - Central de Monitoramento e Abastecimento

Disciplina: Computational Thinking with Python

Turma: Engenharia de Software - 1ESPV

Este arquivo registra como a IA ajudou no projeto.

## 1. Ferramentas usadas

- Google Gemini e Claude.
- Elas ajudaram na organização do projeto, nos cálculos e na interface.

## 2. Prompts usados

### 2.1. Cálculos matemáticos

- Prompt: "Quais cálculos matemáticos posso usar para calcular o volume, a autonomia e o estado da caixa d'água?"
- Resposta usada: volume pela altura, autonomia pela divisão do volume pelo consumo e estado pelas faixas de autonomia e nível.

### 2.2. Organização do projeto

- Prompt: "Como separar as regras de cálculo, a leitura de JSON e o terminal em módulos diferentes?"
- Resposta usada: o grupo separou os arquivos em main, cli, dados e metricas, com as telas em views.

### 2.3. Interface web

- Prompt: "Como mostrar os dados em tabelas e gráficos no Streamlit?"
- Resposta usada: usar DataFrame, gráficos simples e colunas para organizar cada informação.

### 2.4. Revisão dos requisitos

- Prompt: "Revise o projeto inteiro com base nos critérios da disciplina e indique desvios."
- Resposta usada: conferir persistência, JSON, cálculos, interface, documentação e modo terminal.

### 2.5. Correções finais

- Prompt: "Ajuste validação do terminal e JSON, regras até às 5h, contagem por caixa, alertas da web e documentação. Mantenha o modo terminal como entrega principal e uma escrita simples de estudante de engenharia de software."

- Ajustes feitos:
  - Validação de nível, altura da caixa, altura da água e consumo no terminal.
  - Validação dos campos numéricos e do estado ao importar JSON.
  - Cálculo do nível a partir da altura.
  - Cálculo das horas até às 5h usando a hora da leitura.
  - Recalculo de ate_5h e estado durante a importação.
  - Contagem da leitura mais recente por casa e caixa.
  - Alertas da web alinhados com os alertas do terminal.
  - Texto do Registro de Faltas trocado por Histórico de Leituras.
  - Atualização do README, da turma e da documentação dos dados simulados.

## 3. Análise crítica

O projeto ficou mais organizado depois da separação dos módulos e dos cálculos. A IA também ajudou a enxergar pontos que poderiam falhar em uma leitura JSON.

Um exemplo encontrado foi aceitar "45" como texto em um campo que deveria ser número. Isso podia deixar o dado salvo, mas quebrava a tela de visão geral. Agora esse registro pode ser rejeitado ou descartado, conforme o contexto.

Outro ponto é que a detecção automática de falta ainda não foi implementada. Por isso a tela web é chamada de Histórico de Leituras.
