'use strict';
var webpack = require("webpack")
var SaveAssetsJson = require("assets-webpack-plugin");
var path = require("path");

module.exports = {
    target: "web",
    devtool: "#source-map",
    bail: true,
    entry: {
        graphiql: "./frontend/graphql.entry.jsx",
        main: "./frontend/main.entry.jsx"
    },
    output: {
        path: path.join(__dirname, "main/static/"),
        filename: "[name].bundle.js"
    },
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /(node_modules|bower_components)/,
                loader: 'babel', // 'babel-loader' is also a legal name to reference
                query: {
                    presets: ['react', 'es2015'],
                    cacheDirectory: true
                }
            }
        ]
    },

    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(true),
        new webpack.optimize.DedupePlugin(),
        new webpack.optimize.UglifyJsPlugin({
            output: {
                comments: false
            },
            compress: {
                warnings: true,
                screw_ie8: true
            }
        }),
        new webpack.ProvidePlugin({
            'fetch': 'imports?this=>global!exports?global.fetch!whatwg-fetch'
        })
    ]
}