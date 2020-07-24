from sijax.helper import json

from app import config
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import requests
import re

class YtSearch:
    search_str = str
    search_url = str
    search_country = str

    def __init__(self, search_str, search_country):
        self.search_str = search_str
        self.search_country = search_country
        query_string = urllib.parse.urlencode({"search_query": self.search_str})
        self.search_url = config.Config.YT_SEARCH_PAGE + query_string

    def perform_search(self):
        # Request URL and Beautiful Parser
        headers = {"Accept-Language": self.search_country + ";q=0.5"}
        r = requests.get(self.search_url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        aid = soup.find('script', string=re.compile('ytInitialData'))
        format1 = str(aid.contents[0].split("window[\"ytInitialData\"] = ")[1])
        format2 = format1.split("};")[0].strip()
        extracted_josn_text = format2 + "}"
        video_results = json.loads(extracted_josn_text)
        item_section = \
            video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"][
                "contents"][0]["itemSectionRenderer"]["contents"]

        # init results
        results = []

        for item in item_section:
            res_dict = {}
            try:
                video_info = item["videoRenderer"]

                # set the duration
                vid_duration = video_info["lengthText"]["simpleText"]

                # Check duration length from incoming video
                duration_check = int(str(video_info["lengthText"]["simpleText"]).split(":")[0])
                if duration_check > 9:
                    continue

                # set initial data
                title = video_info["title"]["runs"][0]["text"]
                vid_id = video_info["videoId"]
                thumb_url = video_info["thumbnail"]["thumbnails"][0]["url"]
                views = video_info["shortViewCountText"]["simpleText"]

                # map to dict
                res_dict['vid_title'] = title
                res_dict['vid_thumbnail'] = thumb_url
                res_dict['vid_id'] = vid_id
                res_dict['vid_duration'] = vid_duration
                res_dict['vid_views'] = views

                # name & link
                results.append(res_dict)
            except KeyError:
                continue
        # OLD KEEP THIS AS THE HTML PARSER
        # item_section = all_product[0].select("ol.item-section > li")
        # print(len(all_product))

        # for item in item_section:
        #     res_dict = {}
        #
        #     vid_duration = item.find("span", {"class": "accessible-description"})
        #     vid_duration = vid_duration.text if vid_duration else "N/A"
        #     # check_dur = int(re.search(r'\d{2}:\d{2}', vid_duration))
        #     # if check_dur > 9:
        #     #     continue
        #
        #     _pri_attrs = item.find_all("div", {"class": "yt-lockup"})
        #     # check primary attributes
        #     if len(_pri_attrs) < 1 or not _pri_attrs[0].has_attr('data-context-item-id'):
        #         continue
        #
        #     # get attr values
        #     vid_id = item.select("div.yt-lockup")[0]['data-context-item-id']
        #     vid_title = item.select("div.yt-lockup-content > h3.yt-lockup-title > a.yt-uix-tile-link")[
        #         0].get_text()
        #
        #     # set the thumbnail
        #     _thumb_url = item.select("div.yt-thumb img")[0]['src']
        #     thumb_span=item.find("span", {"class": "yt-thumb-simple"})
        #     thumb_img=thumb_span.find_all("img")
        #     if thumb_img[0].has_attr('data-thumb'):
        #         _thumb_url = item.select("div.yt-thumb img")[0]['data-thumb']
        #
        #     # map to dict
        #     res_dict['vid_title'] = vid_title
        #     res_dict['vid_thumbnail'] = _thumb_url
        #     res_dict['vid_id'] = vid_id
        #     res_dict['vid_duration'] = vid_duration
        #
        #     # # name & link
        #     # product_name = item.find("a", {"class": "product__name"})
        #     results.append(res_dict)

        return results
