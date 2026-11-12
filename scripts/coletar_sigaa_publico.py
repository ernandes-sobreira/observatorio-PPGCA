#!/usr/bin/env python3
"""Coleta pública e rastreável do SIGAA UNEMAT. Não utiliza credenciais."""
import argparse,collections,concurrent.futures,datetime,hashlib,http.cookiejar,json,pathlib,re,urllib.parse,urllib.request,time
from html.parser import HTMLParser

ROOT='https://sigaa.unemat.br'
TEAM=ROOT+'/sigaa/public/programa/equipe.jsf?id=655&lc=pt_BR'
class Node:
 def __init__(self,tag,attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.parent=parent;self.children=[]
 def text(self):return ' '.join(c if isinstance(c,str) else c.text() for c in self.children).strip()
 def find(self,tag):
  out=[]
  for c in self.children:
   if isinstance(c,Node):
    if c.tag==tag:out.append(c)
    out+=c.find(tag)
  return out
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.root=Node('root');self.node=self.root
 def handle_starttag(self,tag,attrs):
  n=Node(tag,attrs,self.node);self.node.children.append(n)
  if tag not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.node=n
 def handle_endtag(self,tag):
  n=self.node
  while n.parent and n.tag!=tag:n=n.parent
  if n.parent:self.node=n.parent
 def handle_data(self,data):self.node.children.append(data)
def parse(s):p=Parser();p.feed(s);return p.root
def normalize(s):
 import unicodedata
 return ' '.join(''.join(c for c in unicodedata.normalize('NFD',s.upper()) if unicodedata.category(c)!='Mn').replace('.','').split())
class Fetcher:
 def __init__(self,out):self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()));self.out=out
 def fetch(self,url,label,data=None):
  req=urllib.request.Request(url,data=data,headers={'User-Agent':'PPGCA-Observatorio/1.0 (consulta publica academica; sem autenticacao)'})
  with self.opener.open(req,timeout=30) as r:
   raw=r.read();actual=r.geturl();charset=r.headers.get_content_charset() or 'utf-8'
  text=raw.decode(charset,errors='replace');p=self.out/(label+'.html');p.write_bytes(raw)
  return text,{'url':url,'final_url':actual,'file':p.name,'sha256':hashlib.sha256(raw).hexdigest(),'collected_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def team_rows(tree):
 out=[]
 for tr in tree.find('tr'):
  cells=[c for c in tr.children if isinstance(c,Node) and c.tag in ['td','th']]
  if len(cells)<3:continue
  name=' '.join(cells[0].text().split())
  if not name or 'Nome'==name or not any(t in cells[1].text().upper() for t in ['PROFESSOR','DOUTORANDO']):continue
  links=[urllib.parse.urljoin(TEAM,a.attrs.get('href','')) for a in cells[0].find('a') if '/public/docente/portal.jsf' in a.attrs.get('href','')]
  out.append({'name':name,'key':normalize(name),'role':cells[1].text(),'level':cells[2].text(),'portal':links[0] if links else None})
 return out
CODE=re.compile(r'\b([A-Z]{2,6}\d{1,6}-20\d{2})\b')
def list_records(tree,kind,who,evidence):
 records=[]
 for tr in tree.find('tr'):
  cells=[c for c in tr.children if isinstance(c,Node) and c.tag in ['td','th']]
  if not cells:continue
  # Uma célula com código identifica a linha; linhas contêineras não são tomadas como um projeto.
  first=' '.join(cells[0].text().split());m=CODE.search(first)
  if not m or len(CODE.findall(tr.text()))!=1:continue
  code=m.group(1);texts=[' '.join(c.text().split()) for c in cells]
  title=texts[1] if len(texts)>1 else first[m.end():].strip();area=texts[2] if len(texts)>2 else ''
  if not title:continue
  links=[urllib.parse.urljoin(evidence['final_url'],a.attrs.get('href','')) for a in tr.find('a') if a.attrs.get('href') and not a.attrs.get('href').startswith(('javascript:','#'))]
  if kind=='extension':
   for a in tr.find('a'):
    am=re.search(r"'idAtividadeExtensaoSelecionada'\s*:\s*'(\d+)'",a.attrs.get('onclick',''))
    if am:links.append('https://sigaa.unemat.br/sigaa/link/public/extensao/visualizacaoAcaoExtensao/'+am[1])
  records.append({'id':code,'year':int(code.rsplit('-',1)[-1]),'title':title,'area':area,'kind':kind,'faculty_key':who['key'],'faculty_name':who['name'],'participation_evidence':'Projeto/ação listado na página pública deste docente','source_url':evidence['url'],'collected_at':evidence['collected_at'],'snapshot_sha256':evidence['sha256'],'details_urls':links})
 return records
def collect_doc(who,out):
 result={'person':who,'research':[],'extension':[],'pages':[],'errors':[]}
 if not who['portal']:
  result['errors'].append('Equipe institucional não fornece link de página docente.');print('SEM_LINK',who['name'],flush=True);return result
 f=Fetcher(out)
 try:
  body,ev=f.fetch(who['portal'],'portal_'+re.sub(r'\W','_',who['key']));tree=parse(body);result['pages'].append(ev)
  links={}
  for a in tree.find('a'):
   href=a.attrs.get('href','');txt=normalize(a.text())
   if 'PROJETOS DE PESQUISA' in txt:links['research']=urllib.parse.urljoin(ev['final_url'],href)
   if 'ATIVIDADES DE EXTENSAO' in txt:links['extension']=urllib.parse.urljoin(ev['final_url'],href)
  # O link institucional é a autoridade para siape. Descobrir o menu evita adivinhar identificadores.
  for kind in ['research','extension']:
   url=links.get(kind)
   if not url or 'public/docente/' not in url:result['errors'].append(kind+': menu público não localizado');continue
   try:
    text,e=f.fetch(url,kind+'_'+re.sub(r'\W','_',who['key']));t=parse(text);flat=t.text();result['pages'].append(e)
    if 'Comportamento Inesperado' in flat:raise ValueError('SIGAA retornou erro da aplicação')
    if normalize(who['name']) not in normalize(flat):raise ValueError('Página não confirma o nome do docente; possível redirecionamento')
    result[kind]=list_records(t,kind,who,e)
    if not result[kind]:result['errors'].append(kind+': nenhum código de projeto extraído; não interpretar como ausência de projetos')
    print(kind,who['name'],len(result[kind]),flush=True)
   except Exception as exc:result['errors'].append(kind+': '+str(exc));print('FALHA',kind,who['name'],str(exc)[:100],flush=True)
 except Exception as exc:result['errors'].append('portal: '+str(exc));print('FALHA_PORTAL',who['name'],str(exc)[:100],flush=True)
 return result
def aggregate(results,kind):
 data={}
 for result in results:
  for r in result[kind]:
   p=data.setdefault(r['id'],{'id':r['id'],'year':r['year'],'title':r['title'],'type':'PESQUISA' if kind=='research' else 'EXTENSAO','faculty':[],'participations':[],'area':r['area'],'status':'Situação de execução não publicada na listagem','themes':[],'primaryTheme':'outros','source':'SIGAA — listagens públicas individuais consultadas nesta coleta','url':r['source_url']})
   if r['faculty_key'] not in p['faculty']:p['faculty'].append(r['faculty_key']);p['participations'].append(r)
 for p in data.values():p['docs']='; '.join(r['faculty_name']+' (participação listada)' for r in p['participations'])
 return sorted(data.values(),key=lambda x:(-x['year'],x['id']))
def run(outpath):
 out=pathlib.Path(outpath);out.mkdir(parents=True,exist_ok=True);f=Fetcher(out)
 body,ev=f.fetch(TEAM,'equipe');people=team_rows(parse(body))
 overrides={'WILKINSON LOPES LAZARO':'https://sigaa.unemat.br/sigaa/public/docente/portal.jsf?siape=118181002'}
 for person in people:
  if person['key'] in overrides:person['portal_original']=person['portal'];person['portal']=overrides[person['key']]
 if not people:raise RuntimeError('Equipe não extraída: não continuar com população vazia.')
 print('EQUIPE',len(people),'COM_LINK',sum(bool(x['portal']) for x in people),flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda p:collect_doc(p,out),people))
 result={'method_version':'1.0.0','team_source':ev,'people':people,'results':results,'research_projects':aggregate(results,'research'),'extension_projects':aggregate(results,'extension'),'collected_date':datetime.datetime.now(datetime.timezone.utc).date().isoformat(),'complete':all(not r['errors'] for r in results),'rule':'Ligações apenas por código institucional comum em duas listagens individuais. Coocorrência de temas ou títulos não cria ligação.'}
 (out/'coleta.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
 print('CONCLUIDO',json.dumps({'docentes':len(people),'pesquisa':len(result['research_projects']),'extensao':len(result['extension_projects']),'cobertura_integral':result['complete'],'pessoas_com_falhas':sum(bool(r['errors']) for r in results)},ensure_ascii=False),flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();run(args.output)
