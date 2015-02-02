.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;

.PHONY: pep8
pep8:
	@flake8 . --ignore=F403,F401

.PHONY: test
test:
	@python -m unittest discover
