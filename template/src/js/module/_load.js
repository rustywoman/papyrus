const _MODULE_NAME = 'LOAD';

module.exports.init = function(scriptName){
  return new Promise(
    (resolve, reject) => {
      document.addEventListener(
        'DOMContentLoaded',
        () => {
          console.log(`> ( fn.${_MODULE_NAME} ) ::: [ ${scriptName} ] is loaded.`);
          resolve();
        },
        false
      );
    }
  );
};
