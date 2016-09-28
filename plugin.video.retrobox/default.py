'''

/*
 * (C) Ashish Saxena <ashish@reak.in>
 * (C) 2016 REAK INFOTECH LLP
 *
 * The LICENSE file included with the project would govern the use policy for this code,
 * In case of missing LICENSE file the code will be treated as an Intellectual Property of the creator mentioned above,
 * All rights related to distribution, modifcation, reselling, use for commercial or private use of this code is terminated.
 *
 */

'''
'''
// Developed for Personal Entertainment
// Uses API and access from different servers, which is unauthorized
// Probably against the terms and conditions aswell


For personal usage only, The developer denies any responsibility related to usage. It was built as an educational project.


How to generate / add shows

		:: FOR HOTSTAR ::

		For Hotstar, Find your TV Show from the following link
		http://search.hotstar.com/AVS/besc?action=SearchContents&channel=PCTV&moreFilters=type:SERIES%3Blanguage:hindi%3B&query=*

		Find your show, by looking into the JSON, and find the contentID for it.
		Once you have the contentID, Please visit following link and replace {{contentID}}
		
		http://account.hotstar.com/AVS/besc?action=GetAggregatedContentDetails&channel=PCTV&contentId={{contentID}}

		
		Once the JSON opens up, look for categoryID, copy it down.
		So, now you have {{contentID}} and {{categoryID}} for your favourite show
		One more thing left is pickup the last(rightmost) 2 digits of {{contentID}}, it will be your {{pictureID}}
		// For example, if categoryID is 4278, {{pictureID}} will be 78
		
		Now, add the following
		-!- Please replace all variables {{variables}}, without the {{}} tags -!-
		
		## Copy from here ##
		title1="{{Name of your show}}"
		url{{serialnumber}}="http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId={{contentID}}&channel=PCTV"
		show_img{{serialnumber}}="http://media0-starag.startv.in/r1/thumbs/PCTV/{{pictureID}}/{{categoryID}}/PCTV-{{categoryID}}-vl.jpg"
		addDir(7, title{{serialnumber}}, url{{serialnumber}}, show_img{{serialnumber}}, False)
		## Copy till here ##
		
		
		Look for "Add More shows" tags and paste between them
		
		
		
		
		
		
		
		
		
		
		
		
		
		:: For OZEE Platform Channels ::
		
		http://api.android.zeeone.com/mobile/get/show/bhabi-ji-ghar-par-hai
		Gives show information

		http://api.android.zeeone.com/mobile/get/show_videos/bhabi-ji-ghar-par-hai/0/10/newest
		Gives the newest available episodes


		http://api.android.zeeone.com/mobile/get/show_video/bhabi-ji-ghar-par-hain-episode-291-april-11-2016-full-episode
		Provide the slug and it'll provide link with hmac


		Adding a show, find the slug or URL name from the ozee website
		and add this
		
		slug2 = "bhabi-ji-ghar-par-hai"
		smallimage2 = "http://akamai.vidz.zeecdn.com/ozee/shows/"+slug2+"/listing-image-small.jpg"
		episodeurl2 = "http://api.android.zeeone.com/mobile/get/show_videos/"+slug2+"/0/50/newest"
		addDir(51, slug2 , episodeurl2, smallimage2, False)
		
		Make sure you fix the serial so it doesn't interfere with any other.
		
		
		Happy TV Vieweing [without the ads ;)]


'''
import re, os, sys
import urllib
import urllib2
import json
import requests
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon
from addon.common.addon import Addon
import datetime
import time

addon_id = 'plugin.video.retrobox'
addon = Addon(addon_id, sys.argv)
Addon = xbmcaddon.Addon(addon_id)
debug = Addon.getSetting('debug')

language = (Addon.getSetting('langType')).lower()
perpage = (Addon.getSetting('perPage'))
moviessortType = (Addon.getSetting('moviessortType')).lower()
enableip = (Addon.getSetting('EnableIP'))
ipaddress = (Addon.getSetting('ipaddress'))
quality = (Addon.getSetting('qualityType')).lower()

dialog = xbmcgui.Dialog()


if moviessortType=='name':
	moviessortType='title+asc'
elif moviessortType=='newest':
	moviessortType='last_broadcast_date+desc'#,year+desc,title+asc'
else:
	moviessortType='counter+desc'
	
if (quality=='let me choose'):
	fold = False
else:
	fold = True

s=requests.Session()

