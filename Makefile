# test all modules
test:
	python3 -m unittest -v tests.test_html
	python3 -m unittest -v tests.test_dom
	python3 -m unittest -v tests.test_style
	python3 -m unittest -v tests.test_javascript
	python3 -m unittest -v tests.test_javascript_date
	python3 -m unittest -v tests.test_terminal
	python3 -m unittest -v tests.test_CDN
	python3 -m unittest -v tests.test_JSON
	python3 -m unittest -v tests.test_svg
	python3 -m unittest -v tests.test_collada
	python3 -m unittest -v tests.test_x3d
	python3 -m unittest -v tests.test_dQuery
	python3 -m unittest -v tests.test_geom
	python3 -m unittest -v tests.test_d3
	python3 -m unittest -v tests.test_sitemap
	python3 -m unittest -v tests.test_domonic
	python3 -m unittest -v tests.test_templates
	python3 -m unittest -v tests.test_window

testpc:
	python3 -m unittest -v tests.test_html
	python3 -m unittest -v tests.test_dom
	python3 -m unittest -v tests.test_style
	python3 -m unittest -v tests.test_javascript
	python3 -m unittest -v tests.test_javascript_date
	python3 -m unittest -v tests.test_cmd
	python3 -m unittest -v tests.test_CDN
	python3 -m unittest -v tests.test_JSON
	python3 -m unittest -v tests.test_svg
	python3 -m unittest -v tests.test_collada
	python3 -m unittest -v tests.test_x3d
	python3 -m unittest -v tests.test_dQuery
	python3 -m unittest -v tests.test_geom
	python3 -m unittest -v tests.test_d3
	python3 -m unittest -v tests.test_sitemap
	python3 -m unittest -v tests.test_domonic
	python3 -m unittest -v tests.test_window

# test single modules
test_domonic:
	python3 -m unittest -v tests.test_domonic

test_javascript:
	python3 -m unittest -v tests.test_javascript
	python3 -m unittest -v tests.test_javascript_date

test_html:
	python3 -m unittest -v tests.test_html

test_dom:
	python3 -m unittest -v tests.test_dom

test_svg:
	python3 -m unittest -v tests.test_svg

format:
	black domonic -l 120 && isort domonic

# release
build:
	rm -rf dist/
	python3 setup.py sdist bdist_wheel
	rm -r build/

deploy:
	rm -rf dist/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -r build/