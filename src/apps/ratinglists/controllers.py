import base64
import datetime
import gc
import io
import json
import logging
import os
import subprocess
import xml.etree.ElementTree as ET

from datetime import date
from datetime import timedelta
from io import BytesIO
from zipfile import ZipFile

import matplotlib as mplb
import matplotlib.pyplot as plt

from matplotlib.figure import Figure

from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render

from .models import PlayerProfile
from .models import Post
from .models import RatingList


def create_rating_list(post_pk):
    """
    Generate player profiles from a "post" file.
    """

    print("\n    Debugging create_rating_list()")

    # post = get_object_or_404(Post, id=post_pk)
    post = get_object_or_404(Post, pk=post_pk)

    uploaded_file = post.uploaded_file
    rating_list_zipped = ZipFile(uploaded_file, "r")
    rating_list_name = rating_list_zipped.namelist()[0]
    rating_date = get_rating_date(rating_list_name)
    rating_list_data = rating_list_zipped.read(rating_list_name)
    rating_list_file = BytesIO(rating_list_data)

    rating_list = RatingList()
    rating_list.release_date = rating_date
    rating_list.original_file_name = rating_list_name
    rating_list.save()

    federations = []
    for fed in settings.FIDE_FEDERATIONS:
        federations.append(fed["code"])

    # https://www.iditect.com/faq/python/using-python-iterparse-for-large-xml-files.html
    # https://web.archive.org/web/20201111201837/http://effbot.org/zone/element-iterparse.htm#incremental-parsing
    total_players_inserted = 0
    index = 1
    for event, elem in ET.iterparse(rating_list_file, events=("end",)):
        if elem.tag == "player":
            for player_detail in elem.iter('country'):
                if player_detail.text in federations:
                    player_profile = PlayerProfile()
                    player_profile.rating_list = rating_list
                    player_profile.rating_date = rating_date
                    for player_detail in elem.iter('fideid'):
                        player_profile.fideid = player_detail.text
                    for player_detail in elem.iter('name'):
                        player_profile.name = player_detail.text
                    for player_detail in elem.iter('rating'):
                        player_profile.rating = player_detail.text
                    for player_detail in elem.iter('country'):
                        player_profile.country = player_detail.text
                    for player_detail in elem.iter('sex'):
                        player_profile.sex = player_detail.text
                    for player_detail in elem.iter('birthday'):
                        if player_detail.text:
                            player_profile.birthday = int(player_detail.text)
                        else:
                            player_profile.birthday = player_detail.text
                    for player_detail in elem.iter('games'):
                        player_profile.games = int(player_detail.text)
                    player_profile.index = index
                    player_profile.slug = rating_date + "-" + str(index)
                    # player_profile.slug = player_profile.fideid + "-" + release_date
                    player_profile.save()
                    total_players_inserted = total_players_inserted + 1
            index = index + 1
            elem.clear()  # Free memory

    print("\n    Total player profiles inserted: ", total_players_inserted)

    rating_list.player_total = index
    rating_list.save()

    post.is_extracted = True
    post.unzipped_file_name = rating_list_name
    post.save()

    print("\n    Finishing create_rating_list()    \n\n")

    return rating_list


def create_fed_profile(fed, date):
    """
    Generate details of a federation from a particular rating list.
    """

    print("\n    Debugging create_fed_profile()")

    rating_list = get_object_or_404(RatingList, release_date=date)

    players = PlayerProfile.objects.filter(rating_date=date, country=fed)

    total_players = len(players)

    fed_profile = dict()

    fed_profile["name"] = fed
    fed_profile["date"] = date
    fed_profile["total_players"] = total_players

    print("\n    Finishing create_fed_profile()    \n\n")

    return fed_profile


