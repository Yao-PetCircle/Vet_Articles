const cheerio = require("cheerio");
const requestImageSize = require("request-image-size");
const https = require("node:https");
const fs = require("node:fs");
const sizeOf = require("image-size");

fs.readFile(
  "article/3-common-new-pet-problems.html",
  "utf8",
  async (err, data) => {
    if (err) {
      console.error(err);
      return;
    }
    const $ = cheerio.load(data);

    let url = $("img").attr("src");

    console.log(url);
    url = url.replace("www.petcircle.com.au", "storage.googleapis.com");
    https.get(url, function (response) {
      const chunks = [];
      response
        .on("data", function (chunk) {
          chunks.push(chunk);
        })
        .on("end", function () {
          const buffer = Buffer.concat(chunks);
          console.log(sizeOf(buffer));
        });
    });
  }
);
