import sys, urllib.request, urllib.parse, re, xml.etree.ElementTree as ET
ns={'a':'http://www.w3.org/2005/Atom','x':'http://arxiv.org/schemas/atom'}
def q(query, n=25):
    url="http://export.arxiv.org/api/query?"+urllib.parse.urlencode({'search_query':query,'start':0,'max_results':n,'sortBy':'submittedDate','sortOrder':'descending'})
    d=urllib.request.urlopen(url,timeout=40).read()
    r=ET.fromstring(d)
    for e in r.findall('a:entry',ns):
        i=e.find('a:id',ns).text.split('/abs/')[-1]
        t=re.sub(r'\s+',' ',e.find('a:title',ns).text)
        au=", ".join(a.find('a:name',ns).text for a in e.findall('a:author',ns))[:70]
        jr=e.find('x:journal_ref',ns); jr=jr.text if jr is not None else ''
        print(f"{i} | {t[:95]} | {au} | {jr[:60]}")
for qq in sys.argv[1:]:
    print("###",qq); q(qq)
