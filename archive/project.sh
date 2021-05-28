function project(){

	PROJECT_NAME=$1
	
	NAME="byteface"
	EMAIL=""
	GITHUB="byteface"
	LICENSE="MIT"

	echo $PROJECT_NAME
	mkdir $PROJECT_NAME
	cd $PROJECT_NAME

	mkdir static
	mkdir static/js
	mkdir static/css
	mkdir static/img
	mkdir static/data

	mkdir archive

	touch app.py
	touch README.md
	touch LICENSE
	touch setup.py
	touch TODO
	touch index.html
	touch MakeFile
	touch fab.py
	touch sitemap.xml

	git init
	touch .gitignore	

	touch db.sqlite

	touch static/js/master.js
	touch static/css/styles.css
	touch static/data/data.json

	python3 -m venv venv
	. venv/bin/activate

	pip3 install requests
	pip3 install fabric
	pip3 install domonic

	pip3 freeze >> requirements.txt

	chmod -R 777 static
	open .

}

project $1