def addon_log(string):
    if debug == 'true':
        xbmc.log("[plugin.video.retrobox-%s]: %s" %(addon_version, string))

def make_request(url):
    try:
		print 'enableip is', enableip
		if enableip=='true':
			headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch', 'Connection':'keep-alive', 'User-Agent':'AppleCoreMedia/1.0.0.12B411 (iPhone; U; CPU OS 8_1 like Mac OS X; en_gb)', 'X-Forwarded-For': ipaddress}
		else:
			headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', 'Accept-Encoding':'gzip, deflate, sdch', 'Connection':'keep-alive', 'User-Agent':'AppleCoreMedia/1.0.0.12B411 (iPhone; U; CPU OS 8_1 like Mac OS X; en_gb)'}
		# print 'url to fetch', url
		print 'headers are', headers
		response = s.get(url, headers=headers, cookies=s.cookies, verify=False)
		data = response.text
		return data
    except urllib2.URLError, e:    # This is the correct syntax
        print e
        ##sys.exit(1)


def new_menu():
	'''	
	title1="mere-angne-mein"
	url1="http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=4210&channel=PCTV"
	show_img1="http://media0-starag.startv.in/r1/thumbs/PCTV/78/4278/PCTV-4278-hs.jpg"
	addDir(7, title1, url1, show_img1, False)
	
	slug2 = "bhabi-ji-ghar-par-hai"
	smallimage2 = "http://akamai.vidz.zeecdn.com/ozee/shows/"+slug2+"/listing-image-small.jpg"
	episodeurl2 = "http://api.android.zeeone.com/mobile/get/show_videos/"+slug2+"/0/50/newest"
	addDir(51, slug2 , episodeurl2, smallimage2, False)
	
	title3="humko-tumse-ho-gaya-hai-pyaar-kya-karein"
	url3="http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=9268&channel=PCTV"
	show_img3="http://media0-starag.startv.in/r1/thumbs/PCTV/84/9384/PCTV-9384-hs.jpg"
	addDir(7, title3, url3, show_img3, False)
	
	title4="ishqbaaaz"
	url4="http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=9449&channel=PCTV"
	show_img4="http://media0-starag.startv.in/r1/thumbs/PCTV/67/9567/PCTV-9567-hs.jpg"
	addDir(7, title4, url4, show_img4, False)
	
	title5="jhalak-dikhhla-jaa-s09"
	url5="http://reak.in/ninja/kodi/jhalaks09.json"
	show_img5="http://kimg.voot.com/kimg/c5dd5c3fee9745d595c50b91b863c4ed_1280X720.jpg"
	addDir(61, title5, url5, show_img5, False)
	'''

	slug2 = "bhabi-ji-ghar-par-hai"
	smallimage2 = "http://akamai.vidz.zeecdn.com/ozee/shows/"+slug2+"/listing-image-small.jpg"
	episodeurl2 = "http://api.android.zeeone.com/mobile/get/show_videos/"+slug2+"/0/50/newest"
	addDir(51, slug2 , episodeurl2, smallimage2, False)
	
	title6="pokemon-gotta-catch-em-'all"
	url6="http://reak.in/ninja/kodi/pokemon.json"
	show_img6="http://www.flickeringmyth.com/wp-content/uploads/2014/07/Pokemon-logo.gif"
	addDir(61, title6, url6, show_img6, False)
	
	
	#title6="sony-mix-live"
	#url6="/home/ashish/.kodi/addons/plugin.video.retrobox/pokemon.json"
	#show_img6="https://en.wikipedia.org/wiki/Pok%C3%A9mon#/media/File:English_Pok%C3%A9mon_logo.svg"
	#addDir(61, title6, url6, show_img6, False)

	## Add more shows between these tags ##
	addDir(24, 'Star Sports', '', 'https://upload.wikimedia.org/wikipedia/en/0/01/STAR_Sports_Logo_New.jpg', False)
	
	addDir(101,'AajTak', '', "http://media2.intoday.in/aajtak/1.0.2/resources/images/logo.jpg", False)
	
	
	
	## Above this please ##

#	addDir(2, '[B][COLOR white]TV Shows[/COLOR][/B]', '', '','')
#	addDir(5, '[B][COLOR green]Movie Collections[/COLOR][/B]', '','', '')
#	addDir(24, '[B]Sports[/B]', '', '','')
#	addDir(12, '[B]Search[/B]', '', '','')
#	addDir(30, '[B][COLOR red]Old look (deprecated)[/COLOR][/B]', '','', '')
	

