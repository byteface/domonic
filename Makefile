# test all modules
test:
	python3 -m unittest tests.test_html
	python3 -m unittest tests.test_dom
	python3 -m unittest tests.test_style
	python3 -m unittest tests.test_javascript
	python3 -m unittest tests.test_terminal
	python3 -m unittest tests.test_CDN
	python3 -m unittest tests.test_JSON
	python3 -m unittest tests.test_svg
	python3 -m unittest tests.test_collada
	python3 -m unittest tests.test_x3d
	python3 -m unittest tests.test_dQuery
	python3 -m unittest tests.test_geom
	python3 -m unittest tests.test_d3
	python3 -m unittest tests.test_domonic

testpc:
	python3 -m unittest tests.test_html
	python3 -m unittest tests.test_dom
	python3 -m unittest tests.test_style
	python3 -m unittest tests.test_javascript
	python3 -m unittest tests.test_cmd
	python3 -m unittest tests.test_CDN
	python3 -m unittest tests.test_JSON
	python3 -m unittest tests.test_svg
	python3 -m unittest tests.test_collada
	python3 -m unittest tests.test_x3d
	python3 -m unittest tests.test_dQuery
	python3 -m unittest tests.test_geom
	python3 -m unittest tests.test_d3
	python3 -m unittest tests.test_domonic


# test single modules
test_domonic:
	python3 -m unittest tests.test_domonic

test_javascript:
	python3 -m unittest tests.test_javascript

test_html:
	python3 -m unittest tests.test_html

test_dom:
	python3 -m unittest tests.test_dom


# release
build:
	rm -r dist/
	python3 setup.py sdist bdist_wheel
	rm -r build/

deploy:
	rm -r dist/
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
	rm -r build/