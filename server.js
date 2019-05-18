var express = require('express');
var app = express();

app.use(express.static('public'))

app.listen(8080, function () {
  console.log('Example app listening on port 8080!');
  //call this app from https://<workspace name>-<user name>.c9users.io
});