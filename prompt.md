# Registro de Uso da IA (`prompts.md`)

Projeto: Tem Água? — Central de Monitoramento e Abastecimento  
Disciplina: Computational Thinking with Python
Turma: Engenharia de Software - 1SPV

Este arquivo documenta o uso de ferramentas de Inteligência Artificial como auxílio no desenvolvimento e estruturação do projeto, conforme as diretrizes da disciplina.

### 1. Ferramenta Utilizada e Finalidade

- Ferramenta: Google Gemini e Claude (IA Generativa).

- Finalidade: Apoio para validação de lógica em Python, mapeamento de métricas matemáticas e sugestões de estruturação de interface em Streamlit.

### 2. Histórico de Prompts e Respostas

#### 2.1. Métricas e Cálculos Matemáticos

- Prompt: "Quais cálculos matemáticos posso levar em consideração para construir as métricas de quantidade e autonomia da caixa d'água?"

- Resumo da Resposta: Definição de três cálculos principais: conversão de altura da coluna d'água em quantidade (V = A x h x 1000), estimativa de autonomia em horas dividindo a quantidade atual pela taxa média de consumo (L/h), e classificação de estados considerando a janela noturna de redução de pressão (19h às 5h).

#### 2.2. Projeto Duplo (Terminal vs. Web)

- Prompt: "Seria viável fazer um projeto separado para rodar tanto pelo terminal quanto por web pela biblioteca do streamlit?"

- Resumo da Resposta: Sim. A recomendação foi aplicar a separação de responsabilidades, isolando as regras de negócio e a leitura de JSON para que tanto o menu do terminal quanto a interface web utilizassem as mesmas funções sem duplicação de código.

#### 2.3. Estilização e Visualização no Streamlit

- Prompt: "Como posso estilizar melhor as tabelas e os gráficos no streamlit para facilitar a leitura dos dados?"*

- Resumo da Resposta: Sugestão do uso de (column_config) para renomear colunas e adicionar barras de progresso diretamente nas tabelas, além da adoção da biblioteca Altair (dependência do streamlit) para construir gráficos com cores por nível de status (Normal, Atenção e Crítica).

### 2.4. Revisão do projeto com base nos critérios da disciplina (Claude)

- Prompt: "Revise o projeto inteiro e veja se há algum desvio com o tema da matéria" (com os slides da disciplina e todos os arquivos do projeto anexados)

- Resumo da resposta: a IA disse que o projeto estava quase 100% de acordo com o tema, e apontou os 
pontos de melhoria: ausência de persistência dos dados, alertou para criar um requirements.txt

### 3. Funcionalidades Desenvolvidas com Auxílio da IA

- A estrutura do código (separação em main, cli, dados, metricas e a pasta views/).
- A lógica de validação de dados JSON simulando os envios do ESP32/Wokwi.
- A formatação visual dos componentes e tabelas no painel web.

### 4. Verificação, Testes e Ajustes

- Testes de Execução: O grupo executou o código localmente tanto no modo Terminal (garantindo o funcionamento do Python puro) quanto no modo Web (Streamlit).

- Ajustes: Validação manual dos dados retornados pelas funções matemáticas comparando com os valores esperados para garantir que as regras de autonomia da caixa d'água estivessem corretas.

### 5. Análise Crítica

- Benefícios: Agilidade na estruturação inicial do projeto, boas práticas de organização de pastas e clareza na aplicação das fórmulas matemáticas propostas no desafio.

- Limitações e Dificuldades: A IA forneceu modelos genéricos que precisaram ser adaptados manualmente pelo grupo para atender estritamente aos requisitos específicos da disciplina.

Ex: A ilustração dos dados sempre vinham bagunçadas e tivemos que adaptar para ficar visualmente claro de entender