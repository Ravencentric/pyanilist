# Examples

!!! note
    These examples use `pyanilist.Anilist` but you can do the same thing with `pyanilist.AsyncAnilist` since they share the same methods

## Anilist ID

```py
from pyanilist import Anilist

media = Anilist().get(16498)

print(media.title.english)
"""
Attack on Titan
"""
```

## Search

```py
from pyanilist import Anilist

media = Anilist().search("Attack on titan")

print(media.format)
"""
ANIME
"""
print(media.title.romaji)
"""
Shingeki no Kyojin
"""
print(media.episodes)
"""
25
"""
```

## Search with constraints

```py
from pyanilist import Anilist, MediaSeason, MediaType, MediaStatus, MediaFormat
media = Anilist().search(
        "My Hero Academia",
        season=MediaSeason.SPRING,
        season_year=2016,
        type=MediaType.ANIME,
        format=MediaFormat.TV,
        status=MediaStatus.FINISHED,

)
print(media.title.romaji)
"""
Boku no Hero Academia
"""
print(media.start_date.iso_format())
"""
2016-04-03
"""
print(media.site_url)
"""
https://anilist.co/anime/21459
"""
```

## Related media

```py
from pyanilist import Anilist

media = Anilist().search("violet evergarden")

print(media.format)
"""
TV
"""

for relation in media.relations:
    print(f"{relation.title.romaji} ({relation.format}) - {relation.site_url}")
"""
Violet Evergarden: Kitto "Ai" wo Shiru Hi ga Kuru no Darou (OVA) - https://anilist.co/anime/101432
Violet Evergarden (NOVEL) - https://anilist.co/manga/97298
Violet Evergarden Gaiden: Eien to Jidou Shuki Ningyou (MOVIE) - https://anilist.co/anime/109190
Violet Evergarden CM (ONA) - https://anilist.co/anime/154164
"""
```

## Retries

Anilist API is flaky, sometimes it might return an error for a perfectly valid request. `pyanilist` handles this by simply retrying failed requests a specified number of times (default is 5) before raising an error. Every subsequent retry also adds an additional one-second delay between requests.

```py
from pyanilist import Anilist

# Configure the number of retries. Setting it to 1 basically disables retrying.
anilist = Anilist(retries=1)

media = anilist.search("violet evergarden")

print(f"{media.title.english} - {media.site_url}")
"""
Violet Evergarden - https://anilist.co/anime/21827
"""
```

## Client

`pyanilist` gives you direct access to the internal [`httpx.Client()`](https://www.python-httpx.org/api/#client) used to send the POST request.

```py
from pyanilist import Anilist

headers = {'user-agent': 'my-app/0.0.1'}

# You can pass any httpx.Client() keyword argument to Anilist()
anilist = Anilist(headers=headers)

media = anilist.get(105333)

print(media.title.english)
"""
Dr. STONE
"""
```