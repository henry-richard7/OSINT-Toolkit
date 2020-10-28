import requests
import json
import cfscrape
from msedge.selenium_tools import Edge, EdgeOptions
import html
from GPSPhoto import gpsphoto
from terminaltables import AsciiTable
from colored import fg, bg, attr

reset = attr('reset')
from art import text2art

runner = cfscrape.create_scraper()
default_color = fg("#23ccb3")
heading_color = fg("#2db57c")
content_color = fg('#a9b521')


def getIpInfo():
    ip = input(default_color + "Enter IP Address> " + reset)
    try:
        dirty_response = requests.get(f'https://censys.io/ipv4/{ip}/raw').text
        clean_response = dirty_response.replace('&#34;', '"')
        x = clean_response.split('<code class="json">')[1].split('</code>')[0]
        censys = json.loads(x)

        print(heading_color + "\n[+] Gathering Location Information from [censys]\n" + reset)
        print(heading_color + "\n--------------------- Location Info ----------------\n" + reset)
        print(content_color + "Country       : " + str(censys["location"]["country"]))
        print("Continent     : " + str(censys["location"]["continent"]))
        print("Country Code  : " + str(censys["location"]["country_code"]))
        print("Province      : " + str(censys["location"]["province"]))
        print("Latitude      : " + str(censys["location"]["latitude"]))
        print("Longitude     : " + str(censys["location"]["longitude"]) + reset)
        print(heading_color + "\n--------------------- Autonomous system ----------------\n" + reset)
        print(content_color + "Description   : " + str(censys["autonomous_system"]["description"]))
        print("Routed prefix : " + str(censys["autonomous_system"]["routed_prefix"]))
        print("Asn           : " + str(censys["autonomous_system"]["asn"]) + reset)
        print(heading_color + "\n---------------------------------------------------------\n" + reset)


    except:
        print("Unavailable")


def getMacInfo():
    mac = input(default_color + "Enter MAC Address> " + reset)
    url = f"https://macvendors.co/api/{mac}"

    try:
        result = requests.get(url).json()
        print(heading_color + "----------------------MAC Address Lookup------------" + reset)
        print()
        print(content_color + f"MAC        : {mac}")
        print(f"Company    : {result['result']['company']}\n"
              f"MAC Prefix : {result['result']['mac_prefix']}\n"
              f"Address    : {result['result']['address']}\n"
              f"Country    : {result['result']['country']}\n" + reset)
        print()
        print(heading_color + "----------------------------------------------------" + reset)
    except:
        print(fg("red") + f"[*] Nothing found for {mac}")


def macToLocation():
    mac = input(default_color + "Enter MAC Address> " + reset)
    locations = requests.get("https://api.mylnikov.org/wifi?v=1.1&bssid=" + mac).json()
    print(heading_color + "------------------MAC Address To Location--------------" + reset)
    print()
    if locations['result'] == 200:
        print(content_color + f"MAC  : {mac}")
        print(f"Lat  : {locations['data']['lat']} \n"
              f"Long : {locations['data']['lon']}" + reset)
        print()
        print(heading_color + "--------------------------------------------------" + reset)

    else:
        print(fg("red") + f"MAC  : {mac}")
        print("Location not Available" + reset)
        print()
        print(heading_color + "--------------------------------------------------" + reset)


def getTorrentDownloads():
    ip = input(default_color + "Enter IP Address> " + reset)
    url = f"https://api.antitor.com/history/peer/?ip={ip}&key=3cd6463b477d46b79e9eeec21342e4c7"
    res = runner.get(url).json()

    print(heading_color + f"[*] Getting Torrent Downloaded by the IP Address : {ip}.............!\n" + reset)
    if len(url) != 0:
        print()
        print(content_color + "ISP: " + res['isp'])
        print("Country: " + res['geoData']['country'])
        print("Latitude: " + str(res['geoData']['latitude']))
        print("Longitude: " + str(res['geoData']['longitude']) + "\n"+reset)
        for i in res['contents']:
            print(content_color+"Category:" + i['category'])
            print("Name:" + i['name'])
            print("Start:" + i['startDate'])
            print("End:" + i['endDate'])
            print("Size:" + str(i['torrent']['size']) + reset)
            print()
            print(heading_color + "--------------------------------------------------" + reset)
    else:
        print("Error: Something Went Wrong")
        print(heading_color + "--------------------------------------------------" + reset)


