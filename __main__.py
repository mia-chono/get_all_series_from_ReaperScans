from bs4 import BeautifulSoup

import requests


def get_body_data(is_series: bool, page_number: int) -> dict:
    """ Generate the body data for the POST request """

    data = {
        "action": "madara_load_more",
        "page": page_number,
        "template": "madara-core/content/content-archive",
        "vars[paged]": "1",
        "vars[template]": "archive",
        "vars[sidebar]": "full",
        "vars[post_type]": "wp-manga",
        "vars[meta_query][relation]": "OR",
        "vars[post_status]": "publish",
        "vars[order]": "ASC",
    }
    if is_series:
        data.update({
            "vars[orderby]": "meta_value_num",
            "vars[meta_key]": "_latest_update",
            "vars[manga_archives_item_layout]": "big_thumbnail"
        })
    else:
        data.update({
            "vars[orderby]": "post_title",
            "vars[meta_query][0][0][key]": "_wp_manga_chapter_type",
            "vars[meta_query][0][0][value]": "manga",
            "vars[meta_query][0][relation]": "AND",
        })

    return data


def get_series(link: str, page_number: int = 0) -> BeautifulSoup:
    """ Get the series from the website by page number """

    is_series = "series" in link
    ajax_link = "https://reaperscans.fr/wp-admin/admin-ajax.php"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    headers = {
        'User-Agent': user_agent,
        'referer': link
    }
    response = requests.post(ajax_link, headers=headers, data=get_body_data(is_series, page_number))
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_all_webtoons() -> [str]:
    series = []
    link = "https://reaperscans.fr/webtoons/"
    i = 0
    while True:
        r = get_series(link, i)
        if not r.contents:
            break
        for x in r.select(".item-thumb.c-image-hover a"):
            series.append(x.attrs["href"])
        i += 1

    return series


def get_all_series() -> [str]:
    series = []
    link = "https://reaperscans.fr/series/"
    i = 0
    while True:
        r = get_series(link, i)
        if not r.contents:
            break
        for x in r.select(".item-thumb.c-image-hover a"):
            series.append(x.attrs["href"])
        i += 1

    return series


if __name__ != "__main__":
    print("not executed by main")
    exit(0)

webtoon_results = get_all_webtoons()
webtoon_results += get_all_series()

# save to file
with open("series.txt", "w") as f:
    for x in webtoon_results:
        f.write(x + "\n")
