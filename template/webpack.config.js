const path                 = require('path');
const express              = require('express');
const favicon              = require('serve-favicon');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin    = require('html-webpack-plugin');
const TerserPlugin         = require('terser-webpack-plugin');
const CompressionPlugin    = require('compression-webpack-plugin');
const webpack              = require('webpack');
const devServerPort        = 8080;
const distRootDir          = `${__dirname}/dist`;
const webpackDevServer     = {
  contentBase : distRootDir,
  stats       : 'normal',
  host        : '0.0.0.0',
  port        : devServerPort,
  before      : (app) => {
    app.use(
      favicon(
        path.join(__dirname, 'src/image', 'logo.ico')
      )
    );
    app.use(
      '/image',
      express.static(path.resolve(__dirname, 'src/image'))
    );
  }
};

module.exports = (env, options) => {
  // ---
  // 1. Argv : [ --t ]
  // ---
  let focusedFlg = false;
  let focusedBuildEntry = '';
  if(process.argv.length === 3){
    const tmpFocusedBuildEntry = process.argv[2].split('=');
    if(tmpFocusedBuildEntry.length === 2 && tmpFocusedBuildEntry[0] === '--t'){
      focusedBuildEntry = tmpFocusedBuildEntry[1];
    }
  }
  if(focusedBuildEntry !== ''){
    focusedFlg = true;
  }
  let buildMode = options.environment;
  let _entries = {};
  let assetsPublicPath = '/';
  let staticPath = `http://localhost:${devServerPort}`;
  let minimizer = [];
  let plugins = [];
  [
    'index',
    'template_1',
    'template_2'
  ].forEach(
    (pageName) => {
      _entries[pageName] = `./src/js/${pageName}.js`
    }
  );
  switch(buildMode){
    case 'remote':
      assetsPublicPath = 'http://127.0.0.1:3020/';
      minimizer = [
        new TerserPlugin(
          {
            extractComments : {
              condition: true,
              filename : () => {
                return 'LICENSE.txt';
              },
              banner : () => {
                return '';
              },
            },
            terserOptions   : {
              compress : {
                drop_console : true
              }
            }
          }
        )
      ];
      plugins = [
        new CompressionPlugin({
          test : /.*-common.(js|css)/i
        }),
        new MiniCssExtractPlugin({
          filename : 'css/[name].css'
        })
      ];
      break;
    default:
      buildMode = 'dev';
      plugins = [
        new MiniCssExtractPlugin({
          filename : 'css/[name].css'
        })
      ];
      break;
  }
  // Dynamic Webpack Config
  // ---
  const webpackConfig = {
    performance : {
      maxEntrypointSize : 888888,
      maxAssetSize      : 888888,
    },
    mode   : 'production',
    entry  : _entries,
    output : {
      path       : distRootDir,
      filename   : 'js/[name].js',
      publicPath : assetsPublicPath
    },
    optimization : {
      splitChunks : {
        cacheGroups : {
          styles : {
            name               : 'papyrus-common',
            test               : /common*.scss/,
            chunks             : 'all',
            minChunks          : 1,
            reuseExistingChunk : true,
            enforce            : true
          },
          scripts : {
            name               : 'papyrus-common',
            chunks             : 'initial',
            test               : /settings|src\/js\/module|src\/js\/lib|node_modules/,
            reuseExistingChunk : true,
            enforce            : true
          }
        }
      },
      minimizer   : minimizer
    },
    module : {
      rules : [
        {
          test : /\.pug$/,
          use  : [
            {
              loader  : 'pug-loader',
              options : {
                self : true
              }
            }
          ]
        },
        {
          test : /\.scss$/,
          use  : [
            { loader : MiniCssExtractPlugin.loader },
            { loader : 'css-loader' },
            { loader : 'sass-loader' }
          ]
        }
      ]
    },
    devServer : webpackDevServer,
    plugins   : plugins
  };
  // Complement `HTML`(pug) Plugin
  // ---
  if(webpackConfig.entry[focusedBuildEntry] === undefined){
    console.log(`\n[ FOCUS ] You will build all articles.\n`);
    focusedFlg = false;
  }else{
    console.log(`\n[ FOCUS ] You will build only "${focusedBuildEntry}".\n`);
  }
  if(focusedFlg){
    for(let buildEntry in webpackConfig.entry){
      if(buildEntry !== 'common'){
        if(
          buildEntry === 'index' ||
          buildEntry === focusedBuildEntry
        ){
          webpackConfig.plugins.push(
            new HtmlWebpackPlugin(
              {
                template    : './src/html/' + buildEntry + '.pug',
                filename    : buildEntry + '.html',
                inject      : true,
                chunks      : [buildEntry],
                staticPath  : assetsPublicPath,
                buildMode   : buildMode
              }
            )
          );
        }
      }
    }
  }else{
    for(let buildEntry in webpackConfig.entry){
      if(buildEntry !== 'common'){
        webpackConfig.plugins.push(
          new HtmlWebpackPlugin(
            {
              template    : './src/html/' + buildEntry + '.pug',
              filename    : buildEntry + '.html',
              inject      : true,
              chunks      : [buildEntry],
              staticPath  : assetsPublicPath,
              buildMode   : buildMode
            }
          )
        );
      }
    }
  }
  return webpackConfig;
};
