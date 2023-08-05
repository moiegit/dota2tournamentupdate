# dota2tournamentupdate
notifies my discord server for Tier 1 tournaments of Dota 2 for the next 24hours

Python Scraping Practice
Azure Function Practice
Github Repos Practice


I - Start by checking for ONGOING Tier 1 tournaments for Dota 2.
    - https://liquipedia.net/dota2/Main_Page
    - Tier 1 tournaments does not happen all the time. Sometimes, there is a 1 to 2 months of break before another T1 tournament commence

II - Go over the upcoming matches if a T1 tournament is found in step 1
    - https://liquipedia.net/dota2/Liquipedia:Upcoming_and_ongoing_matches
    - This list is long. It even hides some of the recently finished matches so it does return a huge amount of array data
    - Scrape for: 
        = Team 1
        = Team 2
        = Best of ?
        = Date and time of the match
        = Tournament name

III - Arrange and set it up to be sent on a discord server that updates its members if a Tier 1 Tournament is about to happen for the next 24 hours
    - invite code for the interested: https://discord.gg/27ej7MJJ
    - properly list the fetched/scraped data and notify the members at 8:00 AM if it triggers a return for Tier 1 Dota 2 tournaments