def checkEmailBreached():
    email = input(default_color + "Email Address> " + reset)
    print()
    url = f"https://haveibeenpwned.com/unifiedsearch/{email}"

    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('ignore-certificate-errors')
    options.add_argument("--log-level=OFF")
    driver = Edge(options=options, executable_path=r"WebDriver\msedgedriver.exe")
    driver.get(url)
    try:
        dirty_response = \
            driver.page_source.split(
                '<html><head></head><body><pre style="word-wrap: break-word; white-space: pre-wrap;">')[1]

        raw_json = dirty_response.split("</pre></body></html>")[0]

        res = json.loads(raw_json)
        driver.close()

        print(heading_color + "---------------------Check For Breached Email--------------" + reset)

        for i in range(len(res['Breaches'])):
            print(content_color + f"Name        : {res['Breaches'][i]['Name']}\n"
                                  f"Title       : {res['Breaches'][i]['Title']}\n"
                                  f"Domain      : {res['Breaches'][i]['Domain']}\n"
                                  f"Breached On : {res['Breaches'][i]['BreachDate']}\n{reset}"
                                  f"{heading_color}--------------------------------------\n{reset}")
        if res['Pastes'] is None:
            print(fg("red") + "[*] No Public Paste Found" + reset)
        else:
            print(heading_color + "[*] Public Paste Found\n" + reset)
            pastes = res["Pastes"]
            for i in range(len(pastes)):
                print(content_color + f"Source     : {pastes[i]['Source']}\n"
                                      f"Title      : {pastes[i]['Title']}\n"
                                      f"Date       : {pastes[i]['Date']}\n"
                                      f"EmailCount : {pastes[i]['EmailCount']}\n")
                if pastes[i]['Source'] == "Pastebin":
                    print(f"Paste URL  : https://pastebin.com/{pastes[i]['Id']}\n{reset}"
                          f"{heading_color}----------------------------------------------------{reset}")
    except:
        print(fg("red") + f"[*] The provided Email {email} is not breached!" + reset)
        pass


def findUserName():
    username = input(default_color + "Enter username> " + reset)
    print()

    website = ["Spotify", "Gravatar", "Facebook", "PlayStore", "Twitch", "Twitter", "VK", "Steam", "Instagram",
               "Myspace", "MyAnimeList", "Patreon", "Pinterest", "Pokemon Showdown", "Quora", "Reddit", "Roblox"]

    urls = ["https://open.spotify.com/user", "http://en.gravatar.com", "https://www.facebook.com",
            "https://play.google.com/store/apps/developer?id=", "https://www.twitch.tv", "https://mobile.twitter.com",
            "https://vk.com", "https://steamcommunity.com/id", "https://www.instagram.com", "https://myspace.com",
            "https://myanimelist.net/profile", "https://www.patreon.com", "https://www.pinterest.com",
            "https://pokemonshowdown.com/users", "https://www.quora.com/profile", "https://www.reddit.com/user",
            "https://www.roblox.com/user.aspx?username="]

    for i in range(len(urls)):
     try:
        if i == 3 or i == 16:
            res = requests.get(f"{urls[i]}{username}").status_code

        elif i == 15 or 5:
            res = runner.get(f"{urls[i]}/{username}").status_code

        elif i == 7:
            res1 = requests.get(f"{urls[i]}/{username}").text
            if "The specified profile could not be found" in res1:
                print(f"[*] {username} is not available in {website[i]}")
                continue
            else:
                print(f"[*] {username} is available in {website[i]} url: {urls[i]}/{username}")
                continue


        else:
            res = requests.get(f"{urls[i]}/{username}").status_code
        if res == 200:
            if i == 3 or i == 16:
                print(f"[*] {username} is available in {website[i]} url: {urls[i]}{username}")
            else:
                print(f"[*] {username} is available in {website[i]} url: {urls[i]}/{username}")
        else:
            print(f"[*] {username} is not available in {website[i]}")
     except:
         continue



