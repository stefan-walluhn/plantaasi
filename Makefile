INTERFACE?=/dev/ttyUSB0
PLANTAASI_FILES=main.py config.json plantaasi

venv: requirements.txt ## create local basic python environment
	python3 -m venv venv
	venv/bin/pip install --upgrade pip

venv/.requirements_installed: venv ## install requirements to the python environment
	venv/bin/pip install --upgrade -r requirements.txt
	touch $@

.PHONY: install
install: venv/.requirements_installed

.PHONY: upload
upload: venv/.requirements_installed ## upload plantassi files to the microcontroler
	``
	@for upload in $(PLANTAASI_FILES) ; do\
		echo "put $$upload" ;\
		venv/bin/ampy --port $(INTERFACE) put $$upload ;\
	done	

.PHONY: clean
clean:
	rm -rf venv
