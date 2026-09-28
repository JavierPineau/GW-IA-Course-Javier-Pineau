import sys, json, urllib.request, urllib.parse
def q(s):
    u="https://api.crossref.org/works?rows=2&select=DOI,title,author,container-title,volume,issue,page,article-number,issued&query.bibliographic="+urllib.parse.quote(s)
    try: d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'prov-check (mailto:CAMBIAR_POR_TU_EMAIL)'}),timeout=40))
    except Exception as e: print("ERR",s,e); return
    print("##",s)
    for it in d['message']['items'][:1]:
        au=", ".join(a.get('family','?') for a in it.get('author',[])[:4])
        print("  ",it['DOI'],"|",(it.get('title') or [''])[0][:80],"|",au,"|",(it.get('container-title') or [''])[0],it.get('volume',''),it.get('page',it.get('article-number','')),it['issued']['date-parts'][0][0])
qs=["Henneaux Teitelboim The cosmological constant and general covariance Physics Letters B 1989",
"Unruh A unimodular theory of canonical quantum gravity Physical Review D 1989",
"Weinberg The cosmological constant problem Reviews of Modern Physics 1989",
"Ng van Dam Unimodular theory of gravity and the cosmological constant J Math Phys 1991",
"Anderson Finkelstein Cosmological constant and fundamental length American Journal of Physics 1971",
"Padilla Saltas A note on classical and quantum unimodular gravity European Physical Journal C 2015",
"Ellis van Elst Murugan Uzan On the trace-free Einstein equations as a viable alternative to general relativity Classical and Quantum Gravity 2011",
"Ellis The trace-free Einstein equations and inflation General Relativity and Gravitation 2014",
"Gao Brandenberger Cai Chen Cosmological perturbations in unimodular gravity JCAP 2014",
"Basak Fabre Shankaranarayanan Cosmological perturbations of unimodular gravity and general relativity are identical GRG 2016",
"Josset Perez Sudarsky Dark energy from violation of energy conservation Physical Review Letters 2017",
"Perez Sudarsky Dark energy from quantum gravity discreteness Physical Review Letters 2019",
"Landau Benetti Perez Sudarsky Cosmological constraints on unimodular gravity models with diffusion Physical Review D 2023",
"Cho Singh Unimodular theory of gravity and inflation Classical and Quantum Gravity 2015",
"Fabris Alvarenga Hamani-Daouda Velten Nonconservative unimodular gravity: gravitational waves Symmetry 2022",
"Leon Inflation and the cosmological (not-so) constant in unimodular gravity Classical and Quantum Gravity 2022",
"Bengochea Leon Perez Sudarsky A clarification on prevailing misconceptions in unimodular gravity",
"Linares Cedeno Nucamendi Gauge fixing in cosmological perturbations of unimodular gravity JCAP 2023",
"de Cesare Wilson-Ewing Interacting dark sector from the trace-free Einstein equations Physical Review D 2022",
"Alvarenga Fabris Velten Using cosmological perturbation theory to distinguish between general relativity and unimodular gravity Symmetry 2023",
"Maroto TDiff invariant field theories for cosmology JCAP 2024",
"Jaramillo-Garrido Maroto Martin-Moruno TDiff in the dark JHEP 2024",
"Mukhanov Feldman Brandenberger Theory of cosmological perturbations Physics Reports 1992",
"Planck 2018 results X Constraints on inflation",
"BICEP Keck Improved constraints on primordial gravitational waves using Planck WMAP and BICEP/Keck observations through the 2018 observing season",
"Baumann TASI lectures on inflation",
"Caprini Figueroa Cosmological backgrounds of gravitational waves Classical and Quantum Gravity 2018",
"Fabris Alvarenga Hamani-Daouda Velten Nonconservative unimodular gravity: a viable cosmological scenario European Physical Journal C 2022",
"Alvarez Blas Garriga Verdaguer Transverse Fierz-Pauli symmetry Nuclear Physics B 2006"]
for s in qs: q(s)