def create_region_profile(name):

    print("\n    Debugging create_region_profile()")

    region = []

    for fed in settings.FIDE_FEDERATIONS:
        date = "2013-02-01"
        stats = []
        stats.append(fed["code"])
        while int(date[:4]) < 2027:
            players = PlayerProfile.objects.filter(rating_date=date, country=fed["code"])
            stats.append(len(players))
            date = str(int(date[:4]) + 1) + date[4:]
        region.append(stats)

    # matplotlib.use("svg")

    # x = ["2013", "2014", "2015", "2016"]
    # y = [region[0][1], region[0][2], region[0][3], region[0][4]]

    # appdocs/matplotlib/recipes/embedding-in-web-application.md
    # fig, ax = plt.subplots()
    fig = Figure()
    ax = fig.subplots()

    years = []
    for year in range(2013, 2027):
        years.append(year)

    for fed in region:
        ax.plot(years, fed[1:], label=fed[0])
        # ax.plot(years, d, label="Uganda")
        # plot(2013, 4, 'bo')
        # plot(2013, 9, 'go')

    ax.set_xlabel('Year')  # Add an x-label to the axes.
    ax.set_ylabel('Rated Players')  # Add a y-label to the axes.
    # ax.set_title("Rated Chess Players in Africa")  # Add a title to the axes.
    # ax.legend();  # Add a legend.

    # print(type(fig))
    # plt.show()
    # savefig('filename')
    # plt.savefig()

    # Save the image to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    chart_image = "data:image/png;base64," + data

    print("\n    Finishing create_region_profile()    \n\n")

    return (region, chart_image)


def create_region_profile_monthly(name):

    print("\n    Debugging create_region_profile_monthly()")

    region_monthly = []

    for fed in settings.FIDE_FEDERATIONS:
        date = "2013-02-01"
        stats = []
        stats.append(fed["code"])
        while int(date[:4]) < 2014:
            while int(date[5:7]) < 13:
                players = PlayerProfile.objects.filter(rating_date=date, country=fed["code"])
                stats.append(len(players))
                if int(date[6:7]) < 9:
                    date = date[:6] + str(int(date[6:7]) + 1) + date[7:]
                else:
                    date = date[:5] + str(int(date[6:7]) + 1) + date[7:]
            date = str(int(date[:4]) + 1) + "-01-01"
        region_monthly.append(stats)

    print("\n    Finishing create_region_profile_monthly()    \n\n")

    return region_monthly


