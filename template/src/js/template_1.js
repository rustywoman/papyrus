import '../scss/common.scss';
import '../scss/template_1.scss';

require('./lib/materialize.min');
const load = require('./module/_load');

(() => {
  load.init('template_1')
    .then(
      () => {}
    );
})();
