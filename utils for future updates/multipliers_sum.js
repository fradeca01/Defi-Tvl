const cheerio = require('cheerio')
const fs = require('fs')
let _ = require('lodash');

async function parse() {
    console.log('Parsing farms HTML...');
    // the input filename
    const htmlFilename = 'farms2.html';
    // read the HTML from disk
    const html = await fs.promises.readFile(htmlFilename);
    // parse the HTML with Cheerio
    const $ = cheerio.load(html);
    // for each of the shot divs, convert to JSON
    const divs = $('div.sc-hQYpqk.eDAkhI').toArray();
    // TODO: convert divs to shot JSON objects

    let farms = divs.map(div => {
        const $div = $(div);
        return $div.text()     
      });

    return farms
  }

async function main() {
    console.log('Starting...');

    farms = await parse();

    console.log(farms); 

    let farms1 = farms.map(m => Number(m.slice(0,-1)));

    // for(let i = 0; i < farms1.length; i++){
    //     console.log(farms1[i]);
    // }

    console.log("Total = " + _.sum(farms1));

    console.log('Done!');
  }

main();