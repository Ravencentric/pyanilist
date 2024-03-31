query_string = """
query ($id: Int, $season: MediaSeason, $seasonYear: Int, $type: MediaType, $format: MediaFormat, $status: MediaStatus, $search: String) {
  Media(id: $id, season: $season, seasonYear: $seasonYear, type: $type, format: $format, status: $status, search: $search) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    type
    format
    status
    defaultDescription: description(asHtml: false)
    htmlDescription: description(asHtml: true)
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    season
    seasonYear
    seasonInt
    episodes
    duration
    chapters
    volumes
    countryOfOrigin
    isLicensed
    source(version: 3)
    hashtag
    trailer {
      id
      site
      thumbnail
    }
    updatedAt
    coverImage {
      extraLarge
      large
      medium
      color
    }
    bannerImage
    genres
    synonyms
    averageScore
    meanScore
    popularity
    isLocked
    trending
    favourites
    tags {
      id
      name
      description
      category
      rank
      isGeneralSpoiler
      isMediaSpoiler
      isAdult
      userId
    }
    relations {
      edges {
        node {
          id
          idMal
          title {
            romaji
            english
            native
          }
          type
          format
          status
          defaultDescription: description(asHtml: false)
          htmlDescription: description(asHtml: true)
          startDate {
            year
            month
            day
          }
          endDate {
            year
            month
            day
          }
          season
          seasonYear
          seasonInt
          episodes
          duration
          chapters
          volumes
          countryOfOrigin
          isLicensed
          source(version: 3)
          hashtag
          trailer {
            id
            site
            thumbnail
          }
          updatedAt
          coverImage {
            extraLarge
            large
            medium
            color
          }
          bannerImage
          genres
          synonyms
          averageScore
          meanScore
          popularity
          isLocked
          trending
          favourites
          tags {
            id
            name
            description
            category
            rank
            isGeneralSpoiler
            isMediaSpoiler
            isAdult
            userId
          }
          isAdult
          nextAiringEpisode {
            id
            airingAt
            timeUntilAiring
            episode
            mediaId
          }
          externalLinks {
            id
            url
            site
            siteId
            type
            language
            color
            icon
            notes
            isDisabled
          }
          streamingEpisodes {
            title
            thumbnail
            url
            site
          }
          siteUrl
        }
        relationType(version: 2)
      }
    }
    characters {
      edges {
        node {
          id
          name {
            first
            middle
            last
            full
            native
          }
          image {
            large
            medium
          }
          description
          gender
          dateOfBirth {
            year
            month
            day
          }
          age
          bloodType
          siteUrl
        }
        role
      }
    }
    staff {
      nodes {
        id
        name {
          first
          middle
          last
          full
          native
          userPreferred
        }
        languageV2
        image {
          large
          medium
        }
        description
        primaryOccupations
        gender
        dateOfBirth {
          year
          month
          day
        }
        dateOfDeath {
          year
          month
          day
        }
        age
        yearsActive
        homeTown
        bloodType
        siteUrl
      }
      edges {
        role
      }
    }
    studios {
      edges {
        node {
          id
          name
          isAnimationStudio
          siteUrl
          favourites
        }
        isMain
      }
    }
    isAdult
    nextAiringEpisode {
      id
      airingAt
      timeUntilAiring
      episode
      mediaId
      media {
        id
      }
    }
    externalLinks {
      id
      url
      site
      siteId
      type
      language
      color
      icon
      notes
      isDisabled
    }
    streamingEpisodes {
      title
      thumbnail
      url
      site
    }
    rankings {
      id
      rank
      type
      format
      year
      season
      allTime
      context
    }
    siteUrl
  }
}

"""
