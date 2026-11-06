
<h1 align="center">Agente de IA — Data Quality</h1>

<h2 align="center">AI-Powered Data Quality Analysis &amp; Validation</h2>

<p align="center">
  Data Quality · Python · AI Agents · Data Validation · Human-in-the-Loop
</p>

<p align="center">
  <img src="https://img.shields.io/badge/PYTHON-3776AB?style=flat&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/PANDAS-150458?style=flat&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/GROQ_API-F55036?style=flat&logoColor=white" />
  <img src="https://img.shields.io/badge/GPT--OSS--20B-412991?style=flat&logoColor=white" />
  <img src="https://img.shields.io/badge/PYTEST-2676B8?style=flat&logo=pytest&logoColor=white" />
  <img src="https://img.shields.io/badge/JSON-34495E?style=flat&logo=json&logoColor=white" />
  <img src="https://img.shields.io/badge/GIT%20%2F%20GITHUB-24292F?style=flat&logo=github&logoColor=white" />
</p>

<p align="center">
  <strong>Transformando inconsistências em dados confiáveis, análises estruturadas e decisões orientadas por qualidade.</strong>
</p>

---

## Visão Executiva

O **Agente de IA — Data Quality** é um projeto de desenvolvimento de uma solução inteligente aplicada à análise, identificação e interpretação de problemas de qualidade de dados.

A solução combina processamento técnico com Python, validação de regras de negócio e Inteligência Artificial generativa utilizando a API da Groq e o modelo GPT-OSS-20B.

O agente analisa conjuntos de dados, identifica inconsistências, estrutura recomendações de tratamento e utiliza IA para transformar resultados técnicos em informações organizadas e compreensíveis.

A arquitetura incorpora uma etapa de validação da interpretação gerada pela IA, buscando assegurar consistência entre os resultados da análise técnica e as conclusões apresentadas.

Mais do que identificar problemas, o projeto explora como agentes de IA podem apoiar processos de Data Quality, mantendo o analista responsável pela validação, interpretação e aprovação das ações recomendadas.

**DATA QUALITY · DATA ANALYTICS · ARTIFICIAL INTELLIGENCE**

Dados → Análise Técnica → Regras de Negócio → IA → Validação → Decisão

## Problema de Negócio

A qualidade dos dados é fundamental para a confiabilidade das análises, indicadores e decisões utilizadas pelas organizações.

Bases de dados podem apresentar:

- Valores ausentes;
- Identificadores duplicados;
- Dados fora dos intervalos permitidos;
- Informações com formatos inválidos;
- Inconsistências em regras de negócio.

A identificação manual dessas ocorrências pode exigir tempo, esforço operacional e conhecimento técnico.

O projeto busca explorar como a combinação entre análise programática e Inteligência Artificial pode apoiar esse processo.

### Questões abordadas

- Quais problemas de qualidade existem na base?
- Quais regras de negócio foram violadas?
- Quantos registros estão envolvidos?
- Quais problemas devem receber prioridade?
- Como organizar recomendações de tratamento?
- A interpretação da IA está consistente com os resultados técnicos?
- Como preservar a supervisão humana durante o processo?

O objetivo é transformar verificações técnicas em informações estruturadas para apoiar decisões relacionadas à qualidade dos dados.

## Sobre os Dados

| Característica | Descrição |
|---|---|
| Tipo de projeto | Agente de IA aplicado a Data Quality |
| Segmento | Data Analytics e Inteligência Artificial |
| Formato de origem | CSV |
| Dataset de validação | Base sintética de clientes |
| Volume analisado | 10.000 registros |
| Estrutura | 4 colunas |
| Processamento | Python e Pandas |
| Interpretação | Groq API — GPT-OSS-20B |
| Saída técnica | JSON e relatórios textuais |

### Entidades e atributos analisados

| Campo | Descrição |
|---|---|
| `id_cliente` | Identificador do cliente |
| `nome` | Nome fictício do cliente |
| `idade` | Idade utilizada nas validações |
| `email` | E-mail utilizado nas verificações |

Os dados utilizados no teste de volume são sintéticos e foram preparados para simular problemas controlados de qualidade.

### Problemas introduzidos no dataset

- Valores ausentes em idade e e-mail;
- Identificadores duplicados;
- E-mails com formato inválido;
- Idades fora do intervalo permitido.

A utilização de dados sintéticos permite testar o comportamento do agente sem expor informações pessoais reais.

## Tecnologias e Ferramentas

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Desenvolvimento da lógica do agente |
| Pandas | Processamento e análise dos dados |
| Groq API | Integração com modelo de IA |
| GPT-OSS-20B | Interpretação dos resultados técnicos |
| Pytest | Testes automatizados |
| CSV | Dados de entrada |
| JSON | Relatórios e resultados estruturados |
| Git / GitHub | Versionamento e publicação |

## Metodologia

O projeto foi desenvolvido seguindo um fluxo de trabalho estruturado.

### 1. Data Profiling

Inspeção inicial do arquivo para compreender:

- Dimensões;
- Colunas;
- Tipos de dados;
- Estrutura da base;
- Características dos registros.

### 2. Data Quality

Verificações relacionadas a:

- Valores ausentes;
- Duplicidades;
- Problemas estruturais;
- Consistência dos registros.

### 3. Business Rules

Implementação de regras de negócio para validar condições específicas.

| Regra | Coluna | Objetivo |
|---|---|---|
| `valor_unico` | `id_cliente` | Identificar identificadores duplicados |
| `formato_email` | `email` | Identificar e-mails inválidos |
| `intervalo_idade` | `idade` | Identificar valores fora do intervalo permitido |

