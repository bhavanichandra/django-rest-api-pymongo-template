OS = mac
VENV=.venv
COMMIT_MESSAGE=
BRANCH=main

ifeq ($(OS), mac)
	PYTHON = $(VENV)/bin/python
	PIP = $(VENV)/bin/pip
else
	PYTHON = $(VENV)/Scripts/python
	PIP = $(VENV)/Scripts/pip
endif

run: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python -m venv $(VENV)
	$(PIP) install -r requirements.txt

update-requirements: 
	rm requirements.txt
	$(PIP) freeze > requirements.txt

commit-push: update-requirements
	git add --all
	git commit -m "$(COMMIT_MESSAGE)"
	git push pi $(BRANCH)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)