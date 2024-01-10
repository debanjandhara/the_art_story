Similarity Check : 
check the online xml with the xml file here, then if similarity = NO, download the xml in directory
and filter it... and vectorise it

run check_changed api --> to if merged not merged , merge vector

functions 
1) link parser xml
2) check_similarity from url_xml to base_xml
3) download_xml
4) vectorise
5) token_counter
6) query_api

tell cloud guy --> set cron job, using curl

similariry (call model --> last_checked update)
filter (call model --> last_modified updated, merged/not-merged --> not-merged)
vectorise (call model --> last_vectorised updated)

create api for
1) initiate refresh
2) download csv
3) fastbot

sitemap scrape
    store <li> in different lists --> artists, critics, etc. 
    for items in list , link_paerser_xml(), check similariry online v/s offline
        similarity()
            check_similarity(url)
                break type and artist
                // file exist or not
                    if not return flag = 1
                // similarity code here
                if not similar return flag = 1
                if flag = 1
                    store --> raw xml (store id in a id_var)
                    from id_var(artist) --> filter xml
                    vectorise()
        merge()
            rucursively_merge vector db
            and changed 'non merged to merged'
