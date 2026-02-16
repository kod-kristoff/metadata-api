download-schema:
	cd tests/assets/schema && test -f metadata.json || wget https://github.com/spraakbanken/metadata/raw/refs/heads/main/schema/metadata.json
