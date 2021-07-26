const mysql = require('mysql2');
const express = require('express');
const bodyParser = require("body-parser");
 
/*apt-get install nodejs
apt-get install mariadb-server
apt-get install npm
npm install mysql2
npm install express
npm install body-parser
sudo npm install forever -g
mkdir myproject
cd myproject
npm init
nano index.js
mkdir static
nano ./static/index.html
mysql
CREATE DATABASE mytestdatabase;
USE mytestdatabase;
CREATE TABLE mytesttable (id int NOT NULL AUTO_INCREMENT, name varchar(20) NOT NULL, money int DEFAULT 0, PRIMARY KEY (id));
GRANT ALL PRIVILEGES ON *.* TO 'master'@'localhost' IDENTIFIED BY 'secret';
sudo su
[node | forever] index.js*/
var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'master',
  password : 'secret',
  database : 'mytestdatabase'
});
 
const app = express();
app.use(bodyParser.json());
connection.connect();
 
app.get('/', (req, res) => {
  res.sendfile('index.html', { root: __dirname + "/static" } );
});
 
app.post('/addUser', (req, res) => {
	console.log('added user: ');
	console.log(req.body);
	let name = req.body.name.replace(/^[0-9\s]*|[+*\r\n]/g, '');
	query = `INSERT INTO mytesttable (name, money) VALUES ('`+name+`', `+ Math.floor(1000*Math.random())+`);`;
	console.log(query);
	connection.query(query, function(err, results, fields) {
		console.log(err);
		console.log(results);
		res.json({'message': 'Lookup successful.', 'users':results});
	});
});
 
app.get('/getUsers', (req, res) => {
	console.log('Getting users.');
	query = `SELECT name, money FROM mytesttable;`;
	connection.query(query, function(err, results, fields) {
		console.log(results);
		res.json({'message': 'Lookup successful.', 'users':results});
	});
});
 
// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = 80;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});
 
 
 
 