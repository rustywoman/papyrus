import '../scss/common.scss';
import '../scss/template_2.scss';

const load = require('./module/_load');

(() => {
  load.init('template_2')
    .then(
      () => {}
    );
})();
