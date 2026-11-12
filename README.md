# Observatório Científico PPGCA UNEMAT

Painel para análise estratégica de publicações, coautorias, pesquisa, extensão e internacionalização.

**Idealizado por ERNANDES SOBREIRA e WILKINSON LÁZARO para fins de análise estratégica do programa.**

Versão de referência: 1.1.0 — 12/11/2026.

## Arquivos

- `index.html`: painel com código e fotografia dos dados incorporados. Abra em um navegador ou hospede em GitHub Pages.
- `scripts/coletar_sigaa_publico.py`: coletor de pesquisa e extensão; Python 3, apenas biblioteca padrão, sem login ou API institucional.
- `dados/base-inicial-2026-11-12.json`: coleta inicial com fontes, datas, hashes e lacunas.
- `METODO.md`: regras de construção e limites das redes.
- `observatorio-ppgca-codigo-v1.1.0.zip`: versão congelada do código; resumo em `SHA256SUMS.txt`.

## Executar coleta

```sh
python3 scripts/coletar_sigaa_publico.py --output dados/coletas/AAAA-MM-DD
```

A execução consulta a equipe do programa, segue as páginas individuais e extrai códigos institucionais. Produz coleta.json e evidências HTML. Não altera automaticamente o painel nem publica arquivos. A agenda mensal assistida do ChatGPT é independente deste repositório; hospedar o HTML não ativa o coletor.

O link institucional de Wilkinson estava incorreto em 12/11/2026. Há uma resolução explícita para o perfil público confirmado, que continua sujeito à validação do nome em cada coleta.

## Estado da base

Coleta inicial executada em 12/11/2026: 98 códigos de pesquisa, 286 ações de extensão. Cobertura parcial: páginas sem link ou sem registros extraíveis não equivalem a ausência de projetos. Datas de cadastro não comprovam execução atual. Equipes nominais de extensão preservadas da coleta anterior ainda exigem revalidação.

## Preservação e registro

O pacote e seu SHA-256 permitem identificar esta versão. Guarde o arquivo original sem alterações. O repositório e os hashes não constituem registro concedido pelo INPI, comprovação de novidade ou definição de titularidade. O pedido de registro de programa de computador é uma etapa própria.

## Redes corrigidas

As 286 ações conhecidas tiveram a equipe nominal pública conferida. O grafo permite alternar cadastro PPGCA e equipe completa. Pesquisa reúne listagens atuais e 16 equipes documentais com data de emissão própria. Há códigos distintos com títulos iguais, sinalizados para conferência institucional. O grafo é pessoa → projeto, sem pressupor colaboração direta entre todos os pares. Cadastros e vigências são filtros distintos. Consulte CHANGELOG.md e os arquivos auditoria-redes.json e arestas-projetos.csv em .