def ozee_get_episode():
	html = make_request(url)
	data = json.loads(html)
	for var in data:
		name = var['video_title']
		slug = var['slug']
		slug = "http://api.android.zeeone.com/mobile/get/show_video/"+slug
		image = var['video_image']
		addDir(52, name, slug, image, False)
		
'''
		#print row
		episodelink = row.a['href']
		episodeimage = row.img['src']
		episodename = row.img['title']
		if name in episodelink:
			addDir(52, episodename, episodelink, episodeimage, False)
'''
			
def ozee_play_episode():
	html = make_request(url)
	data = json.loads(html)
	name = data['title']
	playbackurl = data['playback_url']
	preurl = playbackurl.split("master")
	image = data['listing_image_small']
	html = make_request(playbackurl)
	links = html.splitlines()
	addDir(0, "[144] "+name, preurl[0]+links[4], image, isplayable=True)
	addDir(0, "[240] "+name, preurl[0]+links[6], image, isplayable=True)
	addDir(0, "[480] "+name, preurl[0]+links[8], image, isplayable=True)
	
def voot_get_episode(url):
	html = make_request(url)
	bobo = json.loads(html)
	for var in bobo:
		name = var['MediaName']
		url = var['URL']
		image = var['Pictures'][0]['URL']
		addDir(62, name, url, image, False)
		
def voot_play_episode(slug):
	html = make_request(slug)
	links = html.splitlines()
	addDir(0, "[144] "+name, links[4], image, isplayable=True)
	addDir(0, "[240] "+name, links[6], image, isplayable=True)
	addDir(0, "[480] "+name, links[8], image, isplayable=True)

def get_seasons():
	#print url
	html = make_request(url)
	#print html
	#data = html.decode('utf-8')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['contentInfo']:
		seasons = result['contentTitle']
		season_link = 'http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId='+str(result['categoryId'])+'&channel=PCTV'#'http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId='++'&channel=PCTV'#	
		season_img = ''#'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hcc.jpg'
		addDir(7, seasons, season_link, season_img, False)
			
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
		
def get_seasons_ep_links():
	print "get seasons ep links: "+url
	html = make_request(url)
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList']:
		for result2 in result['categoryList']:
			ep_titles = result2['categoryName']
			ep_links = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result2['categoryId'])+'&channel=PCTV'
			ep_images = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result2['urlPictures'])[-2:]+'/'+str(result2['urlPictures'])+'/PCTV-'+str(result2['urlPictures'])+'-hsea.jpg'
			addDir(8, ep_titles, ep_links, ep_images, False)
		
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('episodes', 'episode-view')	
	
def get_episodes():
	print "get_episodes: "+url
	html = make_request(url)
	#data = html.decode('utf-8')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['contentList']:
		fin_ep_titles = str(result['episodeNumber'])+' - '+result['episodeTitle'].encode('ascii', 'ignore')
		duration = result['duration']
		fin_ep_links = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&id='+str(result['contentId'])+'&type=VOD'
		fin_ep_images = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hs.jpg'
		addDir(9, fin_ep_titles, fin_ep_links, fin_ep_images,duration, fold)
		
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
	setView('episodes', 'episode-view')
	
def get_new_sports():
	html = make_request('http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=5962&channel=PCTV')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList'][0]['categoryList']:
		if '5967' not in str(result['categoryId']):
			if 'Popular in' not in result['contentTitle']:
				if 'masthead' in result['contentTitle']:
					title = 'Live Events (Praise the god and click)'
				else:
					title = result['contentTitle']
				sports_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result['categoryId'])+'&channel=PCTV'
				sports_img = ''
				addDir(14, title, sports_link, sports_img, False)
	
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True) 
	
def get_ss_event():
	# print 'ss url', url
	html = make_request(url)
	data = html
	html = json.loads(data)
	if 'ArrayContent' in url:
		for result in html['resultObj']['contentList']:
			title = result['contentTitle']
			duration = result['duration']
			event_link = 'http://getcdn.hotstar.com/AVS/besc?action=GetCDN&asJson=Y&channel=PCTV&id='+str(result['contentId'])+'&type=VOD'
			event_img = 'http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hl.jpg'
			addDir(9, title, event_link, event_img,duration, fold)
	else:
		for result in html['resultObj']['categoryList'][0]['categoryList']:
			title = result['contentTitle']
			event_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(result['categoryId'])+'&channel=PCTV'
			event_img = ''
			addDir(14, title, event_link, event_img, False)
	
	setView('episodes', 'episode-view')
	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
	
