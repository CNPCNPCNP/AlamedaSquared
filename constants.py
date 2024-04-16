#CONSTANTS. Use all capitals to define global constants please
import re
from betfairlightweight import filters

WIN_MARKET_REGEX = re.compile(r'^R\d+$')
PRICE_PROJECTION = filters.price_projection(price_data = filters.price_data(ex_best_offers=True))
RUN_TIME_MINUTES = 840

#First value is BETR venue name, second value is betfair venue name
VENUES = {# Greyhound races
          "Gunnedah": "Gunnedah",
          "Nowra": "Nowra",
          "Warrnambool": "Warrnambool",
          "Maitland": "Maitland",
          "Angle Park": "Angle Park",
          "Doncaster": "Doncaster",
          "Romford": "Romford",
          "Albion Park": "Albion Park",
          "Warragul": "Warragul",
          "Grafton": "Grafton",
          "Gosford": "Gosford",
          "Taree": "Taree",
          "Gawler": "Gawler",
          "Manawatu": "Manawatu",
          "Capalaba": "Capalaba",
          "The Meadows": "The Meadows",
          "Richmond": "Richmond",
          "Traralgon": "Traralgon",
          "Addington": "Addington",
          "Cannington": "Cannington",
          "Shepparton": "Shepparton",
          "Horsham": "Horsham",
          "Casino": "Casino",
          "Ballarat": "Ballarat",
          "Dapto": "Dapto",
          "Hobart": "Hobart",
          "Temora": "Temora",
          "Murray Bridge Straight": "Murray Bridge",
          "Healesville": "Healesville",
          "Sandown Park": "Sandown Park",
          "Dubbo": "Dubbo",
          "The Gardens": "The Gardens",


          # Trots
          "Pinjarra": "Pinjarra",
          "Mildura": "Mildura",
          "Bendigo": "Bendigo",
          "Globe Derby": "Globe Derby",
          "Wagga": "Wagga",
          "Hamilton": "Hamilton",
          "Ascot Park": "Ascot Park",
          "Bunbury": "Bunbury",
          "Hamilton": "Hamilton",
          "Swan Hill": "Swan Hill",
          "Bathurst": "Bathurst",
          "Redcliffe": "Redcliffe",
          "Melton": "Melton",
          "Alexandra Park": "Alexandra Park",
          "Melton": "Melton",
          "Menangle": "Menangle",
          "Charlton": "Charlton",
          "Young": "Young",
          "Gloucester Park": "Gloucester Park",
          "Echuca": "Echuca",
          "Sapphire Coast": "Sapphire Coast",
          
          # Horse races
          "Geelong": "Geelong",
          "Murwillumbah": "Murwillumbah",
          "Newcastle": "Newcastle",
          "Le Croise Laroc": "Le Croise-Laroche",
          "Southwell": "Southwell",
          "Finger Lakes": "Finger Lakes",
          "Ludlow": "Ludlow",
          "Sedgefield": "Sedgefield",
          "Morphettville": "Morphettville",
          "Laurel Park": "Laurel Park",
          "Philadelphia Park": "Philadelphia",
          "Sandown": "Sandown",
          "Ascot": "Ascot",
          "Mountaineer Park": "Mountaineer Park",
          "Avondale": "Avondale",
          "Doomben": "Doomben",
          "Balaklava": "Balaklava",
          "Warwick Farm": "Warwick Farm",
          "Launceston": "Launceston",
          "Narromine": "Narromine",
          "Belmont": "Belmont",
          "Northam": "Northam",
          "Wyong": "Wyong",
          "Cairns": "Cairns",
          "Ipswich": "Ipswich",
          "Wanganui": "Wanganui",
          "Rosehill": "Rosehill",
          "Moe": "Moe",
          "Gold Coast": "Gold Coast",
          "Caulfield": "Caulfield",
          "Kembla Grange": "Kembla Grange",
          "Coonamble": "Coonamble",
          "Wagga Riverside": "Wagga",
          "Kempsey": "Kempsey",
          "Kilcoy": "Kilcoy",
          "Pioneer Park": "Alice Springs",
          "Geraldton": "Geraldton",
          "Townsville": "Townsville",
          "Ararat": "Ararat",
          "Tamworth": "Tamworth",
          "Mornington": "Mornington",
          "Mudgee": "Mudgee",
          "Randwich Kensington": "Randwick",
          "Moonee Valley": "Moonee Valley",
          "Mt Gambier": "Mount Gambier",
          "Mount Gambier": "Mount Gambier",
          "Sunshine Coast": "Sunshine Coast",
          "Pakenham": "Pakenham",
          "Stawell": "Stawell",
          "Albury": "Albury",
          "Rockhampton": "Rockhampton",
          "Toowoomba": "Toowoomba",
          "Darwin": "Darwin",
          "Esperance": "Esperance",
          "Werribee": "Werribee",
          "Bairnsdale": "Bairnsdale",
          "Hawkesbury": "Hawkesbury",
          "Murray Bridge": "Murray Bridge",
          "Gatton": "Gatton",
          "Mackay": "Mackay",
          "Port Pirie": "Port Pirie",
          "Yarra Valley": "Yarra Valley",
          "Devonport Synthetic": "Devonport",
          "Kilmore": "Kilmore",
          "Tuncurry": "Tuncurry",
          "Lismore": "Lismore",
          "Orange": "Orange",
          "Strathalbyn": "Strathalbyn",
          "Camperdown": "Camperdown",
          "Randwick": "Randwick",
          "Benalla": "Benalla",
          "Canterbury": "Canterbury",

          # US horse races have different format, need to scrape differently. Here for now
          #"Hawthorne": "Hawthorne",
          #"Delta Downs": "Delta Downs",
          #"Penn National": "Penn National",
          #"Remington Park": "Remington Park",
          #"Charles Town": "Charles Town",
          #"Zia Park": "Zia Park",
          #"Turf Paradise": "Turf Paradise",
          #"Golden Gate": "Golden Gate Fields",
          #"Philadelphia Park": "Philadelphia"
          }

AMERICAN_RACES = {"Hawthorne", 
                  "Delta Downs", 
                  "Penn National", 
                  "Remington Park", 
                  "Charles Town",
                  "Golden Gate Fields",
                  "Turf Paradise",
                  "Zia Park",
                  "Philadelphia",
                  "Mountaineer Park"}