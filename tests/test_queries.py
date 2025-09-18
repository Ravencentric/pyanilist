from __future__ import annotations

import pytest

from pyanilist._query import (
    ALL_MEDIA_QUERY,
    MEDIA_QUERY,
    MEDIA_QUERY_VARS_SNAKE_CASE_TO_ANILIST_CASE,
    RECOMMENDATIONS_QUERY,
    RELATIONS_QUERY,
)


def test_media_fields_in_queries() -> None:
    fields = "{ id idMal type format status description season seasonYear episodes duration chapters volumes countryOfOrigin isLicensed source hashtag updatedAt bannerImage genres synonyms averageScore meanScore popularity isLocked trending favourites isAdult siteUrl trailer { id site thumbnail } title { romaji english native } tags { id name description category rank isGeneralSpoiler isMediaSpoiler isAdult userId } startDate { year month day } rankings { id rank type format year season allTime context } externalLinks { id url site siteId type language color icon notes isDisabled } endDate { year month day } coverImage { extraLarge large medium color } nextAiringEpisode { timeUntilAiring id episode airingAt } streamingEpisodes { title thumbnail url site } }"  # noqa: E501
    media_query_fields = "$id: Int $idMal: Int $startDate: FuzzyDateInt $endDate: FuzzyDateInt $season: MediaSeason $seasonYear: Int $type: MediaType $format: MediaFormat $status: MediaStatus $episodes: Int $chapters: Int $duration: Int $volumes: Int $isAdult: Boolean $genre: String $tag: String $minimumTagRank: Int $tagCategory: String $licensedBy: String $licensedById: Int $averageScore: Int $popularity: Int $source: MediaSource $countryOfOrigin: CountryCode $isLicensed: Boolean $search: String $id_not: Int $id_in: [Int] $id_not_in: [Int] $idMal_not: Int $idMal_in: [Int] $idMal_not_in: [Int] $startDate_greater: FuzzyDateInt $startDate_lesser: FuzzyDateInt $startDate_like: String $endDate_greater: FuzzyDateInt $endDate_lesser: FuzzyDateInt $endDate_like: String $format_in: [MediaFormat] $format_not: MediaFormat $format_not_in: [MediaFormat] $status_in: [MediaStatus] $status_not: MediaStatus $status_not_in: [MediaStatus] $episodes_greater: Int $episodes_lesser: Int $duration_greater: Int $duration_lesser: Int $chapters_greater: Int $chapters_lesser: Int $volumes_greater: Int $volumes_lesser: Int $genre_in: [String] $genre_not_in: [String] $tag_in: [String] $tag_not_in: [String] $tagCategory_in: [String] $tagCategory_not_in: [String] $licensedBy_in: [String] $licensedById_in: [Int] $averageScore_not: Int $averageScore_greater: Int $averageScore_lesser: Int $popularity_not: Int $popularity_greater: Int $popularity_lesser: Int $source_in: [MediaSource] $sort: [MediaSort]"  # noqa: E501
    media_fields = "( id: $id idMal: $idMal startDate: $startDate endDate: $endDate season: $season seasonYear: $seasonYear type: $type format: $format status: $status episodes: $episodes chapters: $chapters duration: $duration volumes: $volumes isAdult: $isAdult genre: $genre tag: $tag minimumTagRank: $minimumTagRank tagCategory: $tagCategory licensedBy: $licensedBy licensedById: $licensedById averageScore: $averageScore popularity: $popularity source: $source countryOfOrigin: $countryOfOrigin isLicensed: $isLicensed search: $search id_not: $id_not id_in: $id_in id_not_in: $id_not_in idMal_not: $idMal_not idMal_in: $idMal_in idMal_not_in: $idMal_not_in startDate_greater: $startDate_greater startDate_lesser: $startDate_lesser startDate_like: $startDate_like endDate_greater: $endDate_greater endDate_lesser: $endDate_lesser endDate_like: $endDate_like format_in: $format_in format_not: $format_not format_not_in: $format_not_in status_in: $status_in status_not: $status_not status_not_in: $status_not_in episodes_greater: $episodes_greater episodes_lesser: $episodes_lesser duration_greater: $duration_greater duration_lesser: $duration_lesser chapters_greater: $chapters_greater chapters_lesser: $chapters_lesser volumes_greater: $volumes_greater volumes_lesser: $volumes_lesser genre_in: $genre_in genre_not_in: $genre_not_in tag_in: $tag_in tag_not_in: $tag_not_in tagCategory_in: $tagCategory_in tagCategory_not_in: $tagCategory_not_in licensedBy_in: $licensedBy_in licensedById_in: $licensedById_in averageScore_not: $averageScore_not averageScore_greater: $averageScore_greater averageScore_lesser: $averageScore_lesser popularity_not: $popularity_not popularity_greater: $popularity_greater popularity_lesser: $popularity_lesser source_in: $source_in sort: $sort )"  # noqa: E501

    assert fields in " ".join(field.strip() for field in MEDIA_QUERY.split())
    assert fields in " ".join(field.strip() for field in ALL_MEDIA_QUERY.split())

    assert media_query_fields in " ".join(field.strip() for field in MEDIA_QUERY.split())
    assert media_query_fields in " ".join(field.strip() for field in ALL_MEDIA_QUERY.split())

    assert media_fields in " ".join(field.strip() for field in MEDIA_QUERY.split())
    assert media_fields in " ".join(field.strip() for field in ALL_MEDIA_QUERY.split())

    assert fields in " ".join(field.strip() for field in RECOMMENDATIONS_QUERY.split())
    assert fields in " ".join(field.strip() for field in RELATIONS_QUERY.split())


