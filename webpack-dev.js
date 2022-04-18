
const path = require('path');
const webpack = require('webpack');

module.exports = {
	mode: 'development',
	entry: {
		'pyams': './src/pyams_content/skin/resources/src/pyams-src.js'
	},
	output: {
		path: path.resolve(__dirname, 'src', 'pyams_content', 'skin', 'resources', 'js'),
		filename: 'pyams-dev.js'
	},
	plugins: [
		new webpack.ProvidePlugin({
			$: 'jquery',
			jQuery: 'jquery',
			'window.jQuery': 'jquery'
		})
	],
	resolve: {
		alias: {
			'jquery': path.join(__dirname, 'node_modules', 'jquery', 'dist', 'jquery.js')
		}
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /(node_modules)/,
				use: {
					loader: 'babel-loader',
					options: {
						presets: ['@babel/preset-env']
					}
				}
			},
			{
				test: /\.css$/,
				use: [
					'style-loader',
					'css-loader'
				]
			}
		]
	},
	devtool: 'source-map'
}