def dnsMap():
    domain = input(default_color + "Enter Domain> " + reset)
    print()

    image = requests.get(f'https://dnsdumpster.com/static/map/{domain}.png')
    print(heading_color + "----------------------DNS MAP---------------------------" + reset)

    if image.status_code == 200:
        image_name = domain.replace(".com", "")
        with open(f'DNS Map\\{image_name}.png', 'wb') as f:
            f.write(image.content)
            print(content_color + f"\n[*] {image_name}.png DNS Map image stored to DNS Map directory" + reset)
        print(heading_color + "--------------------------------------------------" + reset)


    else:
        print(content_color + f"[*] No DNS Map was available for {domain}" + reset)
        print(heading_color + "--------------------------------------------------" + reset)


def dnslookup():
    host = input(default_color + "Enter Domain> " + reset)
    print()
    result = requests.get(f'http://api.hackertarget.com/dnslookup/?q={host}').text
    print(content_color + '\n' + result + "\n" + reset)


def PortScan():
    ip = input(default_color + "Enter Domain> " + reset)
    print()
    result = requests.get(f'http://api.hackertarget.com/nmap/?q={ip}').text
    print(content_color + '\n' + result + '\n' + reset)


def whois():
    choice = int(input("Type of Whois to perform:\n"
                       "1. For IP Address\n"
                       "2. For Domain\n"
                       "Your Choice> "))
    if choice == 1:
        ip = input("IP Address> ")
        print(heading_color + f"Fetching Whois for {ip}........" + reset)
        print()
        result = requests.get(f'https://who.is/whois-ip/ip-address/{ip}').text
        print(
            content_color + result.split('<div class="col-md-12 queryResponseBodyKey"><pre>')[1].split("</pre></div>")[
                0] + reset)
        print(heading_color + "--------------------------------------------------" + reset)

    elif choice == 2:
        domain = input("Domains> ")
        print()
        print(heading_color + f"[*] Fetching whois information for {domain}..................." + reset)
        print()
        result = runner.get(f"https://www.whois.com/whois/{domain}").text
        result = result.split(
            '</div><div class="clear"></div></div></div><div class="df-block-raw"><div class="df-heading">Raw Whois Data</div><pre class="df-raw" id="registrarData">')[
            1]
        result = result.split('</pre></div>')[0]
        result_decoded = html.unescape(result)
        print(content_color + result_decoded.replace("\n", "\n\n") + reset)
        print(heading_color + "--------------------------------------------------" + reset)


def getMetaDataPhoto():
    location = input(default_color + "Image Path> " + reset)
    data = gpsphoto.getGPSData(location)
    print()
    for tag in data.keys():
        print(f"{content_color}{tag}: {data[tag]}{reset}")


def help_table():
    commands_table = [["Index", "Action"],
                      ["1.", "Get IP information"],
                      ["2.", "Get MAC Address Information"],
                      ["3.", "Get physical address from BSSID or MAC Address"],
                      ["4.", "Get torrent download information for given IP Address"],
                      ["5.", "Check if given email ID is breached and publicly available"],
                      ["6.", "Find the given username in some popular social media sites"],
                      ["7.", "To download DNS Map for a given domain"],
                      ["8.", "To perform DNS Lookup (Using hackertarget API)"],
                      ["9.", "To Perform Port Scan (Using hackertarget API)"],
                      ["10.", "To perform whois lookup for given IP or Domain"],
                      ["11.", "To get Location Meta Data from Photos"],
                      ['0.', "Show Help"],
                      ["12", "Exit"]
                      ]
    table = AsciiTable(commands_table)
    table_color = fg("#66e887")
    print(table_color + table.table + reset)


art = text2art("OSINT Tool Kit v1", "varsity")
print(fg("#03fc0b") + art + reset)
print(f"{fg('#0ecf12')}Developed by Henry Richard J{reset}")
help_table()

while True:
    choice = int(input(default_color + "OSINT Tool Kits> " + reset))

    if choice == 00:
        help_table()

    elif choice == 12:
        break

    elif choice == 1:
        getIpInfo()

    if choice == 2:
        getMacInfo()

    elif choice == 3:
        macToLocation()

    elif choice == 4:
        getTorrentDownloads()

    elif choice == 5:
        checkEmailBreached()

    elif choice == 6:
        findUserName()

    elif choice == 7:
        dnsMap()

    elif choice == 8:
        dnslookup()

    elif choice == 9:
        PortScan()

    elif choice == 10:
        whois()

    elif choice == 11:
        getMetaDataPhoto()