@pytest.mark.parametrize(
    ("key", "expected"),
    [
        ("id", "id"),
        ("id_mal", "idMal"),
        ("start_date", "startDate"),
        ("end_date", "endDate"),
        ("season", "season"),
        ("season_year", "seasonYear"),
        ("type", "type"),
        ("format", "format"),
        ("status", "status"),
        ("episodes", "episodes"),
        ("chapters", "chapters"),
        ("duration", "duration"),
        ("volumes", "volumes"),
        ("is_adult", "isAdult"),
        ("genre", "genre"),
        ("tag", "tag"),
        ("minimum_tag_rank", "minimumTagRank"),
        ("tag_category", "tagCategory"),
        ("licensed_by", "licensedBy"),
        ("licensed_by_id", "licensedById"),
        ("average_score", "averageScore"),
        ("popularity", "popularity"),
        ("source", "source"),
        ("country_of_origin", "countryOfOrigin"),
        ("is_licensed", "isLicensed"),
        ("search", "search"),
        ("id_not", "id_not"),
        ("id_in", "id_in"),
        ("id_not_in", "id_not_in"),
        ("id_mal_not", "idMal_not"),
        ("id_mal_in", "idMal_in"),
        ("id_mal_not_in", "idMal_not_in"),
        ("start_date_greater", "startDate_greater"),
        ("start_date_lesser", "startDate_lesser"),
        ("start_date_like", "startDate_like"),
        ("end_date_greater", "endDate_greater"),
        ("end_date_lesser", "endDate_lesser"),
        ("end_date_like", "endDate_like"),
        ("format_in", "format_in"),
        ("format_not", "format_not"),
        ("format_not_in", "format_not_in"),
        ("status_in", "status_in"),
        ("status_not", "status_not"),
        ("status_not_in", "status_not_in"),
        ("episodes_greater", "episodes_greater"),
        ("episodes_lesser", "episodes_lesser"),
        ("duration_greater", "duration_greater"),
        ("duration_lesser", "duration_lesser"),
        ("chapters_greater", "chapters_greater"),
        ("chapters_lesser", "chapters_lesser"),
        ("volumes_greater", "volumes_greater"),
        ("volumes_lesser", "volumes_lesser"),
        ("genre_in", "genre_in"),
        ("genre_not_in", "genre_not_in"),
        ("tag_in", "tag_in"),
        ("tag_not_in", "tag_not_in"),
        ("tag_category_in", "tagCategory_in"),
        ("tag_category_not_in", "tagCategory_not_in"),
        ("licensed_by_in", "licensedBy_in"),
        ("licensed_by_id_in", "licensedById_in"),
        ("average_score_not", "averageScore_not"),
        ("average_score_greater", "averageScore_greater"),
        ("average_score_lesser", "averageScore_lesser"),
        ("popularity_not", "popularity_not"),
        ("popularity_greater", "popularity_greater"),
        ("popularity_lesser", "popularity_lesser"),
        ("source_in", "source_in"),
        ("sort", "sort"),
    ],
)
def test_media_query_vars_snake_case_to_anilist_case(key: str, expected: str) -> None:
    assert MEDIA_QUERY_VARS_SNAKE_CASE_TO_ANILIST_CASE[key] == expected
