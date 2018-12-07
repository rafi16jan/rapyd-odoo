process.chdir(__dirname)
process.on('uncaughtException', function(error){
    console.error(error);
});
var fs = require('fs');
var conf = "" +
"default_url = http://localhost\n" +
"port = 8069\n" +
"client_db = local\n" +
var modules_list = '';
var controllerst_list = '';
try {
    modules_list = require('child_process').execSync('cd modules && for module in $(find * -maxdepth 1 -mindepth 1 | grep modules.pyj | grep -v .pyj-cached); do echo "import $module" | sed "s/.pyj//g" | tr / .; done', {cwd: __dirname}).toString();
    controllers_list = require('child_process').execSync('cd modules && for module in $(find * -maxdepth 1 -mindepth 1 | grep controllers.pyj | grep -v .pyj-cached); do echo "import $module" | sed "s/.pyj//g" | tr / .; done', {cwd: __dirname}).toString();
    fs.writeFileSync(__dirname + '/modules/modules.pyj', modules_list)
    fs.writeFileSync(__dirname + '/modules/controllers.pyj', controllers_list)
    if (fs.existsSync(__dirname + '/app.conf') === false) {
        fs.writeFileSync(__dirname + '/app.conf', conf)
    }
} catch(error) {
    console.log(error)
}
conf = fs.readFileSync(__dirname + '/app.conf').toString()
if (conf !== '') {
    conf = conf.split(' =').join('=').split('= ').join('=').split('=').join('":"').split('\n').join('","');
    conf = '{"' + conf.slice(0, -2) + '}';
    conf = JSON.parse(conf);
    process.env = Object.assign(process.env, conf);
}
//process.env.RAPYDSCRIPT_IMPORT_PATH = 'modules/';
var command = process.execPath + ' ./node_modules/.bin/rapydscript -p modules/';
if (process.env.custom_modules !== undefined && process.env.custom_modules !== false) {
    //command += ':' + process.env.custom_modules + '/';
    process.env.RAPYDSCRIPT_IMPORT_PATH = process.env.custom_modules;
    try {
        if (fs.existsSync(process.env.custom_modules + '/__init__.pyj') === false) {
            fs.writeFileSync(process.env.custom_modules + '/__init__.pyj', '');
        }
        modules_list += require('child_process').execSync('cd ' + process.env.custom_modules + ' && for module in $(find * -maxdepth 1 -mindepth 1 | grep modules.pyj | grep -v .pyj-cached); do echo "import $module" | sed "s/.pyj//g" | tr / .; done', {cwd: __dirname}).toString();
        controllers_list += require('child_process').execSync('cd ' + process.env.custom_modules + ' && for module in $(find * -maxdepth 1 -mindepth 1 | grep controllers.pyj | grep -v .pyj-cached); do echo "import $module" | sed "s/.pyj//g" | tr / .; done', {cwd: __dirname}).toString();
        fs.writeFileSync(__dirname + '/modules/modules.pyj', modules_list);
        fs.writeFileSync(__dirname + '/modules/controllers.pyj', controllers_list);
    } catch(error) {
        console.log(error);
    }
}
var pipe;
command += '-x client.pyj';
pipe = 'inherit';
if (process.argv.indexOf('--clear-cache') !== -1) {
    command = 'rm -f */*.pyj-cached && ' + command;
}
result = require('child_process').execSync(command, {cwd: __dirname, stdio: pipe, env: process.env});
process.env.rapyd_client_js = result.toString();
require('child_process').execSync('python python/server.py', {cwd: __dirname + '/python', stdio: pipe, env: process.env});