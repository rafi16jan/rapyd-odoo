process.chdir(__dirname);
require('../client.js');
require('fs').writeFileSync('./config.json', process.env.rapyd_config_json);