def get_top_20_players(fed, date):


    federation = fed

    print("\n\n    Federation:", fed)

    print("\n\n    Rating Date:", date)

    players = PlayerProfile.objects.filter(rating_date=date, country=fed)
    players = players.exclude(name__icontains="Adam, Aslam")
    players = players.exclude(name__icontains="Ateka, Nathan")
    players = players.exclude(name__icontains="Andolo, Humphrey")
    players = players.exclude(name__icontains="Gateri, Martin")
    players = players.exclude(name__icontains="Makatia, Alex")
    players = players.exclude(name__icontains="Odiah, Isaac Babu")
    players = players.exclude(name__icontains="Lwanga, Solomon Lubega")
    players = players.exclude(name__icontains="Kiunga, Boniface Kathurima")
    players = players.exclude(name__icontains="Mowlid, Ahmed")
    players = players.exclude(name__icontains="Deng Achuoth, Atem")
    players = players.exclude(name__icontains="Shah, Krishi")
    players = players.exclude(name__icontains="Mahdi Abdi Yousuf")
    players = players.exclude(name__icontains="Oyagi, Arnold")
    players = players.exclude(name__icontains="Adan, Abdul Roba")
    players = players.exclude(name__icontains="Kangari Fredrick")
    players = players.exclude(name__icontains="Mugi, Edwin")
    players = players.exclude(name__icontains="Owoko, Henry")
    players = players.exclude(name__icontains="Mutugi Flabian")
    players = players.exclude(name__icontains="Nagda, Ankush")
    players = players.exclude(name__icontains="Mwangi, John Milton Kihara")
    players = players.exclude(name__icontains="Wangombe Mugo")
    players = players.exclude(name__icontains="Otanga, Ernest Emisiko")
    players = players.exclude(name__icontains="Habilov, Mushfig")
    players = players.exclude(name__icontains="Ateka, Nathan")
    players = players.exclude(name__icontains="Ateka, Nathan")
    players = players.order_by("-rating")

    all_players = players[:10]

    veterans = players
    veterans = veterans.exclude(birthday__icontains="202")
    veterans = veterans.exclude(birthday__icontains="201")
    veterans = veterans.exclude(birthday__icontains="200")
    veterans = veterans.exclude(birthday__icontains="199")
    veterans = veterans.exclude(birthday__icontains="1989")
    veterans = veterans.exclude(birthday__icontains="1988")
    veterans = veterans.exclude(birthday__icontains="1987")
    veterans = veterans[:10]

    youngbloods = players
    youngbloods = youngbloods.exclude(birthday=None)
    youngbloods = youngbloods.exclude(birthday__icontains="195")
    youngbloods = youngbloods.exclude(birthday__icontains="196")
    youngbloods = youngbloods.exclude(birthday__icontains="197")
    youngbloods = youngbloods.exclude(birthday__icontains="1980")
    youngbloods = youngbloods.exclude(birthday__icontains="1981")
    youngbloods = youngbloods.exclude(birthday__icontains="1982")
    youngbloods = youngbloods.exclude(birthday__icontains="1983")
    youngbloods = youngbloods.exclude(birthday__icontains="1984")
    youngbloods = youngbloods.exclude(birthday__icontains="1985")
    youngbloods = youngbloods[:10]

    ladies = players.filter(sex="F")
    ladies = ladies[:10]

    junior_boys = players.filter(sex="M")
    junior_boys = junior_boys.exclude(birthday=None)
    junior_boys = junior_boys.exclude(birthday__icontains="195")
    junior_boys = junior_boys.exclude(birthday__icontains="196")
    junior_boys = junior_boys.exclude(birthday__icontains="197")
    junior_boys = junior_boys.exclude(birthday__icontains="198")
    junior_boys = junior_boys.exclude(birthday__icontains="199")
    junior_boys = junior_boys.exclude(birthday__icontains="2000")
    junior_boys = junior_boys.exclude(birthday__icontains="2001")
    junior_boys = junior_boys.exclude(birthday__icontains="2002")
    junior_boys = junior_boys.exclude(birthday__icontains="2003")
    junior_boys = junior_boys.exclude(birthday__icontains="2004")
    junior_boys = junior_boys.exclude(birthday__icontains="2005")
    junior_boys = junior_boys.order_by("-rating")[:10]

    junior_girls = players.filter(sex="F")
    junior_girls = junior_girls.exclude(birthday=None)
    junior_girls = junior_girls.exclude(birthday__icontains="195")
    junior_girls = junior_girls.exclude(birthday__icontains="196")
    junior_girls = junior_girls.exclude(birthday__icontains="197")
    junior_girls = junior_girls.exclude(birthday__icontains="198")
    junior_girls = junior_girls.exclude(birthday__icontains="199")
    junior_girls = junior_girls.exclude(birthday__icontains="2000")
    junior_girls = junior_girls.exclude(birthday__icontains="2001")
    junior_girls = junior_girls.exclude(birthday__icontains="2002")
    junior_girls = junior_girls.exclude(birthday__icontains="2003")
    junior_girls = junior_girls.exclude(birthday__icontains="2004")
    junior_girls = junior_girls.exclude(birthday__icontains="2005")
    junior_girls = junior_girls.order_by("-rating")[:10]

    under_12_boys = players.filter(sex="M")
    under_12_boys = under_12_boys.exclude(birthday=None)
    under_12_boys = under_12_boys.exclude(birthday__icontains="195")
    under_12_boys = under_12_boys.exclude(birthday__icontains="196")
    under_12_boys = under_12_boys.exclude(birthday__icontains="197")
    under_12_boys = under_12_boys.exclude(birthday__icontains="198")
    under_12_boys = under_12_boys.exclude(birthday__icontains="199")
    under_12_boys = under_12_boys.exclude(birthday__icontains="200")
    under_12_boys = under_12_boys.exclude(birthday__icontains="2010")
    under_12_boys = under_12_boys.exclude(birthday__icontains="2011")
    under_12_boys = under_12_boys.exclude(birthday__icontains="2012")
    under_12_boys = under_12_boys.exclude(birthday__icontains="2013")
    under_12_boys = under_12_boys.order_by("-rating")[:10]

    under_12_girls = players.filter(sex="F")
    under_12_girls = under_12_girls.exclude(birthday=None)
    under_12_girls = under_12_girls.exclude(birthday__icontains="195")
    under_12_girls = under_12_girls.exclude(birthday__icontains="196")
    under_12_girls = under_12_girls.exclude(birthday__icontains="197")
    under_12_girls = under_12_girls.exclude(birthday__icontains="198")
    under_12_girls = under_12_girls.exclude(birthday__icontains="199")
    under_12_girls = under_12_girls.exclude(birthday__icontains="200")
    under_12_girls = under_12_girls.exclude(birthday__icontains="2010")
    under_12_girls = under_12_girls.exclude(birthday__icontains="2011")
    under_12_girls = under_12_girls.exclude(birthday__icontains="2012")
    under_12_girls = under_12_girls.exclude(birthday__icontains="2013")
    under_12_girls = under_12_girls.order_by("-rating")[:10]

    under_8 = players
    under_8 = under_8.exclude(birthday=None)
    under_8 = under_8.exclude(birthday__icontains="195")
    under_8 = under_8.exclude(birthday__icontains="196")
    under_8 = under_8.exclude(birthday__icontains="197")
    under_8 = under_8.exclude(birthday__icontains="198")
    under_8 = under_8.exclude(birthday__icontains="199")
    under_8 = under_8.exclude(birthday__icontains="200")
    under_8 = under_8.exclude(birthday__icontains="2010")
    under_8 = under_8.exclude(birthday__icontains="2011")
    under_8 = under_8.exclude(birthday__icontains="2012")
    under_8 = under_8.exclude(birthday__icontains="2013")
    under_8 = under_8.exclude(birthday__icontains="2014")
    under_8 = under_8.exclude(birthday__icontains="2015")
    under_8 = under_8.exclude(birthday__icontains="2016")
    under_8 = under_8.exclude(birthday__icontains="2017")
    under_8 = under_8.order_by("-rating")[:10]

    top_1960s = players
    top_1960s = top_1960s.exclude(birthday=None)
    top_1960s = top_1960s.filter(birthday__icontains="196")
    top_1960s = top_1960s.order_by("-rating")[:20]

    top_1970s = players
    top_1970s = top_1970s.exclude(birthday=None)
    top_1970s = top_1970s.filter(birthday__icontains="197")
    top_1970s = top_1970s.order_by("-rating")[:20]

    top_1980s = players
    top_1980s = top_1980s.exclude(birthday=None)
    top_1980s = top_1980s.filter(birthday__icontains="198")
    top_1980s = top_1980s.order_by("-rating")[:20]

    top_1990s = players
    top_1990s = top_1990s.exclude(birthday=None)
    top_1990s = top_1990s.filter(birthday__icontains="199")
    top_1990s = top_1990s.order_by("-rating")[:20]

    top_2000s = players
    top_2000s = top_2000s.exclude(birthday=None)
    top_2000s = top_2000s.filter(birthday__icontains="200")
    top_2000s = top_2000s.order_by("-rating")[:20]

    top_2010s = players
    top_2010s = top_2010s.exclude(birthday=None)
    top_2010s = top_2010s.filter(birthday__icontains="201")
    top_2010s = top_2010s.order_by("-rating")[:20]

    rating_date = datetime.datetime.fromisoformat(date)

    top_players = dict()

    top_players["rating_date"] = rating_date
    top_players["all_players"] = all_players
    top_players["veterans"] = veterans
    top_players["youngbloods"] = youngbloods
    top_players["ladies"] = ladies
    top_players["junior_boys"] = junior_boys
    top_players["junior_girls"] = junior_girls
    top_players["under_12_boys"] = under_12_boys
    top_players["under_12_girls"] = under_12_girls
    top_players["under_8"] = under_8
    top_players["top_1960s"] = top_1960s
    top_players["top_1970s"] = top_1970s
    top_players["top_1980s"] = top_1980s
    top_players["top_1990s"] = top_1990s
    top_players["top_2000s"] = top_2000s
    top_players["top_2010s"] = top_2010s

    return top_players


def convert_date(short_date):
    """e.g. convert the date dec25 to 2025-12-01"""

    months = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    iso_date = "20" + short_date[:-2] + "-" + months[short_date[3:]] + "-01"

    return iso_date


def get_rating_date(rating_list_file_name):
    """e.g. convert "standard_dec15frl_xml.zip" to "2015-12-01" """

    months = {
        "jan": "01",
        "feb": "02",
        "mar": "03",
        "apr": "04",
        "may": "05",
        "jun": "06",
        "jul": "07",
        "aug": "08",
        "sep": "09",
        "oct": "10",
        "nov": "11",
        "dec": "12",
    }

    rating_month = rating_list_file_name[9:-13]

    rating_year = rating_list_file_name[12:-11]

    rating_date = "20" + rating_year + "-" + months[rating_month] + "-" + "01"

    return rating_date


if __name__ == '__main__':

    print("\n    Ratinglists Controllers")

    print("\n\n")

