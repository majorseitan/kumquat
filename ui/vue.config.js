// https://github.com/vuejs/vue-cli/blob/dev/docs/config.md
module.exports = {
  lintOnSave: true,
    configureWebpack: {
	 devtool: "source-map"
    },
    devServer: {
	proxy : { "/repository": { "target" : "http://localhost:5000" , "secure" : "false" } }
    }
}
// bit of a hack
if(process.env.npm_lifecycle_event == 'build'){
    module.exports.configureWebpack.output = {
	path: __dirname + "/../static",
	publicPath : "static/"
    }
}
