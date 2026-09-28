import sys, urllib.request, re, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom','x':'http://arxiv.org/schemas/atom'}
ids=",".join(sys.argv[1:])
d=urllib.request.urlopen("http://export.arxiv.org/api/query?id_list="+ids+"&max_results=50",timeout=40).read()
for e in ET.fromstring(d).findall('a:entry',ns):
    i=e.find('a:id',ns).text.split('/abs/')[-1]
    t=re.sub(r'\s+',' ',e.find('a:title',ns).text)
    au=", ".join(a.find('a:name',ns).text for a in e.findall('a:author',ns))
    jr=e.find('x:journal_ref',ns); jr=jr.text if jr is not None else '-'
    doi=e.find('x:doi',ns); doi=doi.text if doi is not None else '-'
    pub=e.find('a:published',ns).text[:10]
    ab=re.sub(r'\s+',' ',e.find('a:summary',ns).text)
    print(f"\n[{i}] {t}\n  authors: {au}\n  published: {pub} | journal: {jr} | doi: {doi}\n  abstract: {ab}")
