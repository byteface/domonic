# test all modules
PYTHON ?= ./venv/bin/python

test:
	$(PYTHON) -m unittest -v tests.test_html
	$(PYTHON) -m unittest -v tests.test_events
	$(PYTHON) -m unittest -v tests.test_dom
	$(PYTHON) -m unittest -v tests.test_style
	$(PYTHON) -m unittest -v tests.test_javascript
	$(PYTHON) -m unittest -v tests.test_javascript_date
	$(PYTHON) -m unittest -v tests.test_terminal
	$(PYTHON) -m unittest -v tests.test_CDN
	$(PYTHON) -m unittest -v tests.test_JSON
	$(PYTHON) -m unittest -v tests.test_svg
	$(PYTHON) -m unittest -v tests.test_collada
	$(PYTHON) -m unittest -v tests.test_x3d
	$(PYTHON) -m unittest -v tests.test_dQuery
	$(PYTHON) -m unittest -v tests.test_geom
	$(PYTHON) -m unittest -v tests.test_d3
	$(PYTHON) -m unittest -v tests.test_sitemap
	$(PYTHON) -m unittest -v tests.test_domonic
	$(PYTHON) -m unittest -v tests.test_templates
	$(PYTHON) -m unittest -v tests.test_window

testpc:
	$(PYTHON) -m unittest -v tests.test_html
	$(PYTHON) -m unittest -v tests.test_events
	$(PYTHON) -m unittest -v tests.test_dom
	$(PYTHON) -m unittest -v tests.test_style
	$(PYTHON) -m unittest -v tests.test_javascript
	$(PYTHON) -m unittest -v tests.test_javascript_date
	$(PYTHON) -m unittest -v tests.test_cmd
	$(PYTHON) -m unittest -v tests.test_CDN
	$(PYTHON) -m unittest -v tests.test_JSON
	$(PYTHON) -m unittest -v tests.test_svg
	$(PYTHON) -m unittest -v tests.test_collada
	$(PYTHON) -m unittest -v tests.test_x3d
	$(PYTHON) -m unittest -v tests.test_dQuery
	$(PYTHON) -m unittest -v tests.test_geom
	$(PYTHON) -m unittest -v tests.test_d3
	$(PYTHON) -m unittest -v tests.test_sitemap
	$(PYTHON) -m unittest -v tests.test_domonic
	$(PYTHON) -m unittest -v tests.test_window

# test single modules
test_domonic:
	$(PYTHON) -m unittest -v tests.test_domonic

test_javascript:
	$(PYTHON) -m unittest -v tests.test_javascript
	$(PYTHON) -m unittest -v tests.test_javascript_date

test_html:
	$(PYTHON) -m unittest -v tests.test_html

test_dom:
	$(PYTHON) -m unittest -v tests.test_dom

test_svg:
	$(PYTHON) -m unittest -v tests.test_svg

format:
	black domonic -l 120 && isort domonic


# test individual modules with coverage
coverage:
	coverage erase
	coverage run -m unittest -v tests.test_html
	coverage run --append -m unittest -v tests.test_events
	coverage run --append -m unittest -v tests.test_dom
	coverage run --append -m unittest -v tests.test_style
	coverage run --append -m unittest -v tests.test_javascript
	coverage run --append -m unittest -v tests.test_javascript_date
	coverage run --append -m unittest -v tests.test_terminal
	coverage run --append -m unittest -v tests.test_CDN
	coverage run --append -m unittest -v tests.test_JSON
	coverage run --append -m unittest -v tests.test_svg
	coverage run --append -m unittest -v tests.test_collada
	coverage run --append -m unittest -v tests.test_x3d
	coverage run --append -m unittest -v tests.test_dQuery
	coverage run --append -m unittest -v tests.test_geom
	coverage run --append -m unittest -v tests.test_d3
	coverage run --append -m unittest -v tests.test_sitemap
	coverage run --append -m unittest -v tests.test_domonic
	coverage run --append -m unittest -v tests.test_templates
	coverage run --append -m unittest -v tests.test_window
	coverage report


# release
clean:
	rm -rf build/ dist/ domonic.egg-info/

build:
	rm -rf dist/ build/ domonic.egg-info/
	$(PYTHON) -m build
	rm -rf build/

deploy:
	rm -rf dist/ build/ domonic.egg-info/
	$(PYTHON) -m build
	twine upload dist/*
	rm -rf build/
