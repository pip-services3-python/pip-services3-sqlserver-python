init:
	pip install -r requirements.txt
    
clean:
	rm -rf .cache
	rm -rf build
	rm -rf pip_services3_sqlserver.egg-info
	rm -f pip_services3_sqlserver/*.pyc
	rm -f pip_services3_sqlserver/**/*.pyc
	rm -rf test/__pycache__
	rm -rf test/**/__pycache__
	
install:
	pip install -e .

.PHONY: test
test:
	py.test test -s

docgen:
	pip install -U sphinx==3.3.1
	pip install sphinx-rtd-theme
	
	sphinx-apidoc -f -e -o build pip_services3_sqlserver
	cp conf.py ./build/
	cp index.rst ./build/
	sphinx-build -b html build docs -c .
	rm -rf build
