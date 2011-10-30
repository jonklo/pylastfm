pylastfm
========

Python bindings for the [Last.FM API](http://www.last.fm/api). The big
selling point is the memoization. For example, calls to get an artist's
similar artists only fetch from the API endpoint once.

Dependencies
------------

- python-dateutil

Usage
=====

So far, pylastfm only supports the operations that don't require user
authentication. It does support the important API points:

### Artists

The `Artist` class provides a number of static class functions:

	import last
	results = last.Artist.search('they might be giants')
	# results.totalResults => 59
	# results.artists => [<last.artist.Artist object>, ...]
	# Get a specific artist
	tmbg = last.Artist.get('they might be giants')
	# Get events from the artist
	events = last.Artist.getEvents('they might be giants', festivalsonly=1, limit=100)
	# Find images of the artist
	images = last.Artist.getImages('they might be giants')
	# And similar artists
	similar = last.Artist.getSimilar('they might be giants')
	# And top albums, tags and tracks
	last.Artist.getTopAlbums('they might be giants')
	last.Artist.getTopTags('they might be giants')
	last.Artist.getTopTracks('they might be giants')
	# Get the top artists
	last.Artist.top()

In addition, instance members automatically glean information from the
above API endpoints. Information is pulled lazily, but is stored when
it's absent, it's fetched automatically

	bnl = last.Artist.get('barenaked ladies')
	# Get BNL's images, bio, etc.
	bnl.images => [<last.image.Image object>, ...]
	bnl.bio => {'content': '...', 'summary': '...', ...}
	# This fetches from the API
	bnl.similar
	# This second access does not fetch from the API
	bnl.similar
	# Get the artist's top tracks
	bnl.tracks
	# And events...
	bnl.events
	# And albums...
	bnl.albums
