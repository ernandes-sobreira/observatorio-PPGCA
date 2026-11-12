import pathlib,re,json,hashlib,datetime
from coletar_sigaa_publico import normalize
import argparse
ap=argparse.ArgumentParser();ap.add_argument('--documents',required=True);ap.add_argument('--output',required=True);args=ap.parse_args()
root=pathlib.Path(args.documents);records={}
for f in sorted(root.glob('documento_*.txt')):
 s=f.read_text();cm=re.search(r'Código:\s*([A-Z]+\d+-\d{4})',s)
 if not cm:continue
 code=cm[1];em=re.search(r'Emitido em (\d{2}/\d{2}/\d{4})',s);date=em[1] if em else None
 team=[]
 pat=r'\[ID REMOVIDO\]\s*(.*?)\s+(DOCENTE|DISCENTE|EXTERNO|SERVIDOR|TECNICO)\s+\d+(?:[.,]\d+)?\s+((?:VICE\s+)?COORDENADOR\(A\)|COLABORADOR\(A\)|Colaborador|Membro Externo|MEMBRO)'
 for m in re.finditer(pat,s,re.S|re.I):
  name=' '.join(m[1].split());team.append({'name':name,'key':normalize(name),'category':m[2].upper(),'role':m[3].upper(),'portal':None})
 period=re.search(r'Período (?:do Projeto|de Execução):\s*(\d{2}/\d{2}/\d{4})\s+a\s+(\d{2}/\d{2}/\d{4})',s)
 title=re.search(r'(?:Titulo do Projeto|Título):\s*(.*?)\s+Tipo(?: do Projeto)?:',s,re.S)
 status=re.search(r'Situação(?: do Projeto)?:\s*([^\n]+)',s)
 if not team:continue
 record={'id':code,'title':' '.join(title[1].split()) if title else '', 'team':team,'document_date':date,'source':'Relatório institucional SIGAA fornecido no acervo do Drive','date_consulted':'2026-11-12','redacted_text_sha256':hashlib.sha256(s.encode()).hexdigest(),'period':{'start':datetime.datetime.strptime(period[1],'%d/%m/%Y').date().isoformat(),'end':datetime.datetime.strptime(period[2],'%d/%m/%Y').date().isoformat()} if period else None,'status_in_document':status[1] if status else None,'source_file_private':f.name}
 prev=records.get(code)
 def dt(x):return datetime.datetime.strptime(x,'%d/%m/%Y') if x else datetime.datetime(1900,1,1)
 if not prev or dt(date)>dt(prev['document_date']):records[code]=record
pathlib.Path(args.output).write_text(json.dumps(list(records.values()),ensure_ascii=False,indent=2))
for r in records.values():print(r['id'],r['document_date'],'members',len(r['team']),r['period'])
