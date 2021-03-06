help:
	@echo '                                                                                     		'
	@echo 'Makefile for the edX Cloudmanager SDK                                                            ' 
	@echo '                                                                                     		'
	@echo 'Usage:                                                                               		'
	@echo '    make requirements                 install requirements for local development     		'
	@echo '    make clean                        delete generated byte code and coverage reports		'
	@echo '    make quality                      run PEP8 and Pylint                            		'
	@echo '    make validate                     Run Python and JavaScript unit tests and linting 		'
	@echo '    make accept                       run acceptance tests                           		'
	@echo '                                                                                     		'

requirements:
	pip install -qr requirements/local.txt --exists-action w

clean:
	find . -name '*.pyc' -delete
	coverage erase
	rm -rf coverage

validate_python: clean
	coverage report
	make quality

fast_validate_python: clean
	make quality

quality:
	pep8 --config=.pep8 cm_sdk 
	pylint --rcfile=pylintrc cm_sdk 

validate: validate_python


# Targets in a Makefile which do not produce an output file with the same name as the target name
.PHONY: help requirements clean validate_python quality fast_validate_python
