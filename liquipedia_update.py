import requests
import os
import pytz
from bs4 import BeautifulSoup as bs
from datetime import timezone, timedelta
from datetime import datetime as dt


urltournaments = 'https://liquipedia.net/dota2/Main_Page'
urlmatches = 'https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches'
urldiscord = 'https://discord.com/api/v9/channels/1137200272238706729/messages'


match_r = requests.get(urlmatches)
match_s = bs(match_r.content, 'html.parser')

tier1_tournaments = []
upcoming_matches = []
team_names = []
date_format = '%B %d, %Y - %H:%M %Z'
manila_tz = pytz.timezone('Asia/Manila')
current_time = dt.now(manila_tz)  
auth_token = os.getenv('discordauth')
auth = {
    'authorization': auth_token
}

#get tier 1 tournaments list to filter only the top tournaments available on the website
def get_tier1_tournaments():
    tournament_r = requests.get(urltournaments)
    tournament_s = bs(tournament_r.content, 'html.parser')
    tournament_list = tournament_s.find_all('ul', class_="tournaments-list")

    for tl in tournament_list:
        div_elements = tl.find_all('div', {'data-filter-category': "1"})
        if div_elements:
            
            for div_element in div_elements:
            # Print the content of each <div> element
                span_element = div_element.find('span', class_='tournaments-list-name')
                a_tag = span_element.find_all('a')

                if len(a_tag) >= 2:
                    second_a_tag = a_tag[1]  # Get the second <a> tag
                    tournament_name = second_a_tag.text.strip()
                    tier1_tournaments.append(tournament_name)
                else:
                    print("Not enough <a> tags within the <span> element to fetch the second one.")

        else:
            print("No <div> elements with data-filter-category='1' found on the page.")
    #print(tier1_tournaments)       
    return tier1_tournaments


#get all the upcoming matches available on the website
#takenote: the website shows even the concluded matches so make sure to filter them out of the list
# https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches
#convert datime to use my PH time zone
def get_matches():
    match_body = match_s.find_all('table', class_="wikitable wikitable-striped infobox_matches_content")

    for matches in match_body:
        left_team_elements = matches.find_all('td', class_='team-left')
        right_team_elements = matches.find_all('td', class_='team-right')
        
        match_versus = matches.find_all('td', class_='versus')
        match_date = matches.find_all('td', class_='match-filler')
        
        # For left teams
        for left_team_element in left_team_elements:
            a_tag = left_team_element.find('a')
            if a_tag:
                team_name = a_tag.attrs['title']
                team_names.append(team_name)
            else:
                team_names.append('To be Determined')

        # For right teams
        for right_team_element in right_team_elements:
            a_tag = right_team_element.find('a')
            if a_tag:
                team_name = a_tag.attrs['title']
                team_names.append(team_name)
            else:
                team_names.append('To be Determined')
        
        # For Best of ?       
        for mv_element in match_versus:
            a_tag = mv_element.find('abbr')
            if a_tag:
                mv = a_tag.attrs['title']
                team_names.append(mv)
            else:
                team_names.append('To be Determined')
        
        # For match date        
        for md_element in match_date:
            a_tag = md_element.find('span')
            if a_tag:
                md = a_tag.text.strip()

                # Create a timezone object for UTC
                utc_tz = pytz.timezone('UTC')

                # Convert string to datetime object and attach the UTC timezone object
                date_obj_utc = dt.strptime(md, date_format)
                date_obj_utc = utc_tz.localize(date_obj_utc)

                # Convert the datetime object to Manila timezone
                date_obj_manila = date_obj_utc.astimezone(manila_tz)

                # If date_obj is in the future, append item to filtered_list
                time_24hr_later = current_time + timedelta(hours=24)

                # If date_obj is in the future and less than 24 hours from now, append item to filtered_list
                if current_time < date_obj_manila < time_24hr_later:
                    md = date_obj_manila.strftime(date_format)
                    team_names.append(md)
                else:
                    team_names.append('To be Determined')
                    break


            else:
                team_names.append('To be Determined')
        
        # for Tournament name/tier
        for tourna in match_date:
            mt_element = tourna.find_all('a')
            if mt_element:
                last_anchor_tag = mt_element[-1]
                mt_value = last_anchor_tag.text
                team_names.append(mt_value)
            else:
                team_names.append('To be Determined')

# send daily updates on discord if there are any T1 tournaments and matches to expect
def post_discordmsg():
    if len(upcoming_matches) == 0:
        discordmsg = {
            'content': 'No TIER 1 matches available today: **' + current_time.strftime("%m/%d/%Y") + '**.'
        }
        requests.post(urldiscord, headers = auth, data = discordmsg)
    else:
        formatted_matches = [f'**{match[0]}** VS **{match[1]}** in a **{match[2]}**.\n Watch the game live this coming *{match[3]}*.\n'
                             for match in upcoming_matches]
        discordmsg = {
                'content': 'TIER 1 DOTA 2 Tournament matches available in 24 hours: **' + current_time.strftime("%m/%d/%Y") 
                + '**\n@here [WATCH IT LIVE - Dota 2 Twitch.tv](https://www.twitch.tv/directory/game/Dota%202)\n\n' 
                + '\n'.join(formatted_matches)
            }
        requests.post(urldiscord, headers = auth, data = discordmsg)

get_tier1_tournaments()
get_matches()

for i in range(0, len(team_names), 5):
    checktoprint = team_names[i:i+5]
    if checktoprint[3] == 'To be Determined':
        continue
    if team_names[i+4] in tier1_tournaments:
        upcoming_matches.append(team_names[i:i+5])

post_discordmsg()
# Print for testing
#print(tier1_tournaments)
#print(team_names)
#print(upcoming_matches)