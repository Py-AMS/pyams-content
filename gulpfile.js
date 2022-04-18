
const { src, dest, task, watch, parallel } = require('gulp');

const clean = require('gulp-clean-css');
const rename = require('gulp-rename');
const replace = require('gulp-replace');
const sass = require('gulp-sass')(require('node-sass'));
const webpack = require('gulp-webpack');
const stream = require('webpack-stream');

const package = require('./package.json');


task('sass_dev', function() {
	return src('src/pyams_content/skin/resources/sass/pyams.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(replace('$version$', package.version))
		.pipe(rename(function(path) {
			path.basename += '-dev';
		}))
		.pipe(dest('src/pyams_content/skin/resources/css'))
});


task('sass', function() {
	return src('src/pyams_content/skin/resources/sass/pyams.scss')
		.pipe(sass().on('error', sass.logError))
		.pipe(replace('$version$', package.version))
		.pipe(clean())
		.pipe(dest('src/pyams_content/skin/resources/css'))
});


task('build_dev', function() {
	const config = require('./webpack-dev.js');
	return src('src/pyams_content/skin/resources/src/pyams-src.js')
		.pipe(stream(config), webpack)
		.pipe(replace('$version$', package.version))
		.pipe(dest('src/pyams_content/skin/resources/js'));
});


task('build', function() {
	const config = require('./webpack.js');
	return src('src/pyams_content/skin/resources/src/pyams-src.js')
		.pipe(stream(config), webpack)
		.pipe(replace('$version$', package.version))
		.pipe(dest('src/pyams_content/skin/resources/js'));
});


exports.sass_dev = task('sass_dev');
exports.sass = task('sass');

exports.build_dev = task('build_dev');
exports.build = task('build');


exports.default = function() {
	watch('src/pyams_content/skin/resources/sass/*.scss',
		parallel('sass_dev', 'sass', 'build_dev', 'build'));
	watch(['src/pyams_content/skin/resources/css/*.css',
		'src/pyams_content/skin/resources/src/*.js'],
		parallel('build_dev', 'build'));
};
