import '../scss/common.scss';
import '../scss/index.scss';

const load = require('./module/_load');

(() => {
  load.init('index')
    .then(
      () => {}
    );
})();