def get_collections():
	html = make_request('http://account.hotstar.com/AVS/besc?action=GetCatalogueTree&categoryId=558&channel=PCTV')
	data = html
	html = json.loads(data)
	for result in html['resultObj']['categoryList']:
		for subval in result['categoryList']:
			if language in subval['language'].lower():
				title = '[B][COLOR green]'+subval['categoryName']+'[/COLOR][/B]'
				col_link = 'http://account.hotstar.com/AVS/besc?action=GetArrayContentList&categoryId='+str(subval['categoryId'])+'&channel=PCTV'
				col_img='http://media0-starag.startv.in/r1/thumbs/PCTV/'+str(result['urlPictures'])[-2:]+'/'+str(result['urlPictures'])+'/PCTV-'+str(result['urlPictures'])+'-hs.jpg'
				addDir(10, title, col_link, col_img, False)

	xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=True)
	
def play_aajtak():
	#addDir(0, "[144] "+name, preurl[0]+links[4], image, isplayable=True)
	#addDir(0, "[240] "+name, preurl[0]+links[6], image, isplayable=True)
	
	addDir(0, "[144] AajTak Live News", "http://streamer6.vidgyor.com/aajtak/live5/chunks.m3u8", "http://media2.intoday.in/aajtak/1.0.2/resources/images/logo.jpg", isplayable=True)
	addDir(0, "[240] AajTak Live News", "http://streamer6.vidgyor.com/aajtak/live4/chunks.m3u8", "http://media2.intoday.in/aajtak/1.0.2/resources/images/logo.jpg", isplayable=True)
	addDir(0, "[360] AajTak Live News", "http://streamer6.vidgyor.com/aajtak/live3/chunks.m3u8", "http://media2.intoday.in/aajtak/1.0.2/resources/images/logo.jpg", isplayable=True)
	addDir(0, "[480] AajTak Live News", "http://streamer6.vidgyor.com/aajtak/live2/chunks.m3u8", "http://media2.intoday.in/aajtak/1.0.2/resources/images/logo.jpg", isplayable=True)
	addDir(0, "[720] AajTak Live News", "http://streamer6.vidgyor.com/aajtak/live1/chunks.m3u8", "http://media2.intoday.in/aajtak/1.0.2/resources/images/logo.jpg", isplayable=True)
	
