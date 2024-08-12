// https://stackoverflow.com/questions/10049557/reading-all-files-in-a-directory-store-them-in-objects-and-send-the-object
// https://linuxhint.com/wait-function-finish-javascript/

// global store
let globalStore = [];

// Define the folder path
var folderPath = 'C:/Users/abhbhagw/OneDrive - Capgemini/Desktop/SAP ABAP COMPELETED';
var fileName = '';
const newFile = (
    file
) => `<span class="badge m-1 text-left text-white border" style="color:#FFFFFF">
        <a onclick="deleteFiles.apply(this)">${file}</a>
        </span>`;

runOnLoad = () => {

    const data = {
        folderPath: folderPath,
        fileName: fileName
    };

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Request failed.');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
        });

    fetch('/getFileNames', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Request failed.');
            }
            return response.json();
        })
        .then((data) => {
            console.log("get getFileNames res data", data);
            var length = data["size"];

            const htmlContainer = document.querySelector(".task__container");
            for (var index = 1; index <= length; index++) {
                const newFileData = newFile(data[index]);
                htmlContainer.insertAdjacentHTML("beforeend", newFileData);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
};

const deleteFiles = (event) => {
    event = window.event;
    ext = ["docx", 'txt', 'xls', 'doc'];
    if (event.target.textContent !== "") {
        fileName = event.target.textContent;
        const parts = fileName.split('.');
        const extension = parts[parts.length - 1];

        if (ext.includes(extension)) {
            console.log("not a folder",fileName);
            return;
        }
    }

    // Select the nodes to delete
    const nodesToDelete = document.getElementsByClassName('task__container');

    // Remove each node
    Array.from(nodesToDelete).forEach(node => {
        node.remove();
    });

    const data = {
        folderPath: folderPath,
        fileName: fileName
    };

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then((response) => {
            if (response.ok) {
                folderPath = folderPath + '/' + fileName;
            }
            else {
                throw new Error('Request failed.');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error:', error);
        });


    fetch('/getFileNames', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Request failed.');
            }
            return response.json();
        })
        .then((data) => {
            console.log("get getFileNames req data", data);
            var length = data["size"];

            const parentHtmlContainer = document.querySelector(".parent_task__container");

            if (parentHtmlContainer !== undefined) {
                parentHtmlContainer.insertAdjacentHTML("beforeend", `<div class="column task__container">
                </div>`);

                const htmlContainer = document.querySelector(".task__container");

                for (var index = 1; index <= length; index++) {
                    const newFileData = newFile(data[index]);
                    htmlContainer.insertAdjacentHTML("beforeend", newFileData);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
};