from __future__ import annotations

import re

from pyanilist._query import ALL_MEDIA_QUERY, MEDIA_QUERY, RECOMMENDATIONS_QUERY, RELATIONS_QUERY


def test_media_query() -> None:
    # Make sure all variables are used
    # by testing that they are present twice, one for query and one for Media
    var_pattern = r"\$\w+"
    vars = re.findall(var_pattern, MEDIA_QUERY)
    vars_all_media = re.findall(var_pattern, ALL_MEDIA_QUERY)

    # Now check if every var in query also has a corresponding var in Media
    var_pattern2 = r"[a-z]\w+:"
    vars2 = re.findall(var_pattern2, MEDIA_QUERY)
    vars2_all_media = re.findall(var_pattern, ALL_MEDIA_QUERY)

    assert (
        len(set(vars))
        == len(vars) / 2
        == len(set(vars2))
        == len(vars2) / 2
        # ALL_MEDIA_QUERY has 2 extra vars (page and perPage)
        == len(set(vars_all_media)) - 2
        == (len(vars_all_media) / 2) - 2
        == len(set(vars2_all_media)) - 2
        == (len(vars2_all_media) / 2) - 2
    )


def test_media_fields_in_queries() -> None:
    fields = "id idMal type format status description season seasonYear episodes duration chapters volumes countryOfOrigin isLicensed source hashtag updatedAt bannerImage genres synonyms averageScore meanScore popularity isLocked trending favourites isAdult siteUrl trailer { id site thumbnail } title { romaji english native } tags { id name description category rank isGeneralSpoiler isMediaSpoiler isAdult userId } startDate { year month day } rankings { id rank type format year season allTime context } externalLinks { id url site siteId type language color icon notes isDisabled } endDate { year month day } coverImage { extraLarge large medium color } nextAiringEpisode { timeUntilAiring id episode airingAt } streamingEpisodes { title thumbnail url site }"

    assert fields in " ".join(field.strip() for field in MEDIA_QUERY.split())
    assert fields in " ".join(field.strip() for field in ALL_MEDIA_QUERY.split())
    assert fields in " ".join(field.strip() for field in RECOMMENDATIONS_QUERY.split())
    assert fields in " ".join(field.strip() for field in RELATIONS_QUERY.split())
