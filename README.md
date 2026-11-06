# Agente de IA — Data Quality

<h2 align="center">AI-Powered Data Quality Analysis & Validation</h2>

<p align="center">
  Data Quality · Python · AI Agents · Data Validation · Human-in-the-Loop
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue" alt="Python 3.12">
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458" alt="Pandas">
  <img src="https://img.shields.io/badge/Groq-LLM-orange" alt="Groq">
  <img src="https://img.shields.io/badge/Data%20Quality-Validation-green" alt="Data Quality">
  <img src="https://img.shields.io/badge/AI-Human--in--the--Loop-purple" alt="Human in the Loop">
</p>

---

## 1. Visão geral

O **Agente de IA — Data Quality** é um projeto de análise e validação da qualidade de dados que combina regras determinísticas, processamento com Python e Pandas e inteligência artificial generativa.

O objetivo é transformar verificações técnicas em informações estruturadas, recomendações de tratamento e insights que apoiem a tomada de decisão.

A solução utiliza a API Groq para interpretar resultados e auxiliar na elaboração de recomendações, mantendo a validação técnica e a aprovação das ações sob responsabilidade humana.

## 2. Problema de negócio

Dados inconsistentes, incompletos ou inválidos comprometem análises, indicadores e decisões.

Em processos de Data Quality, a identificação de problemas pode exigir verificações manuais e interpretação de múltiplas regras.

Este projeto explora como a combinação de validações tradicionais e IA pode:

- Identificar problemas de qualidade de dados.
- Organizar resultados de forma estruturada.
- Interpretar ocorrências e possíveis impactos.
- Sugerir ações de tratamento.
- Apoiar a análise sem substituir a decisão humana.

## 3. Objetivos do projeto

- Desenvolver um agente de IA aplicado à qualidade de dados.
- Automatizar verificações de consistência e validade.
- Identificar problemas em bases de clientes.
- Gerar recomendações contextualizadas.
- Implementar validação da interpretação produzida pela IA.
- Aplicar princípios de governança, segurança e supervisão humana.

## 4. Dataset

O projeto utiliza uma **base sintética de clientes**, criada para testes e validação do agente.

| Característica | Descrição |
|---|---|
| Tipo de projeto | Agente de IA aplicado a Data Quality |
| Segmento | Data Analytics e Inteligência Artificial |
| Formato de origem | CSV |
| Dataset de teste | Base sintética de clientes |
| Volume analisado | 10.000 registros |
| Estrutura | 4 colunas |
| Processamento | Python e Pandas |

### Campos analisados

- `id_cliente`
- `nome`
- `idade`
- `email`

A base contém ocorrências intencionalmente inseridas para simular problemas encontrados em cenários reais de qualidade de dados.

## 5. Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Desenvolvimento e execução do agente |
| Pandas | Manipulação e análise de dados |
| Groq API | Interpretação e geração de recomendações por IA |
| GPT-OSS-20B | Modelo utilizado na integração com Groq |
| CSV | Fonte de dados |
| Pytest | Testes automatizados |
| dotenv | Gerenciamento de variáveis de ambiente |

## 6. Metodologia

O fluxo de processamento foi estruturado em etapas:

1. Recepção da base de dados.
2. Análise inicial e profiling.
3. Aplicação de regras de qualidade.
4. Identificação e consolidação de ocorrências.
5. Interpretação dos resultados pela IA.
6. Geração de recomendações.
7. Validação da interpretação.
8. Revisão e aprovação humana das ações sugeridas.

### Dimensões de qualidade avaliadas

- Completude: identificação de valores ausentes.
- Unicidade: identificação de registros duplicados.
- Validade: verificação de formatos e valores permitidos.
- Consistência: análise de regras e restrições.
- Integridade: avaliação de condições relacionadas aos dados.

## 7. Arquitetura do projeto

A solução separa a análise determinística, a interpretação por IA e a validação das recomendações.

```text
CSV
 │
 ▼
Data Profiling
 │
 ▼
Data Quality Rules
 │
 ▼
Consolidação das ocorrências
 │
 ▼
Agente de IA — Groq
 │
 ▼
Interpretação e recomendações
 │
 ▼
Validação da interpretação
 │
 ▼
Revisão humana
```

A IA atua como componente de apoio analítico, não como autoridade final sobre a qualidade dos dados.

## 8. Resultados da validação

A execução de validação do dataset de 10.000 registros apresentou os seguintes resultados:

