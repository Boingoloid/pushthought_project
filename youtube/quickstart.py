from apiclient.discovery import build

YOUTUBE_READ_WRITE_SSL_SCOPE = \
    'https://www.googleapis.com/auth/youtube.readonly'
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

MISSING_CLIENT_SECRETS_MESSAGE = 'WARNING: Please configure OAuth 2.0'


def get_authenticated_service(args):
  return build(API_SERVICE_NAME, API_VERSION, developerKey='AIzaSyDrox7y7PqBoPM5fau2Wg2Gd-qyXk_G88U')

args = {'key': 'AIzaSyDrox7y7PqBoPM5fau2Wg2Gd-qyXk_G88U'}
service = get_authenticated_service(args)


def videos_list_by_id(id):
  results = service.videos().list(
      part='snippet',
      id=id
  ).execute()

  return results


def youtube_search(q, max_results):
    from youtube.quickstart import service

    search_response = service.search().list(
        q=q,
        part="id,snippet",
        maxResults=max_results
    ).execute()

    videos = []

    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                     search_result["id"]["videoId"]))

            program, created = models.Program.objects.get_or_create(
                url=search_result['url']
            )
            if created:
                program.title = search_result['']
                program.plot_outline = search_result['']
                program.image = search_result['']
                program.runtime = search_result['']
                program.type = 'webvideo'
                program.save()
