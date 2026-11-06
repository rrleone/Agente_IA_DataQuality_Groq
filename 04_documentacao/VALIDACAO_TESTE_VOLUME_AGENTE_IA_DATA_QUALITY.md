Agente de IA — Data Quality (Groq)
Evidência de validação do teste de volume
Data do teste: 06/11/2026
Dataset: 01_data/clientes_teste_10000.csv
Script executado: src/main_teste_volume.py
Modelo de IA: openai/gpt-oss-20b (Groq)
1. Objetivo
Validar o comportamento do agente em um dataset de volume, verificando se ele consegue:
- executar a análise técnica de qualidade de dados;
- identificar violações de regras de negócio;
- elaborar um plano de tratamento;
- gerar uma interpretação executiva com apoio da IA;
- validar a interpretação contra os resultados técnicos;
- preservar a aprovação humana antes de qualquer tratamento.
2. Características do dataset
Indicador	Resultado
Registros	10.000
Colunas	4
Linhas completamente duplicadas	0
Células ausentes	149


Ausências por coluna
Coluna	Células ausentes	Percentual
id_cliente	0	0,00%
nome	0	0,00%
idade	50	0,50%
email	99	0,99%
Total	149	0,75%


3. Regras de negócio violadas
Regra	Coluna	Severidade	Ocorrências
valor_unico	id_cliente	Alta	60
formato_email	email	Média	80
intervalo_idade	idade	Média	7
Total			147


Observação: as 60 ocorrências relacionadas à unicidade representam registros envolvidos em IDs repetidos. Não correspondem necessariamente a 60 valores distintos duplicados.
4. Plano de tratamento
O agente recomendou três ações:
1. Investigar os IDs repetidos e confirmar qual identificador deve ser mantido ou corrigido.
2. Validar os e-mails com a fonte responsável antes de qualquer atualização.
3. Conferir as idades fora do intervalo na fonte original.
Status: 3 ações pendentes.
Aprovação humana: necessária para todas as ações.

O agente não executou correções automaticamente.
5. Interpretação gerada pela IA
A interpretação apresentou as nove seções esperadas:
1. Resumo Executivo
2. Indicadores Gerais de Qualidade
3. Problemas Identificados
4. Violações das Regras de Negócio
5. Registros Afetados
6. Riscos para o Negócio
7. Recomendações
8. Priorização das Ações
9. Conclusão
A resposta informou o total de 149 células ausentes, detalhou as contagens por coluna e apresentou exemplos de registros afetados.
6. Ajuste técnico realizado
Durante os testes, a chamada à Groq apresentou inicialmente erro HTTP 413 relacionado ao tamanho do payload/contexto.

Para reduzir o conteúdo enviado ao modelo, foi implementado um resumo compacto do relatório técnico:
- o relatório completo continua sendo gerado e salvo localmente;
- a IA recebe uma versão resumida, com indicadores e exemplos limitados;
- o validador continua utilizando o relatório técnico completo e os dados locais.
Essa abordagem reduziu o volume enviado à IA sem substituir a análise técnica por uma análise feita exclusivamente pelo modelo.
7. Resultado da validação
Status da validação: VALIDAÇÃO INICIAL APROVADA
Total de alertas: 0
Resultado: teste de volume aprovado na execução registrada em 06/11/2026.
8. Limites e cuidados
- A aprovação refere-se à execução e ao dataset descritos neste documento.
- A interpretação da IA é uma camada explicativa; os resultados técnicos locais são a referência para contagens e regras.
- Recomendações de tratamento permanecem sujeitas à aprovação humana.
- Este teste não comprova, por si só, desempenho em datasets maiores, outros formatos de arquivo ou diferentes modelos de IA.
9. Artefatos da execução
Conforme o log da execução:
- Relatório técnico: 03_reports/relatorio_data_quality_20261106_161530.json
- Interpretação da IA: 03_reports/interpretacao_ia_20261106_161530.txt
- Validação da interpretação: 03_reports/validacao_interpretacao_ia_20261106_161530.json
Conclusão: o agente concluiu a análise do dataset de 10 mil registros, produziu a interpretação estruturada e passou pela validação inicial sem alertas. O resultado constitui evidência do teste de volume, mantendo a separação entre análise técnica, interpretação da IA e aprovação humana.