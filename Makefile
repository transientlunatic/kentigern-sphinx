# Makefile: For Python3 development.
# Because fabric doesn't work in Py3 :(

.PHONY: clean demo demo_server wheel

clean:
	rm -rf "dist" \
		"build" \
		"demo/build" \
		"kentigern.egg-info" \
		"theme-files/dist"
	find kentigern/static \( -name "*.js" -o -name "*.css" -o -name "*.woff" -o -name "*.woff2" -o -name "*.LICENSE.txt" \) -delete
	rm -rf "kentigern/static/fonts"

demo: css
	cd demo && make html

# PORT allows you to specify a different port if say
# port 8000 is currently in use
#
# make demo_server PORT=8080
PORT ?= 8000
demo_server: demo
	cd demo/build/html && python3 -m http.server $(PORT)

wheel: css
	python3 -m build --wheel --no-isolation

css:
	cd theme-files && npm install
	cd theme-files && npx webpack --mode production && cp -r dist/* ../kentigern/static
	cp theme-files/darkmode.js kentigern/static/darkmode.js