### 4. Treatment Planning

Organização das ocorrências em um plano de tratamento contendo:

- Regra violada;
- Coluna afetada;
- Severidade;
- Quantidade de registros;
- Recomendação;
- Justificativa;
- Status;
- Necessidade de aprovação humana.

### 5. AI Interpretation

Utilização da IA para interpretar os resultados técnicos e estruturar um relatório com:

- Resumo executivo;
- Indicadores gerais;
- Problemas identificados;
- Violações das regras;
- Registros afetados;
- Riscos para o negócio;
- Recomendações;
- Priorização;
- Conclusão.

### 6. AI Validation

Validação programática da interpretação produzida pela IA.

O objetivo é identificar divergências entre os resultados técnicos e as afirmações apresentadas pelo modelo.

### 7. Reporting

Geração e armazenamento dos resultados técnicos, interpretação e validação em arquivos estruturados e textuais.

### 8. Human-in-the-Loop

As recomendações são submetidas à aprovação humana antes de qualquer tratamento.

O agente não deve substituir a análise crítica nem executar correções sem autorização.

## Arquitetura do Agente

O fluxo do projeto segue as etapas:

**Dados → Análise Técnica → Regras de Negócio → Plano de Tratamento → Interpretação da IA → Validação → Relatórios**

A arquitetura separa a análise determinística da interpretação assistida por IA.

| Componente | Responsabilidade |
|---|---|
| Análise técnica | Inspecionar a estrutura e os dados |
| Regras de qualidade | Identificar violações das regras configuradas |
| Plano de tratamento | Organizar recomendações e prioridades |
| Interpretação da IA | Transformar resultados técnicos em relatório |
| Validação da interpretação | Verificar consistência com os resultados técnicos |
| Relatórios | Registrar resultados e evidências |
| Supervisão humana | Aprovar ou rejeitar ações propostas |

## Indicadores e Validações

Foi realizado um teste de volume utilizando um dataset sintético de 10.000 registros e 4 colunas.

### Resultados do teste

| Indicador | Resultado |
|---|---:|
| Registros analisados | 10.000 |
| Colunas | 4 |
| Células ausentes | 149 |
| IDs duplicados envolvidos | 60 |
| E-mails inválidos | 80 |
| Idades fora do intervalo | 7 |
| Regras violadas | 3 |
| Ocorrências de regras | 147 |
| Ações recomendadas | 3 |
| Ações pendentes | 3 |
| Alertas na validação da IA | 0 |

### Resultado da validação

**VALIDAÇÃO INICIAL APROVADA**

A interpretação gerada pela IA foi submetida à validação programática para verificar sua consistência com os resultados técnicos.

No teste de volume realizado, a validação inicial foi aprovada, sem alertas identificados.

O resultado representa a validação do cenário testado e não garante a ausência de erros em todas as situações possíveis.

## Segurança e Governança

O projeto adota princípios de segurança e supervisão:

- Uso de variáveis de ambiente para armazenar credenciais;
- Utilização de dados sintéticos nos testes documentados;
- Separação entre análise técnica e interpretação da IA;
- Validação programática das respostas;
- Aprovação humana antes da execução de ações de tratamento;
- Registro de recomendações e resultados para auditoria.

## Estrutura do Repositório

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
│   ├── main_teste_volume.py
│   ├── plano_tratamento.py
│   ├── regras_qualidade.py
│   └── validar_interpretacao.py
├── tests/
├── gerar_dataset_teste.py
├── requirements.txt
├── .gitignore
└── README.md
```

Os relatórios gerados durante a execução são armazenados localmente e não fazem parte da publicação do repositório.

## Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/rrleone/Agente_IA_DataQuality_Groq.git
cd Agente_IA_DataQuality_Groq
```

Substitua `URL_DO_REPOSITORIO` pela URL do repositório GitHub.

### 2. Criar ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

pip install -r requirements.txt

### 4. Configurar a API Groq

Configure a variável de ambiente `GROQ_API_KEY` com sua chave pessoal.

export GROQ_API_KEY="sua_chave_groq"

Nunca publique sua chave de API no código ou no repositório.

### 5. Executar o agente

```bash
python src/main.py
```

## Aplicação da Inteligência Artificial

A IA é utilizada como camada de interpretação e apoio à análise.

| Etapa | Responsabilidade |
|---|---|
| Análise técnica | Executada programaticamente |
| Identificação de regras | Determinística |
| Plano de tratamento | Estruturado a partir das ocorrências |
| Interpretação | Assistida por IA |
| Validação | Verificação programática |
| Aprovação | Responsabilidade humana |

A IA não substitui as regras técnicas nem a decisão do analista.

## Limitações e Evoluções

Este projeto representa uma implementação experimental e de portfólio.

Possíveis evoluções:

- Ampliação das regras de qualidade;
- Suporte a diferentes estruturas de dados;
- Evolução da validação das respostas da IA;
- Implementação de logs estruturados e monitoramento;
- Integração com bancos de dados;
- Interface para acompanhamento e aprovação das recomendações.

Os resultados apresentados correspondem ao dataset sintético e ao cenário de teste documentado.

## Conclusão

O projeto demonstra como Python, regras de negócio e Inteligência Artificial podem ser combinados para apoiar processos de Data Quality.

A abordagem mantém a análise técnica como base, utiliza a IA para interpretação e preserva a supervisão humana nas decisões de tratamento.

**Qualidade de dados não é apenas identificar inconsistências. É transformar problemas técnicos em informação confiável para decisões.**

---

## Autor

**Renato Leone**

Analista de Dados | Business Intelligence

Dados • Análise • Insights • Decisões