| Indicador | Resultado |
|---|---:|
| Registros analisados | 10.000 |
| Colunas | 4 |
| Células com valores ausentes | 149 |
| Registros envolvidos em IDs duplicados | 60 |
| E-mails inválidos | 80 |
| Idades fora do intervalo esperado | 7 |
| Regras violadas | 3 |
| Ocorrências de regras | 147 |
| Recomendações / ações sugeridas | 3 |
| Ações pendentes de aprovação | 3 |
| Alertas na validação da interpretação | 0 |

**Status da validação inicial:** aprovada.

As recomendações geradas permanecem pendentes de aprovação humana, conforme a abordagem Human-in-the-Loop.

## 9. Data Quality e inteligência artificial

O projeto diferencia responsabilidades técnicas e atividades apoiadas por IA.

| Etapa | Responsabilidade |
|---|---|
| Identificação de problemas | Regras determinísticas e Python |
| Processamento dos dados | Pandas |
| Interpretação contextual | IA generativa |
| Recomendações | IA com base nos resultados |
| Validação | Código e critérios definidos |
| Aprovação de tratamento | Responsabilidade humana |

A IA acelera a interpretação e a comunicação dos resultados, mas não substitui as regras de qualidade, a validação técnica ou a análise do profissional.

## 10. Segurança e governança

O projeto adota princípios de segurança e supervisão:

- Chaves de API armazenadas em variáveis de ambiente.
- Credenciais não incluídas no código-fonte.
- Arquivo `.env` protegido pelo `.gitignore`.
- Recomendações submetidas à aprovação humana.
- Separação entre identificação técnica e interpretação por IA.
- Validação das respostas produzidas pelo modelo.

A utilização de IA exige atenção à segurança, à rastreabilidade e à confiabilidade das recomendações.

## 11. Estrutura do repositório

```text
Agente_IA_DataQuality_Groq/
├── 01_data/
├── 02_logs/
│   └── .gitkeep
├── 03_reports/
│   └── .gitkeep
├── 04_documentacao/
│   └── VALIDACAO_TESTE_VOLUME_AGENTE_IA_DATA_QUALITY.md
├── src/
│   ├── data_quality.py
│   ├── main.py
│   ├── regras_qualidade.py
│   ├── plano_tratamento.py
│   └── validar_interpretacao.py
├── tests/
├── gerar_dataset_teste.py
├── requirements.txt
├── .gitignore
└── README.md
```

Os relatórios e logs gerados durante a execução são armazenados localmente e não são publicados no repositório.

## 12. Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/rrleone/Agente_IA_DataQuality_Groq.git
cd Agente_IA_DataQuality_Groq
```

### 2. Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar a API Groq

Configure a variável de ambiente `GROQ_API_KEY` com sua chave pessoal.

```bash
export GROQ_API_KEY="sua_chave_groq"
```

Substitua `sua_chave_groq` pela sua chave pessoal obtida na Groq.

Nunca publique sua chave de API no código ou no repositório.

### 5. Executar o agente

```bash
python src/main.py
```

## 13. Testes e validação

O projeto inclui testes automatizados para verificar componentes e comportamentos da solução.

Para executar os testes:

```bash
pytest
```

Os testes contribuem para a confiabilidade do processamento e para a validação das funcionalidades implementadas.

## 14. Uso responsável da IA

A IA generativa pode produzir interpretações incompletas ou incorretas.

Por isso, a solução considera:

- Validação das respostas.
- Conferência das recomendações.
- Supervisão humana.
- Separação entre regras técnicas e interpretação generativa.
- Não execução automática de ações críticas sem aprovação.

O uso da IA é tratado como apoio ao profissional de dados, mantendo a responsabilidade analítica e decisória sob controle humano.

## 15. Possíveis evoluções

- Interface para acompanhamento das análises.
- Histórico de execuções e recomendações.
- Monitoramento contínuo da qualidade.
- Ampliação das regras de Data Quality.
- Integração com bancos de dados.
- Geração de relatórios estruturados.
- Comparação de resultados entre execuções.
- Implementação de indicadores de qualidade.
- Integração com pipelines de ETL.

## 16. Conclusão

O projeto demonstra como Python, Pandas e inteligência artificial generativa podem ser combinados para apoiar processos de Data Quality.

A solução evidencia a importância de integrar automação, validação técnica, interpretação contextual e supervisão humana.

Mais do que identificar inconsistências, o objetivo é transformar ocorrências de qualidade de dados em informações compreensíveis e recomendações que apoiem decisões mais confiáveis.

---

## Autor

**Renato Leone**

Analista de Dados | Business Intelligence

Dados • Análise • Insights • Decisões

GitHub: [github.com/rrleone](https://github.com/rrleone)

Portfólio: [renatoleone](https://www.renatoleone.com.br)
