const fs = require('fs');
const express = require("express");
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

// Define the folder path
var folderPath = 'C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/SAP ABAP COMPELETED';
var fileName = '';
// GET request to send JSON object
app.get('/', (req, res) => {

  const receivedData = req.body;
  console.log('Received data GET /', receivedData);

  // Read the index.html file
  fs.readFile('C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/SAP ABAP COMPELETED/node/index.html', 'utf-8', (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Internal Server Error');
      return;
    }

    // Set the response header
    res.writeHead(200, { 'Content-Type': 'text/html' });

    // Send the index.html content as the response
    res.write(data);
    res.end();
  });
});

app.get('/style.css', (req, res) => {
  // Read and serve the style.css file
  fs.readFile('C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/SAP ABAP COMPELETED/node/style.css', 'utf-8', (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Internal Server Error');
      return;
    }

    // Set the response header
    res.writeHead(200, { 'Content-Type': 'text/css' });

    // Send the style.css content as the response
    res.write(data);
    res.end();
  });
});

app.get('/script.js', (req, res) => {

  // Read and serve the style.css file
  fs.readFile('C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/SAP ABAP COMPELETED/node/script.js', 'utf-8', (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Internal Server Error');
      return;
    }

    // Set the response header
    res.writeHead(200, { 'Content-Type': 'application/javascript' });

    // Send the style.css content as the response
    res.write(data);
    res.end();
  });
});

// GET request to send JSON object and get file names
app.get('/getFileNames',
  (req, res) => {
    var response = { size: 0 };
    var localFolderPath = folderPath;

    if (fileName !== "") {
        localFolderPath = folderPath + '/' + fileName;
        folderPath = localFolderPath;
    }
    fs.readdir(localFolderPath, (err, files) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
        return;
      }
      else {
        var index = 1;
        files.forEach((file) => {
          response[index] = file;
          response["size"] = index;
          index = index + 1;
        });
      }
    });
    setTimeout(function () {
      console.log("response: ", response);
      res.json(response);
    }, 10);
});

// POST request to receive JSON object and updata folderPath
app.post('/', (req, res) => {
  const receivedData = req.body;
  console.log('Received data POST /', receivedData);

  folderPath = receivedData.folderPath;
  fileName = receivedData.fileName;
  const response = {
    message: 'Data received successfully! and updated folderPath',
    data: folderPath
  };
  res.json(response);
});

app.get('/home', (req, res) => {

  const receivedData = req.body;
  console.log('Received data GET /', receivedData);

  // Read the index.html file
  fs.readFile('C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/SAP ABAP COMPELETED/node/index.html', 'utf-8', (err, data) => {
    if (err) {
      res.writeHead(500, { 'Content-Type': 'text/plain' });
      res.end('Internal Server Error');
      return;
    }

    // Set the response header
    res.writeHead(200, { 'Content-Type': 'text/html' });

    // Send the index.html content as the response
    res.write(data);
    res.end();
  });
});

app.get('/file', (req, res) => {
  console.log("/file url is called");
  console.log(req.query.path);
  if (!(req.query.path === "")) {
    folderPath = req.query.path;
    console.log("new folder path", folderPath);

    var response = { size: 0 };
    // Process the received data...
    // Read the folder contents
    fs.readdir(folderPath, (err, files) => {
      if (err) {
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('Internal Server Error');
        return;
      }
      else {
        var index = 1;
        files.forEach((file) => {
          response[index] = file;
          response["size"] = index;
          index = index + 1;
        });
        console.log(response);
      }
    });
    setTimeout(function () {
      console.log("response: ", response);
      res.json(response);
    }, 10);
  }
}
);

// Define the port number
const port = 3001;

// Start the server and listen on the specified port
app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});