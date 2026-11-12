# Método documentado — versão 1.1.0

1. Identificar integrantes pela equipe pública oficial do PPGCA (programa 655), preservando professores e pós-doutorandos como categorias distintas.
2. Seguir links efetivamente publicados para os perfis individuais. Conferir nome da pessoa antes de aceitar registros. Uma resolução de perfil deve ter fonte pública e permanecer explícita.
3. Consultar as listagens de pesquisa e extensão. Registrar código institucional, título, ano de cadastro, integrante, URL, instante UTC e SHA-256 da resposta.
4. Consolidar registros pelo código institucional, preservando eventuais códigos distintos com títulos iguais como uma pendência de identificação institucional. O grafo principal é bipartido: cada aresta liga pessoa a projeto/ação com uma fonte explícita. Compartilhar projeto não é apresentado como prova de colaboração direta entre todos os pares.
5. Não criar ligações por afinidade temática, nome semelhante, orientação ou simples presença numa lista de docentes. Rede de projetos e rede de coautoria são relações distintas.
6. Na extensão, consultar a ficha nominal de cada ação; somente equipes extraídas e com título conferido formam ligações. Comparar a equipe com as listagens individuais e registrar diferenças. Na pesquisa, relatórios institucionais do acervo fornecem equipes e vigências na data de emissão; as listagens atuais são evidências separadas. Coordenação e participação discente exigem registro nominal. Não atribuir execução atual ou resultados sem fonte específica.
7. Distinguir consulta com evidência, página inacessível, menu ausente e resposta sem código. Falhas nunca geram falsos zeros nem exclusão automática de evidência histórica.
8. Comparar participações novas e anteriores por (código, pessoa, tipo). Guardar a última evidência válida e sinalizar participações não reobservadas; não transformar falha de consulta em saída do projeto.
9. Revisar mudanças, atualizar a fotografia de dados no painel e publicar uma versão identificada. A automação mensal assistida é externa ao HTML.

## Base inicial de 12/11/2026

98 códigos de pesquisa e 286 de extensão; 33 integrantes na equipe institucional, incluindo pós-doutorandos. A correção do perfil público de Wilkinson recuperou 18 participações de pesquisa ausentes no painel anterior. Cobertura parcial; consultar o arquivo JSON para lacunas por integrante. A listagem pública não permite afirmar que todos esses projetos estejam em execução em novembro de 2026.

## Publicações e discentes

Publicações exigem registros bibliográficos e identificação de autoria. Correspondência nominal com cadastro discente não comprova matrícula na data do artigo. Afiliação estrangeira exige metadados de instituições dos autores; país de editora não é colaboração internacional. Os conjuntos bibliográficos têm proveniência própria e não são atualizados pelo coletor SIGAA de projetos.

## Preservação

Código congelado e dados são arquivos distintos. A fotografia dos dados está incorporada no HTML portátil; novas coletas geram novas versões. Hash identifica integridade do arquivo, sem atestar exatidão científica, originalidade ou concessão de registro.

## Correção das redes — 12/11/2026

A versão 1.0 usava participação em listagens individuais para projetar pares entre docentes. Essa construção omitia parceiros externos, integrantes sem página e projetos antigos com vigência no recorte. A versão 1.1 apresenta pessoa → projeto, equipes nominais, fontes e datas. Inclui opção de equipe completa e opção restrita ao cadastro PPGCA.

Identidades do cadastro são preservadas. Variantes explícitas: MANOEL DOS SANTOS FILHO corresponde a MANOEL DOS S. FILHO no cadastro; SANDRA MARA ALVES DA SILVA NEVES corresponde a SANDRA MARA ALVES SILVA NEVES. Pessoas externas sem identificador inequívoco não são unificadas entre ações apenas por nome. Categoria EXTERNO numa ação não altera o vínculo da pessoa com o PPGCA. Beatriz Ferraz Bühler e Beatriz Schwantes Marimon são pessoas distintas; Solange Aparecida Arrolho da Silva e Solange Kimie Ikeda Castrillon também.

O filtro de vigência exige início e fim documentados com sobreposição entre 01/01/2025 e a data de referência. Ano do código e período de cota não são vigência. O filtro de cadastro é identificado separadamente. Os relatórios originais podem conter documentos pessoais: somente nomes profissionais, categorias, funções, vigências e metadados de proveniência são extraídos para publicação.

O coletor nominal de extensão é executado após o coletor de listagens: `python3 scripts/auditar_equipes_publicas.py --baseline dados/coletas/AAAA-MM-DD/coleta.json --output dados/equipes/AAAA-MM-DD`. Falhas ficam documentadas, sem equipes inventadas. O pacote v1.0.0 permanece preservado; novas correções geram nova versão.
