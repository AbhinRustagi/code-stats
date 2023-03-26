const path = require("path");
const fs = require("fs");

(function () {
  const logsFolder = path.join("src", "logs");
  console.log(logsFolder);

  fs.readdir(logsFolder, (err, files) => {
    if (err) {
      console.error(String(err));
    } else {
      files.forEach((file) => {
        console.log(file);
      });
    }
  });
})();
