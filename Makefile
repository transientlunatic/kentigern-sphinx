# Makefile: For Python3 development.
# Because fabric doesn't work in Py3 :(

.PHONY: clean demo demo_server

clean:
	rm -rf "dist" \
		"build" \
		"demo/build" \
		"sphinx_bootstrap_theme.egg-info" \
		"theme-files/dist"
	rm -f kentigern/static/kentigern-modern.css \
		kentigern/static/kentigern.js \
		kentigern/static/kentigern.js.LICENSE.txt \
		kentigern/static/*.woff \
		kentigern/static/*.woff2

demo: css
	cd demo && make html

# PORT allows you to specify a different port if say
# port 8000 is currently in use
#
# make demo_server PORT=8080
PORT ?= 8000
demo_server: demo
	cd demo/build/html && python3 -m http.server $(PORT)

css:
	cd theme-files && npm install
	cd theme-files && npm run build
	cp theme-files/dist/kentigern-modern.css kentigern/static/kentigern-modern.css
	cp theme-files/dist/kentigern.js kentigern/static/kentigern.js
	cp theme-files/dist/kentigern.js.LICENSE.txt kentigern/static/kentigern.js.LICENSE.txt
	cp theme-files/dist/*.woff theme-files/dist/*.woff2 kentigern/static/
	cp theme-files/darkmode.js kentigern/static/darkmode.js
