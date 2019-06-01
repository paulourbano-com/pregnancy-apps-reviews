var args = process.argv.slice(2);
app_id = args[0];
lang = args[1];
sort = args[2];

var gplay = require('google-play-scraper');
sort_var = gplay.sort.NEWEST;

if (sort == 'rating') {
	sort_var = gplay.sort.RATING;
} else if (sort == 'helpfulness') {
	sort_var = gplay.sort.HELPFULNESS;
}


t_var = args[3];
pages = parseInt(args[4]);

console.log('Pages: %d',  pages);

var i;
for (i = 0; i < pages; i++) { 
  console.log('---> Page %d', i);
  gplay.reviews({
  appId: app_id,
  page: i,
  sort: sort_var,
	  lang: lang,
	  throttle: t_var
}).then(console.log, console.log);
}

