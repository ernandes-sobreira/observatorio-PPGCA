# Observatório Científico PPGCA UNEMAT

Painel público para análise estratégica de publicações, coautorias, temas, linhas, colaboração discente, pesquisa, extensão e internacionalização.

**Idealizado por ERNANDES SOBREIRA e WILKINSON LÁZARO para fins de análise estratégica do programa.**

## Usar o painel

Abra `index.html` no navegador. A versão portátil contém código e fotografia dos dados incorporados. Os arquivos JSON/CSV e ZIP são os downloads do painel e devem permanecer na mesma pasta ao hospedar.

## Código e método

- `METODO.md`: regras, fontes e limitações.
- `scripts/coletar_sigaa_publico.py`: Python 3, biblioteca padrão, consultas públicas ao SIGAA, sem login ou API institucional.
- `coleta-sigaa-2026-11-12.json`: evidências da coleta inicial, URLs, instantes, hashes e lacunas.
- `observatorio-ppgca-codigo-v1.0.0.zip` e `SHA256SUMS.txt`: cópia congelada do código e resumo de integridade para preservação. Guarde o ZIP original sem alterações. A preparação não equivale a registro concedido pelo INPI nem comprova novidade.

Execute a coleta com `python3 scripts/coletar_sigaa_publico.py --output dados/coletas/AAAA-MM-DD`. O coletor produz evidências; não publica o painel automaticamente. A rotina mensal assistida do ChatGPT é externa ao HTML.

## Base inicial — 12/11/2026

98 códigos de pesquisa e 286 ações de extensão em todos os anos disponíveis. No recorte de cadastro 2025–2026: 55 projetos e 107 ações. Cobertura parcial: páginas indisponíveis e respostas sem código não equivalem a zero projetos. Ano de cadastro não comprova execução atual. Equipes nominais anteriores mantêm data própria e exigem revalidação.

## Hospedagem

O workflow GitHub Pages publica os arquivos estáticos. A primeira execução pode exigir que o proprietário habilite Pages / GitHub Actions nas configurações do repositório. Nenhuma credencial institucional é necessária para visualizar o painel.
