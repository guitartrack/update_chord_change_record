clean:
	rm -rf build

create_build_map:
	mkdir build

install_app:
	cp update_chord_change_record/* build/

install_dependencies:
	pip install -r requirements.txt -t build

invoke:
	sam local invoke --event test.json

test: clean create_build_map install_app install_dependencies invoke
