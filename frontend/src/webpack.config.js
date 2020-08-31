const path = require('path');

module.exports = {
  entry: './index.js',
  output: {
    filename: 'browser-bundle.js'
  },
  devtool: 'source-map',
  module: {
    loaders: [
      {
        test: /\.js*/,
        loader: 'babel-loader',
        exclude: /(node_modules|bower_components)/,
        query: {
          presets: ['@babel/react', ['@babel/preset-env', {
              useBuiltIns: 'entry'
          }]]
      },
      },
      {
        test: /\.css$/i,
        loaders: ['style-loader', 'css-loader']
      }
    ]
  },
  watchOptions: {
   poll: true
  }
};


