# Reproducción completa (desde la raíz del repo).  make all  =  reproduce -> test -> pdf -> docs
# (o por partes: make reproduce | make test | make pdf | make docs)
PY ?= python3
CODE = codigo

all:   ## secuencia completa, incluso si make se invoca con -j
	$(MAKE) reproduce
	$(MAKE) test
	$(MAKE) pdf
	$(MAKE) docs

test:                     ## controles numéricos, simbólicos, notebook, figuras y procedencia
	cd $(CODE) && $(PY) -m pytest -q

reproduce:                ## regenera TODOS los resultados, figuras y el registro de procedencia (~6 min); después `make test`
	cd $(CODE) && $(PY) run_spectrum.py && $(PY) run_spectrum.py starobinsky
	cd $(CODE) && $(PY) checks.py && $(PY) checks.py starobinsky
	cd $(CODE) && $(PY) compare_potentials.py
	cd $(CODE) && $(PY) checks_leon.py && $(PY) run_leon.py
	cd $(CODE) && $(PY) checks_resolution.py
	cd $(CODE) && $(PY) make_figures.py && $(PY) make_report_figures.py && $(PY) make_figures_potenciales.py && $(PY) make_figures_leon.py
	cd $(CODE) && $(PY) provenance_controls.py && $(PY) provenance_diagnostics.py && $(PY) provenance_datasets.py
	cd $(CODE) && $(PY) make_provenance_numbers.py
	$(PY) provenance/validate_provenance.py
	cd $(CODE) && $(PY) make_notebook.py

pdf:                      ## recompila derivation, informe y paper (necesita xelatex; 3 pasadas)
	cd derivation && for i in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error derivation.tex >build.log 2>&1 || { cat build.log; exit 1; }; done
	cd informe && for i in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error informe_UG.tex >build.log 2>&1 || { cat build.log; exit 1; }; done
	cd paper && for i in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error paper_UG.tex >build.log 2>&1 || { cat build.log; exit 1; }; done

docs:                     ## copia figuras y PDF a docs/ (para la página HTML)
	$(PY) docs/build_docs.py

.PHONY: all test reproduce pdf docs
