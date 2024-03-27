from youtubesearchpython import VideosSearch


def search_youtube(query):
    videosSearch = VideosSearch(query, limit=2)
    res = videosSearch.result()
    results = res["result"]
    videos = []
    for val in range(len(results)):
        link = results[val]["link"]
        title = results[val]["title"]
        videos.append({"title": title, "link": link})
    return videos
