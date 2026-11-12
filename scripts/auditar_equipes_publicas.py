import json,re,pathlib,concurrent.futures,urllib.parse,html
from coletar_sigaa_publico import Fetcher,parse,normalize,collect_doc
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
BASE=pathlib.Path(args.baseline).parent;OUT=pathlib.Path(args.output);OUT.mkdir(parents=True,exist_ok=True)
c=json.load(open(args.baseline)); projects=c['extension_projects']; bycode={}
for file in BASE.glob('extension_*.html'):
 t=parse(file.read_text())
 for tr in t.find('tr'):
  txt=tr.text();m=re.match(r'\s*([A-Z]{2,6}\d+-20\d{2})\b',txt)
  if not m or len(txt)>5000:continue
  for a in tr.find('a'):
   mm=re.search(r"'idAtividadeExtensaoSelecionada'\s*:\s*'(\d+)'",a.attrs.get('onclick',''))
   if mm:bycode[m[1]]=mm[1]
def clean(s):return ' '.join(s.split())
def audit(p):
 for participation in p.get('participations',[]):
  for url in participation.get('details_urls',[]):
   if '/visualizacaoAcaoExtensao/' in url:bycode[p['id']]=url.rsplit('/',1)[-1]
 r={'id':p['id'],'expected_title':p['title'],'team':[],'errors':[]};eid=bycode.get(p['id'])
 if not eid:r['errors']=['Identificador de ação não extraído da listagem'];return r
 url='https://sigaa.unemat.br/sigaa/link/public/extensao/visualizacaoAcaoExtensao/'+eid
 try:
  body,ev=Fetcher(OUT).fetch(url,'ext_'+p['id']);t=parse(body);r['evidence']=ev
  fields={}
  for tr in t.find('tr'):
   cells=[x for x in tr.children if not isinstance(x,str) and x.tag in ['td','th']]
   if len(cells)==2 and 0<len(cells[0].text().strip())<90:fields[clean(cells[0].text()).rstrip(':')]=clean(cells[1].text())
  r['fields']=fields
  title=fields.get('Título','')
  if not title:raise ValueError('Ficha pública sem título extraível; conferir retorno ou erro do SIGAA')
  if re.sub(r'[^A-Z0-9]','',normalize(html.unescape(html.unescape(title))))!=re.sub(r'[^A-Z0-9]','',normalize(html.unescape(html.unescape(p['title'])))):raise ValueError('Título da ficha diverge da listagem; não aceitar equipe automaticamente')
  for tab in t.find('table'):
   if tab.attrs.get('id')!='tbEquipe':continue
   text=clean(tab.text());m=re.search(r'^(.*?)\s*Categoria:\s*(.*?)\s*Função\s*:\s*([^@]+)',text)
   if not m:continue
   name=m[1].strip();cat=m[2].strip();role=m[3].strip();role=re.sub(r'\s+\S+$','',role) if re.search(r'\s+\S+@',text) else role
   # Função termina no próximo endereço eletrônico, que nunca é publicado no JSON.
   role=re.split(r'\s+[\w.+-]+@',text.split('Função',1)[1].lstrip(' :'))[0].strip()
   links=[urllib.parse.urljoin(url,re.sub(r'\s','',a.attrs['href'])) for a in tab.find('a') if '/public/docente/portal.jsf' in a.attrs.get('href','')]
   role=re.sub(r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b','',role).strip()
   r['team'].append({'name':name,'key':normalize(name),'category':cat,'role':role,'portal':links[0] if links else None})
  if not r['team']:r['errors'].append('Equipe nominal não extraída; não interpretar como equipe vazia')
 except Exception as ex:r['errors'].append(str(ex));r['team']=[]
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 rs=[]
 for r in pool.map(audit,projects):
  rs.append(r);(OUT/'equipes_extensao.json').write_text(json.dumps(rs,ensure_ascii=False,indent=2))
  if len(rs)%15==0:print('EXT',len(rs),'de',len(projects),'equipes',sum(bool(x['team']) for x in rs),flush=True)
print('EXT_FINAL',len(rs),'sucessos',sum(bool(x['team']) for x in rs),flush=True)
# Novos perfis são descobertos apenas em links efetivamente publicados nas equipes.
resolutions=[]
for original in c['results']:
 if not original['errors']:continue
 person=original['person'];links={m['portal'] for x in rs for m in x['team'] if m['key']==person['key'] and m['portal']}
 if len(links)==1:
  url=next(iter(links))
  if url!=person.get('portal') or any('menu público não localizado' in e for e in original['errors']):
   who={**person,'portal':url};result=collect_doc(who,OUT);result['resolution_source']='Link observado em equipe pública de extensão';resolutions.append(result)
   (OUT/'perfis_recuperados.json').write_text(json.dumps(resolutions,ensure_ascii=False,indent=2))
print('PERFIS_RECUPERADOS',len(resolutions),flush=True)