def get_video_url():
    videos = []
    params = []
    html = make_request(url)
    # name = 'testing singham returns'
    # if 'testing' in name:
		# image = ''
    data = html
    html = json.loads(data)
    manifest1 = html['resultObj']['src']
    manifest1 = manifest1.replace('http://','https://')
    manifest1 = manifest1.replace('/z/','/i/')
    manifest1 = manifest1.replace('manifest.f4m', 'master.m3u8')
    if (quality=='highest'):
		manifest2 = manifest1.replace('1300,2000', '3000,4500')
		manifest_url = make_request(manifest2)
		# print manifest_url
		if 'EXTM3U' in manifest_url:
			matchlist2 = re.compile("BANDWIDTH=([0-9]+)[^\n]*\n([^\n]*)\n").findall(str(manifest_url))
			manifest1 = None
			if matchlist2:
				for (size, video) in matchlist2:
					if size:
						size = int(size)
					else:
						size = 0
					videos.append( [size, video] )
		else:
			manifest1 = manifest2.replace('3000,4500', '1300,2000')
    
    if manifest1:
		manifest_url = make_request(manifest1)
		if manifest_url:
			if (quality=='highest' or quality=='let me choose'):
				# matchlist2 = re.compile("BANDWIDTH=([0-9]+).*RESOLUTION[^\n]*\n([^\n]*)\n").findall(str(manifest_url))
				matchlist2 = re.compile("BANDWIDTH=([0-9]+)[^\n]*\n([^\n]*)\n").findall(str(manifest_url))
			elif (quality == '720p'):
				matchlist2 = re.compile("BANDWIDTH=(\d+).*x720[^\n]*\n([^n].*)").findall(str(manifest_url))
			elif (quality == '404p'):
				matchlist2 = re.compile("BANDWIDTH=(\d+).*x404[^\n]*\n([^n].*)").findall(str(manifest_url))
			else:
				matchlist2 = re.compile("BANDWIDTH=(\d+).*x360[^\n]*\n([^n].*)").findall(str(manifest_url))
			if matchlist2:
				for (size, video) in matchlist2:
					if size:
						size = int(size)
					else:
						size = 0
					videos.append( [size, video] )
		else:
			videos.append( [-2, match] )
    
    videos.sort(key=lambda L : L and L[0], reverse=True)
    cookieString = ""
    c = s.cookies
    i = c.items()
    for name2, value in i:
		cookieString+= name2 + "=" + value + ";"
    # print 'cookieString is', cookieString
	
    if (quality == 'let me choose'):
		print videos
		for video in videos:
			size = '[' + str(video[0]) + '] '
			# print 'video 1 is', video[1]
			# print 'size is', size
			# print 'name is', name
			# print 'ipaddress is', ipaddress
			# print 'image is', image
			if enableip=='true':
				addDir(0, size + name, video[1]+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress, image, isplayable=True)
			else:
				addDir(0, size + name, video[1]+"|Cookie="+cookieString, image, isplayable=True)
    else:
		if videos:
			raw3_start = videos[0][1]
			if enableip=='true':
				high_video = raw3_start+"|Cookie="+cookieString+"&X-Forwarded-For="+ipaddress
			else:
				high_video = raw3_start+"|Cookie="+cookieString
			print 'high_video is: ',high_video
			listitem =xbmcgui.ListItem(name)
			listitem.setProperty('mimetype', 'video/x-msvideo')
			listitem.setPath(high_video)
			# xbmc.executebuiltin("PlayMedia(%s)"%high_video)
			xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)
			# xbmc.Player().play(high_video, listitem)
			# sys.exit()
		else:
			movie_id = 'IP issue?'
			dialog.notification("No Video Links available", movie_id, xbmcgui.NOTIFICATION_INFO, 4000)

    setView('movies', 'movie-view')	
		
def setView(content, viewType):
        
    if content:
        xbmcplugin.setContent(int(sys.argv[1]), content)

    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_LABEL )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RATING )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_VIDEO_RUNTIME )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_GENRE )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_MPAA_RATING )		
		
def addDir(mode,name,url,image,duration="",isplayable=False):
	name = name.encode('utf-8', 'ignore')
	namenew = name.replace("-"," ")
	namenew = namenew.title()
	url = url.encode('utf-8', 'ignore')
	#image = image.encode('utf-8', 'ignore')

	if 0==mode:
		link = url
		print link
	else:
		link = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&image="+urllib.quote_plus(image)

	ok=True
	item=xbmcgui.ListItem(namenew, iconImage="DefaultFolder.png", thumbnailImage=image)
	item.setInfo( type="Video", infoLabels={ "Title": namenew, "Duration": duration } )
	## Adjust for OZEE systems - Search for listing jpg and replace fanart with other ##
	if 'vl.jpg' in image:
		image2 = image.replace('vl.jpg', 'hl.jpg')
		item.setArt({'fanart': image2})
	else:
		item.setArt({'fanart': image})
	if 'listing-image-small.jpg' in image:
		## Adjust for OZEE systems - Search for listing jpg and replace fanart with other ##
		image2 = image.replace('listing-image-small.jpg', 'feature-image.jpg')
		item.setArt({'fanart': image2})
	else:
		item.setArt({'fanart': image})
		
	isfolder=True
	if isplayable:
		item.setProperty('IsPlayable', 'true')
		isfolder=False
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=link,listitem=item,isFolder=isfolder)
	return ok
	
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

params=get_params()	
mode=None
name=None
url=None
image=None

try:
    mode=int(params["mode"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    image=urllib.unquote_plus(params["image"])
except:
    pass

if mode==None:
	new_menu()

if mode==3:
	print "test"
    #Insert bhabhiji function

if mode==6:
    #get_seasons()
	get_seasons_ep_links()

if mode==7:
    get_seasons_ep_links()

if mode==8:
    get_episodes()
    
if mode==9:
    get_video_url()
	
if mode==51:
	ozee_get_episode()

if mode==52:
	ozee_play_episode()
	
if mode==61:
	voot_get_episode(url)

if mode==62:
	voot_play_episode(url)
	
if mode==14:
	get_ss_event()
	
if mode==24:
	get_new_sports();
	
if mode==101:
	play_aajtak();

s.close()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))