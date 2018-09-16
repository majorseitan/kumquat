all: ui/node_modules static/index.html

ui/node_modules:
	(cd ui;npm install)

static/index.html: ui/node_modules
	(cd ui; npm run build)

