run_short:
	./run.py < texts/Short.txt

lookup:
	cd ../whitakers-words/ && ./bin/words $(word)

test:
	python3 -m unittest $(path)
