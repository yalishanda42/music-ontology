default: ontology.owl

venv dependencies:
	python3 -m venv venv
	. venv/bin/activate
	python3 -m pip install --upgrade pip
	pip3 install -r requirements.txt

ontology.owl ontology: venv
	python3 music_ontology/ontology.py

test: ontology.owl
	python3 -m unittest -v