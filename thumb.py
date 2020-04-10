import tvdb

tvdb.authenticate(tvdb.apiauth)
a = tvdb.pagedget('/series/76156/episodes')
tvdb.getallthumbs(a,'./scrubs_thumbnails')
