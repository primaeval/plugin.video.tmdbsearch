import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.tmdbsearch')
 
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import os

import requests
import re
import urllib,urlparse
import HTMLParser
from trakt import Trakt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'resources', 'lib'))
import tmdbsimple

if sys.version_info >= (2, 7):
    from json import loads, dumps
else:
    from simplejson import loads, dumps
    
_url = sys.argv[0]
_handle = int(sys.argv[1])

def get_background():
    addon_path = xbmcaddon.Addon().getAddonInfo("path")
    return os.path.join(addon_path, 'resources', 'img', "background.png")

def get_icon_path(icon_name):
    addon_path = xbmcaddon.Addon().getAddonInfo("path")    
    return os.path.join(addon_path, 'resources', 'img', icon_name+".png")

def get_genre_icon(genre):
    icons = {
    "Any":"genre_any",
    "Action":"genre_action",
    "Adventure":"genre_adventure",
    "Animation":"genre_animation",
    "Biography":"genre_biography",
    "Comedy":"genre_comedy",
    "Crime":"genre_crime",
    "Documentary":"genre_documentary",
    "Drama":"genre_drama",
    "Family":"genre_family",
    "Fantasy":"genre_fantasy",
    "Film Noir":"genre_film_noir",
    "Game show":"genre_game_show",
    "History":"genre_history",
    "Horror":"genre_horror",
    "Music":"genre_music",
    "Musical":"genre_musical",
    "Mystery":"genre_mystery",
    "News":"genre_news",
    "Reality TV":"genre_reality_tv",
    "Romance":"genre_romance",
    "Sci-Fi":"genre_sci_fi",
    "Sport":"genre_sport",
    "Talk Show":"genre_talk_show",
    "Thriller":"genre_thriller",
    "War":"genre_war",
    "Western":"genre_western"
    }
    if genre in icons:
        return get_icon_path(icons[genre])
    return "DefaultVideo.png"

def get_server(server_select):
    server_dict = {"Original Title":"akas",
    "Normal":"www"}
    return server_dict[server_select]

def get_sort(sort_select):
    return sort_select
    sort_dict = {"Any":"Any",
    "Moviemeter,Asc":"moviemeter,asc",
    "Moviemeter,Desc":"moviemeter,desc",
    "Alpha,Asc":"alpha,asc",
    "Alpha,Desc":"alpha,desc",
    "User Rating,Asc":"user_rating,asc",
    "User Rating,Desc":"user_rating,desc",
    "Num Votes,Asc":"num_votes,asc",
    "Num Votes,Desc":"num_votes,desc",
    "Boxoffice Gross US,Asc":"boxoffice_gross_us,asc",
    "Boxoffice Gross US,Desc":"boxoffice_gross_us,desc",
    "Runtime,Asc":"runtime,asc",
    "Runtime,Desc":"runtime,desc",
    "Year,Asc":"year,asc",
    "Year,Desc":"year,desc",
    "Release Date US,Asc":"release_date_us,asc",
    "Release Date US,Desc":"release_date_us,desc",
    "My Ratings":"my_ratings",
    "My Ratings,Asc":"my_ratings,asc"}
    return sort_dict[sort_select]

def get_color(color_select):
    color_dict = {"Any":"Any",
    "Color":"color",
    "Black and White":"black_and_white",
    "Colorized":"colorized",
    "ACES":"aces"}
    return color_dict[color_select]
    
def get_certificate(certificate_select):
    certificate_dict = {"Any":"Any",
    "US:G":"us:g",
    "US:PG":"us:pg",
    "US:PG_13":"us:pg_13",
    "US:R":"us:r",
    "US:NC_17":"us:nc_17",
    "GB:U"  :"gb:u"  ,
    "GB:PG" :"gb:pg" ,
    "GB:12" :"gb:12" ,
    "GB:12A":"gb:12a",
    "GB:15" :"gb:15" ,
    "GB:18" :"gb:18" ,
    "GB:R18":"gb:r18",
    }
    return certificate_dict[certificate_select]

def get_company(companies_select):
    companies_dict = {"Any":"Any",
    "Fox":"fox",
    "Columbia":"columbia",
    "Dreamworks":"dreamworks",
    "MGM":"mgm",
    "Paramount":"paramount",
    "Universal":"universal",
    "Disney":"disney",
    "Warner":"warner"}
    return companies_dict[companies_select]

def get_production_status(production_status_select):
    production_status_dict = {"Any":"*",
    "Released":"released",
    "Post Production":"post production",
    "Filming":"filming",
    "Pre Production":"pre production",
    "Completed":"completed",
    "Script":"script",
    "Optioned Property":"optioned property",
    "Announced":"announced",
    "Treatment Outline":"treatment outline",
    "Pitch":"pitch",
    "Turnaround":"turnaround",
    "Abandoned":"abandoned",
    "Delayed":"delayed",
    "Indefinitely Delayed":"indefinitely delayed",
    "Active":"active",
    "Unknown":"unknown"}
    return production_status_dict[production_status_select]

def get_group(groups_select):
    groups_dict = {"Any":"*",
    "Top 100":"top_100",
    "Top 250":"top_250",
    "Top 1000":"top_1000",
    "Now Playing Us":"now-playing-us",
    "Oscar Winners":"oscar_winners",
    "Oscar Best Picture Winners":"oscar_best_picture_winners",
    "Oscar Best Director Winners":"oscar_best_director_winners",
    "Oscar Nominees":"oscar_nominees",
    "Emmy Winners":"emmy_winners",
    "Emmy Nominees":"emmy_nominees",
    "Golden Globe Winners":"golden_globe_winners",
    "Golden Globe Nominees":"golden_globe_nominees",
    "Razzie Winners":"razzie_winners",
    "Razzie Nominees":"razzie_nominees",
    "National Film Registry":"national_film_registry",
    "Bottom 100":"bottom_100",
    "Bottom 250":"bottom_250",
    "Bottom 1000":"bottom_1000"}
    return groups_dict[groups_select]

def get_genre(genres_select):
    genres_dict = {
    "Any":"",
    "None":"",
    'Mystery': 9648,
    'Romance': 10749,
    'Family': 10751,
    'Science Fiction': 878,
    'Horror': 27,
    'Thriller': 53,
    'Crime': 80,
    'Drama': 18,
    'Fantasy': 14,
    'Western': 37,
    'Animation': 16,
    'Music': 10402,
    'Adventure': 12,
    'Foreign': 10769,
    'Action': 28,
    'Comedy': 35,
    'Documentary': 99,
    'War': 10752,
    'TV Movie': 10770,
    'History': 36}
    return genres_dict[genres_select]

def get_title_type(title_type_select):
    title_type_dict = {
    'Movie':'movie',
    'TV':'tv',
    }
    return title_type_dict[title_type_select]

def get_languages(languages_select):
    languages_dict = {"Any":"*",
    "Arabic":"ar",
    "Bulgarian":"bg",
    "Chinese":"zh",
    "Croatian":"hr",
    "Dutch":"nl",
    "English":"en",
    "Finnish":"fi",
    "French":"fr",
    "German":"de",
    "Greek":"el",
    "Hebrew":"he",
    "Hindi":"hi",
    "Hungarian":"hu",
    "Icelandic":"is",
    "Italian":"it",
    "Japanese":"ja",
    "Korean":"ko",
    "Norwegian":"no",
    "Persian":"fa",
    "Polish":"pl",
    "Portuguese":"pt",
    "Punjabi":"pa",
    "Romanian":"ro",
    "Russian":"ru",
    "Spanish":"es",
    "Swedish":"sv",
    "Turkish":"tr",
    "Ukrainian":"uk",
    "Abkhazian":"ab",
    "Aboriginal":"qac",
    "Ach&#xE9;":"guq",
    "Acholi":"qam",
    "Afrikaans":"af",
    "Aidoukrou":"qas",
    "Akan":"ak",
    "Albanian":"sq",
    "Algonquin":"alg",
    "American Sign Language":"ase",
    "Amharic":"am",
    "Apache languages":"apa",
    "Aragonese":"an",
    "Aramaic":"arc",
    "Arapaho":"arp",
    "Armenian":"hy",
    "Assamese":"as",
    "Assyrian Neo-Aramaic":"aii",
    "Athapascan languages":"ath",
    "Australian Sign Language":"asf",
    "Awadhi":"awa",
    "Aymara":"ay",
    "Azerbaijani":"az",
    "Bable":"ast",
    "Baka":"qbd",
    "Balinese":"ban",
    "Bambara":"bm",
    "Basque":"eu",
    "Bassari":"bsc",
    "Belarusian":"be",
    "Bemba":"bem",
    "Bengali":"bn",
    "Berber languages":"ber",
    "Bhojpuri":"bho",
    "Bicolano":"qbi",
    "Bodo":"qbh",
    "Bosnian":"bs",
    "Brazilian Sign Language":"bzs",
    "Breton":"br",
    "British Sign Language":"bfi",
    "Burmese":"my",
    "Cantonese":"yue",
    "Catalan":"ca",
    "Central Khmer":"km",
    "Chaozhou":"qax",
    "Chechen":"ce",
    "Cherokee":"chr",
    "Cheyenne":"chy",
    "Chhattisgarhi":"hne",
    "Cornish":"kw",
    "Corsican":"co",
    "Cree":"cr",
    "Creek":"mus",
    "Creole":"qal",
    "Creoles and pidgins":"crp",
    "Crow":"cro",
    "Czech":"cs",
    "Danish":"da",
    "Dari":"prs",
    "Desiya":"dso",
    "Dinka":"din",
    "Djerma":"qaw",
    "Dogri":"doi",
    "Dyula":"dyu",
    "Dzongkha":"dz",
    "East-Greenlandic":"qbc",
    "Eastern Frisian":"frs",
    "Egyptian (Ancient)":"egy",
    "Esperanto":"eo",
    "Estonian":"et",
    "Ewe":"ee",
    "Faliasch":"qbg",
    "Faroese":"fo",
    "Filipino":"fil",
    "Flemish":"qbn",
    "Fon":"fon",
    "French Sign Language":"fsl",
    "Fulah":"ff",
    "Fur":"fvr",
    "Gaelic":"gd",
    "Galician":"gl",
    "Georgian":"ka",
    "German Sign Language":"gsg",
    "Grebo":"grb",
    "Greek, Ancient (to 1453)":"grc",
    "Greenlandic":"kl",
    "Guarani":"gn",
    "Gujarati":"gu",
    "Gumatj":"gnn",
    "Gunwinggu":"gup",
    "Haitian":"ht",
    "Hakka":"hak",
    "Haryanvi":"bgc",
    "Hassanya":"qav",
    "Hausa":"ha",
    "Hawaiian":"haw",
    "Hmong":"hmn",
    "Hokkien":"qab",
    "Hopi":"hop",
    "Iban":"iba",
    "Ibo":"qag",
    "Icelandic Sign Language":"icl",
    "Indian Sign Language":"ins",
    "Indonesian":"id",
    "Inuktitut":"iu",
    "Inupiaq":"ik",
    "Irish Gaelic":"ga",
    "Japanese Sign Language":"jsl",
    "Jola-Fonyi":"dyo",
    "Ju&#x27;hoan":"ktz",
    "Kaado":"qbf",
    "Kabuverdianu":"kea",
    "Kabyle":"kab",
    "Kalmyk-Oirat":"xal",
    "Kannada":"kn",
    "Karaj&#xE1;":"kpj",
    "Karbi":"mjw",
    "Karen":"kar",
    "Kazakh":"kk",
    "Khanty":"kca",
    "Khasi":"kha",
    "Kikuyu":"ki",
    "Kinyarwanda":"rw",
    "Kirundi":"qar",
    "Klingon":"tlh",
    "Kodava":"kfa",
    "Konkani":"kok",
    "Korean Sign Language":"kvk",
    "Korowai":"khe",
    "Kriolu":"qaq",
    "Kru":"kro",
    "Kudmali":"kyw",
    "Kuna":"qbb",
    "Kurdish":"ku",
    "Kwakiutl":"kwk",
    "Kyrgyz":"ky",
    "Ladakhi":"lbj",
    "Ladino":"lad",
    "Lao":"lo",
    "Latin":"la",
    "Latvian":"lv",
    "Limbu":"lif",
    "Lingala":"ln",
    "Lithuanian":"lt",
    "Low German":"nds",
    "Luxembourgish":"lb",
    "Macedonian":"mk",
    "Macro-J&#xEA;":"qbm",
    "Magahi":"mag",
    "Maithili":"mai",
    "Malagasy":"mg",
    "Malay":"ms",
    "Malayalam":"ml",
    "Malecite-Passamaquoddy":"pqm",
    "Malinka":"qap",
    "Maltese":"mt",
    "Manchu":"mnc",
    "Mandarin":"cmn",
    "Mandingo":"man",
    "Manipuri":"mni",
    "Maori":"mi",
    "Mapudungun":"arn",
    "Marathi":"mr",
    "Marshallese":"mh",
    "Masai":"mas",
    "Masalit":"mls",
    "Maya":"myn",
    "Mende":"men",
    "Micmac":"mic",
    "Middle English":"enm",
    "Min Nan":"nan",
    "Minangkabau":"min",
    "Mirandese":"mwl",
    "Mizo":"lus",
    "Mohawk":"moh",
    "Mongolian":"mn",
    "Montagnais":"moe",
    "More":"qaf",
    "Morisyen":"mfe",
    "Nagpuri":"qbl",
    "Nahuatl":"nah",
    "Nama":"qba",
    "Navajo":"nv",
    "Naxi":"nbf",
    "Ndebele":"nd",
    "Neapolitan":"nap",
    "Nenets":"yrk",
    "Nepali":"ne",
    "Nisga&#x27;a":"ncg",
    "None":"zxx",
    "Norse, Old":"non",
    "North American Indian":"nai",
    "Nushi":"qbk",
    "Nyaneka":"nyk",
    "Nyanja":"ny",
    "Occitan":"oc",
    "Ojibwa":"oj",
    "Ojihimba":"qaz",
    "Old English":"ang",
    "Oriya":"or",
    "Papiamento":"pap",
    "Parsee":"qaj",
    "Pashtu":"ps",
    "Pawnee":"paw",
    "Peul":"qai",
    "Polynesian":"qah",
    "Pular":"fuf",
    "Purepecha":"tsz",
    "Quechua":"qu",
    "Quenya":"qya",
    "Rajasthani":"raj",
    "Rawan":"qbj",
    "Romansh":"rm",
    "Romany":"rom",
    "Rotuman":"rtm",
    "Russian Sign Language":"rsl",
    "Ryukyuan":"qao",
    "Saami":"qae",
    "Samoan":"sm",
    "Sanskrit":"sa",
    "Sardinian":"sc",
    "Scanian":"qay",
    "Serbian":"sr",
    "Serbo-Croatian":"qbo",
    "Serer":"srr",
    "Shanghainese":"qad",
    "Shanxi":"qau",
    "Shona":"sn",
    "Shoshoni":"shh",
    "Sicilian":"scn",
    "Sindarin":"sjn",
    "Sindhi":"sd",
    "Sinhala":"si",
    "Sioux":"sio",
    "Slovak":"sk",
    "Slovenian":"sl",
    "Somali":"so",
    "Songhay":"son",
    "Soninke":"snk",
    "Sorbian languages":"wen",
    "Sotho":"st",
    "Sousson":"qbe",
    "Spanish Sign Language":"ssp",
    "Sranan":"srn",
    "Swahili":"sw",
    "Swiss German":"gsw",
    "Sylheti":"syl",
    "Tagalog":"tl",
    "Tajik":"tg",
    "Tamashek":"tmh",
    "Tamil":"ta",
    "Tarahumara":"tac",
    "Tatar":"tt",
    "Telugu":"te",
    "Teochew":"qak",
    "Thai":"th",
    "Tibetan":"bo",
    "Tigrigna":"qan",
    "Tlingit":"tli",
    "Tok Pisin":"tpi",
    "Tonga (Tonga Islands)":"to",
    "Tsonga":"ts",
    "Tswa":"tsc",
    "Tswana":"tn",
    "Tulu":"tcy",
    "Tupi":"tup",
    "Turkmen":"tk",
    "Tuvinian":"tyv",
    "Tzotzil":"tzo",
    "Ungwatsi":"qat",
    "Urdu":"ur",
    "Uzbek":"uz",
    "Vietnamese":"vi",
    "Visayan":"qaa",
    "Washoe":"was",
    "Welsh":"cy",
    "Wolof":"wo",
    "Xhosa":"xh",
    "Yakut":"sah",
    "Yapese":"yap",
    "Yiddish":"yi",
    "Yoruba":"yo",
    "Zulu":"zu"}
    return languages_dict[languages_select]

def get_countries(countries_select):
    countries_dict = {"Any":"*",
    "Argentina":"ar",
    "Australia":"au",
    "Austria":"at",
    "Belgium":"be",
    "Brazil":"br",
    "Bulgaria":"bg",
    "Canada":"ca",
    "China":"cn",
    "Colombia":"co",
    "Costa Rica":"cr",
    "Czech Republic":"cz",
    "Denmark":"dk",
    "Finland":"fi",
    "France":"fr",
    "Germany":"de",
    "Greece":"gr",
    "Hong Kong":"hk",
    "Hungary":"hu",
    "Iceland":"is",
    "India":"in",
    "Iran":"ir",
    "Ireland":"ie",
    "Italy":"it",
    "Japan":"jp",
    "Malaysia":"my",
    "Mexico":"mx",
    "Netherlands":"nl",
    "New Zealand":"nz",
    "Pakistan":"pk",
    "Poland":"pl",
    "Portugal":"pt",
    "Romania":"ro",
    "Russia":"ru",
    "Singapore":"sg",
    "South Africa":"za",
    "Spain":"es",
    "Sweden":"se",
    "Switzerland":"ch",
    "Thailand":"th",
    "United Kingdom":"gb",
    "United States":"us",
    "Afghanistan":"af",
    "&#xC5;land Islands":"ax",
    "Albania":"al",
    "Algeria":"dz",
    "American Samoa":"as",
    "Andorra":"ad",
    "Angola":"ao",
    "Anguilla":"ai",
    "Antarctica":"aq",
    "Antigua and Barbuda":"ag",
    "Armenia":"am",
    "Aruba":"aw",
    "Azerbaijan":"az",
    "Bahamas":"bs",
    "Bahrain":"bh",
    "Bangladesh":"bd",
    "Barbados":"bb",
    "Belarus":"by",
    "Belize":"bz",
    "Benin":"bj",
    "Bermuda":"bm",
    "Bhutan":"bt",
    "Bolivia":"bo",
    "Bonaire, Sint Eustatius and Saba":"bq",
    "Bosnia and Herzegovina":"ba",
    "Botswana":"bw",
    "Bouvet Island":"bv",
    "British Indian Ocean Territory":"io",
    "British Virgin Islands":"vg",
    "Brunei Darussalam":"bn",
    "Burkina Faso":"bf",
    "Burma":"bumm",
    "Burundi":"bi",
    "Cambodia":"kh",
    "Cameroon":"cm",
    "Cape Verde":"cv",
    "Cayman Islands":"ky",
    "Central African Republic":"cf",
    "Chad":"td",
    "Chile":"cl",
    "Christmas Island":"cx",
    "Cocos (Keeling) Islands":"cc",
    "Comoros":"km",
    "Congo":"cg",
    "Cook Islands":"ck",
    "C&#xF4;te d&#x27;Ivoire":"ci",
    "Croatia":"hr",
    "Cuba":"cu",
    "Cyprus":"cy",
    "Czechoslovakia":"cshh",
    "Democratic Republic of the Congo":"cd",
    "Djibouti":"dj",
    "Dominica":"dm",
    "Dominican Republic":"do",
    "East Germany":"ddde",
    "Ecuador":"ec",
    "Egypt":"eg",
    "El Salvador":"sv",
    "Equatorial Guinea":"gq",
    "Eritrea":"er",
    "Estonia":"ee",
    "Ethiopia":"et",
    "Falkland Islands":"fk",
    "Faroe Islands":"fo",
    "Federal Republic of Yugoslavia":"yucs",
    "Federated States of Micronesia":"fm",
    "Fiji":"fj",
    "French Guiana":"gf",
    "French Polynesia":"pf",
    "French Southern Territories":"tf",
    "Gabon":"ga",
    "Gambia":"gm",
    "Georgia":"ge",
    "Ghana":"gh",
    "Gibraltar":"gi",
    "Greenland":"gl",
    "Grenada":"gd",
    "Guadeloupe":"gp",
    "Guam":"gu",
    "Guatemala":"gt",
    "Guernsey":"gg",
    "Guinea":"gn",
    "Guinea-Bissau":"gw",
    "Guyana":"gy",
    "Haiti":"ht",
    "Heard Island and McDonald Islands":"hm",
    "Holy See (Vatican City State)":"va",
    "Honduras":"hn",
    "Indonesia":"id",
    "Iraq":"iq",
    "Isle of Man":"im",
    "Israel":"il",
    "Jamaica":"jm",
    "Jersey":"je",
    "Jordan":"jo",
    "Kazakhstan":"kz",
    "Kenya":"ke",
    "Kiribati":"ki",
    "Korea":"xko",
    "Kosovo":"xkv",
    "Kuwait":"kw",
    "Kyrgyzstan":"kg",
    "Laos":"la",
    "Latvia":"lv",
    "Lebanon":"lb",
    "Lesotho":"ls",
    "Liberia":"lr",
    "Libya":"ly",
    "Liechtenstein":"li",
    "Lithuania":"lt",
    "Luxembourg":"lu",
    "Macao":"mo",
    "Madagascar":"mg",
    "Malawi":"mw",
    "Maldives":"mv",
    "Mali":"ml",
    "Malta":"mt",
    "Marshall Islands":"mh",
    "Martinique":"mq",
    "Mauritania":"mr",
    "Mauritius":"mu",
    "Mayotte":"yt",
    "Moldova":"md",
    "Monaco":"mc",
    "Mongolia":"mn",
    "Montenegro":"me",
    "Montserrat":"ms",
    "Morocco":"ma",
    "Mozambique":"mz",
    "Myanmar":"mm",
    "Namibia":"na",
    "Nauru":"nr",
    "Nepal":"np",
    "Netherlands Antilles":"an",
    "New Caledonia":"nc",
    "Nicaragua":"ni",
    "Niger":"ne",
    "Nigeria":"ng",
    "Niue":"nu",
    "Norfolk Island":"nf",
    "North Korea":"kp",
    "North Vietnam":"vdvn",
    "Northern Mariana Islands":"mp",
    "Norway":"no",
    "Oman":"om",
    "Palau":"pw",
    "Palestine":"xpi",
    "Palestinian Territory":"ps",
    "Panama":"pa",
    "Papua New Guinea":"pg",
    "Paraguay":"py",
    "Peru":"pe",
    "Philippines":"ph",
    "Pitcairn":"pn",
    "Puerto Rico":"pr",
    "Qatar":"qa",
    "Republic of Macedonia":"mk",
    "R&#xE9;union":"re",
    "Rwanda":"rw",
    "Saint Barth&#xE9;lemy":"bl",
    "Saint Helena":"sh",
    "Saint Kitts and Nevis":"kn",
    "Saint Lucia":"lc",
    "Saint Martin (French part)":"mf",
    "Saint Pierre and Miquelon":"pm",
    "Saint Vincent and the Grenadines":"vc",
    "Samoa":"ws",
    "San Marino":"sm",
    "Sao Tome and Principe":"st",
    "Saudi Arabia":"sa",
    "Senegal":"sn",
    "Serbia":"rs",
    "Serbia and Montenegro":"csxx",
    "Seychelles":"sc",
    "Siam":"xsi",
    "Sierra Leone":"sl",
    "Slovakia":"sk",
    "Slovenia":"si",
    "Solomon Islands":"sb",
    "Somalia":"so",
    "South Georgia and the South Sandwich Islands":"gs",
    "South Korea":"kr",
    "Soviet Union":"suhh",
    "Sri Lanka":"lk",
    "Sudan":"sd",
    "Suriname":"sr",
    "Svalbard and Jan Mayen":"sj",
    "Swaziland":"sz",
    "Syria":"sy",
    "Taiwan":"tw",
    "Tajikistan":"tj",
    "Tanzania":"tz",
    "Timor-Leste":"tl",
    "Togo":"tg",
    "Tokelau":"tk",
    "Tonga":"to",
    "Trinidad and Tobago":"tt",
    "Tunisia":"tn",
    "Turkey":"tr",
    "Turkmenistan":"tm",
    "Turks and Caicos Islands":"tc",
    "Tuvalu":"tv",
    "U.S. Virgin Islands":"vi",
    "Uganda":"ug",
    "Ukraine":"ua",
    "United Arab Emirates":"ae",
    "United States Minor Outlying Islands":"um",
    "Uruguay":"uy",
    "Uzbekistan":"uz",
    "Vanuatu":"vu",
    "Venezuela":"ve",
    "Vietnam":"vn",
    "Wallis and Futuna":"wf",
    "West Germany":"xwg",
    "Western Sahara":"eh",
    "Yemen":"ye",
    "Yugoslavia":"xyu",
    "Zaire":"zrcd",
    "Zambia":"zm",
    "Zimbabwe":"zw"}
    return countries_dict[countries_select]

def get_searches():
    #TODO persistent searches
    return []
    
def get_categories():
    return ['Any', 'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 
    'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western']

def get_url(category,page):
    imdb_query = [
    ("count", __settings__.getSetting( "count" )),
    ("title", __settings__.getSetting( "title" )),
    ("title_type", get_title_type(__settings__.getSetting( "title_type" ))),
    ("release_date", "%s,%s" % (__settings__.getSetting( "release_date_start" ),__settings__.getSetting( "release_date_end" ))),
    ("user_rating", "%.1f,%.1f" % (float(__settings__.getSetting( "user_rating_low" )),float(__settings__.getSetting( "user_rating_high" )))),
    ("num_votes", "%s,%s" % (__settings__.getSetting( "num_votes_low" ),__settings__.getSetting( "num_votes_high" ))),
    ("genres", "%s,%s" % (get_genre(category),get_genre(__settings__.getSetting( "genres" )))),   
    ("groups", "%s" % (get_group(__settings__.getSetting( "groups" )))),  
    ("companies", get_company(__settings__.getSetting( "companies" ))),
    ("boxoffice_gross_us", "%s,%s" % (__settings__.getSetting( "boxoffice_gross_us_low" ),__settings__.getSetting( "boxoffice_gross_us_high" ))),
    ("sort", get_sort(__settings__.getSetting( "sort" ))),
    ("certificates", get_certificate(__settings__.getSetting( "certificates" ))),
    ("countries", get_countries(__settings__.getSetting( "countries" ))),
    ("languages", get_languages(__settings__.getSetting( "languages" ))),
    ("moviemeter", "%s,%s" % (__settings__.getSetting( "moviemeter_low" ),__settings__.getSetting( "moviemeter_high" ))),
    ("production_status", get_production_status(__settings__.getSetting( "production_status" ))),
    ("runtime", "%s,%s" % (__settings__.getSetting( "runtime_low" ),__settings__.getSetting( "runtime_high" ))),
    ("sort", get_sort(__settings__.getSetting( "sort" ))),
    ("colors", get_color(__settings__.getSetting( "colors" ))),
    ("role", __settings__.getSetting( "crew" )),
    ("plot", __settings__.getSetting( "plot" )),
    ("keywords", __settings__.getSetting( "keywords" )),
    ("locations", __settings__.getSetting( "locations" )),
    ("page", str(page)),
    ]
    #server = get_server(__settings__.getSetting( "server" ))
    #url = "http://%s.imdb.com/search/title?" % server
    params = {}
    for (field, value) in imdb_query:
        if not "Any" in value and value != "None" and value != "" and value != "," and value != "*" and value != "*," and value != ",*": #NOTE title has * sometimes
            params[field] = value
    params_url = urllib.urlencode(params)
    #url = "%s%s" % (url,params_url)
    return (params_url,params)

def get_videos(url):
    params = dict(urlparse.parse_qsl(url))

    xbmc.log(url)
    xbmc.log(repr(params))
    #{'count': ['50'], 'sort': ['popularity.desc'], 'genres': ['Any,27'], 'production_status': ['released'], 'release_date': ['2015,2016'], 'num_votes': ['100,'], 'languages': ['en'], 'user_rating': ['6.0,10.0'], 'title_type': ['movie']}
    sort = params['sort']
    genres = params['genres'].strip(' ,')
    release_date = params['release_date'].split(',')
    num_votes = params['num_votes'].split(',')
    user_rating = params['user_rating'].split(',')
    
    page = params['page']
    LANG = 'en'
    result = tmdbsimple.Discover().movie(language=LANG, **{
    'page': page, 
    'sort_by': sort,
    'primary_release_date.gte': "%s" % release_date[0],
    'primary_release_date.lte': "%s" % release_date[1],
    'vote_count.gte': "%s" % num_votes[0],
    'vote_count.lte': "%s" % num_votes[1],
    'vote_average.gte': "%s" % user_rating[0],
    'vote_average.lte': "%s" % user_rating[1],
    'with_genres': genres,
    })
    xbmc.log(repr(result))
    #(total_results,total_pages,page,results) = result
    
    
    this_page = result['page']
    total_pages = result['total_pages']
    next_url = ''
    if this_page < total_pages:
        next_page = int(this_page) + 1
        params['page'] = next_page
        #params['page'][0] = int(this_page) + 1&
        next_url = urllib.urlencode(params)
    
    items = result['results']
    videos = []
    for item in items:
        xbmc.log(repr(item))
        
        #u'poster_path': u'/vZpB8ezB1IqpxI9rx553TuGwDzJ.jpg',
		#u'title': u'StarWars: TheForceAwakens',
		#u'overview': u'ThirtyyearsafterdefeatingtheGalacticEmpire, crosses paths with the mermaid, Shan, who is sent to avenge her people.",
		#HanSoloandhisalliesfaceanewthreatfromtheevilKyloRenandhisarmyofStormtroopers.',
		#u'release_date': u'2015-12-15',
		#u'popularity': 40.29992,
		#u'original_title': u'StarWars: TheForceAwakens',
		#u'backdrop_path': u'/njv65RTipNSTozFLuF85jL0bcQe.jpg',
		#u'vote_count': 3609,
		#u'video': False,
		#u'adult': False,
		#u'vote_average': 7.68,
		#u'original_language': u'en',
		#u'id': 140607,
		#u'genre_ids': [28,
		#12,
		#878,
        #14]
        title = item['title']
        episode = ''
        img_url = 'http://image.tmdb.org/t/p/w500%s' % item['poster_path']
        fanart_url = 'http://image.tmdb.org/t/p/w1000%s' % item['backdrop_path']
        genres = ''
        meta_url = 'plugin://plugin.video.meta/movies/play/tmdb/%s/select' % item['id']
        episode_id = ''
        imdbID = ''
        id = item['id']
        year = item['release_date'][0:4]
        rating = item['vote_average']
        plot = item['overview']
        sort = ''
        cast = []
        runtime = ''
        votes = item['vote_count']
        certificate = ''
    
        videos.append({'name':title,'episode':episode,'thumb':img_url,'fanart':fanart_url,'genre':genres,
        'video':meta_url,'episode_id':episode_id,'imdb_id':imdbID,
        'code': id,'year':year,'mediatype':'movie','rating':rating,'plot':plot,
        'sort':sort,'cast':cast,'runtime':runtime,'votes':votes, 'certificate':certificate})
            
    #next_url = ''
    #pagination_match = re.search(r'<span class="pagination">.*<a href="(.+?)">Next', html, flags=(re.DOTALL | re.MULTILINE))
    #if pagination_match:
    #    server = get_server(__settings__.getSetting( "server" ))
    #    next_url = "http://%s.imdb.com%s" % (server,pagination_match.group(1))
        
    return (videos,next_url)
    
def get_videosimdb(url):
    r = requests.get(url)
    html = r.text
    html = HTMLParser.HTMLParser().unescape(html)
    
    items = html.split('<tr class="')
    videos = []
    for item in items:
        
        if not re.search(r'^.*?detailed"',item):
            continue
        
        img_url = ''
        img_match = re.search(r'<img src="(.*?)"', item)
        if img_match:
            img = img_match.group(1)
            img_url = re.sub(r'S[XY].*_.jpg','SX344_.jpg',img) #NOTE 344 is Confluence List View width

        title = ''
        imdbID = ''
        year = ''
        title_match = re.search(r'<td class="title">.*?<a href="/title/(.+?)/">(.*?)</a>', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            imdbID = title_match.group(1)
            title = title_match.group(2)

        title_match = re.search(r'<a href="/title/(.+?)/" title="(.+?) \((.+?)\)"', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(3)

        episode = ''
        episode_id = ''
        episode_match = re.search(r'<span class="episode">Episode: <a href="/title/(.+?)/">(.+?)</a>(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if episode_match:
            episode_id = episode_match.group(1)
            episode = "%s%s" % (episode_match.group(2), episode_match.group(3))
            year = episode_match.group(3).strip('() ')
            
        rating = ''
        votes = ''
        rating_match = re.search(r'title="Users rated this (.+?)/10 \((.+?) votes\)', item, flags=(re.DOTALL | re.MULTILINE))
        if rating_match:
            rating = rating_match.group(1)
            votes = rating_match.group(2)
            votes = re.sub(',','',votes)
            
        plot = ''
        plot_match = re.search(r'<span class="outline">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if plot_match:
            plot = plot_match.group(1)
            
        cast = []
        cast_match = re.search(r'<span class="credit">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if cast_match:
            cast = cast_match.group(1)
            cast_list = re.findall(r'<a.+?>(.+?)</a>', cast)
            cast = cast_list
                
        genres = ''
        genre_match = re.search(r'<span class="genre">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if genre_match:
            genre = genre_match.group(1)
            genre_list = re.findall(r'<a.+?>(.+?)</a>', genre)
            genres = ",".join(genre_list)
                
        runtime = ''
        runtime_match = re.search(r'<span class="runtime">(.+?) mins\.</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if runtime_match:
            runtime = int(runtime_match.group(1)) * 60
                
        sort = ''
        sort_match = re.search(r'<span class="sort"><span title="(.+?)"', item, flags=(re.DOTALL | re.MULTILINE))
        if sort_match:
            sort = sort_match.group(1)

        certificate = ''
        certificate_match = re.search(r'<span class="certificate">.*?title="(.+?)"', item, flags=(re.DOTALL | re.MULTILINE))
        if certificate_match:
            certificate = certificate_match.group(1)
            
        if imdbID:
            id = imdbID
            title_type = get_title_type(__settings__.getSetting( "title_type" ))
            if title_type == "tv_series" or title_type == "mini_series": 
                meta_url = "plugin://plugin.video.meta/tv/search_term/%s/1" % re.sub(' ','+',title)
            elif title_type == "tv_episode":
                vlabel = "%s - %s" % (title, episode)
                vlabel = urllib.quote_plus(vlabel.encode("utf8"))
                meta_url = "plugin://plugin.video.imdbsearch/?action=episode&imdb_id=%s&episode_id=%s&title=%s" % (imdbID,episode_id,vlabel)
                id = episode_id
            else:
                meta_url = 'plugin://plugin.video.meta/movies/play/imdb/%s/select' % imdbID

            videos.append({'name':title,'episode':episode,'thumb':img_url,'genre':genres,
            'video':meta_url,'episode_id':episode_id,'imdb_id':imdbID,
            'code': id,'year':year,'mediatype':'movie','rating':rating,'plot':plot,
            'sort':sort,'cast':cast,'runtime':runtime,'votes':votes, 'certificate':certificate})
            
    next_url = ''
    pagination_match = re.search(r'<span class="pagination">.*<a href="(.+?)">Next', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        server = get_server(__settings__.getSetting( "server" ))
        next_url = "http://%s.imdb.com%s" % (server,pagination_match.group(1))
        
    return (videos,next_url)
    
def get_tvdb_id(imdb_id):
    tvdb_url = "http://thetvdb.com//api/GetSeriesByRemoteID.php?imdbid=%s" % imdb_id
    r = requests.get(tvdb_url)
    tvdb_html = r.text
    tvdb_id = ''
    tvdb_match = re.search(r'<seriesid>(.*?)</seriesid>', tvdb_html, flags=(re.DOTALL | re.MULTILINE))
    if tvdb_match:
        tvdb_id = tvdb_match.group(1)
    return tvdb_id

def find_episode(imdb_id,episode_id,title):
    tvdb_id = get_tvdb_id(imdb_id)

    server = get_server(__settings__.getSetting( "server" ))
    episode_url = "http://%s.imdb.com/title/%s" % (server,episode_id)
    r = requests.get(episode_url)
    episode_html = r.text
    episode_html = HTMLParser.HTMLParser().unescape(episode_html)
    season = ''
    episode = ''
    season_match = re.search(r'<div class="bp_heading">Season ([0-9]*?) <span class="ghost">\|</span> Episode ([0-9]*?)</div>', 
    episode_html, flags=(re.DOTALL | re.MULTILINE))
    if season_match:
        season = season_match.group(1)
        episode = season_match.group(2)
        
    meta_url = "plugin://plugin.video.meta/tv/play/%s/%s/%s/%s" % (tvdb_id,season,episode,'select')
    list_item = xbmcgui.ListItem(label=title)
    list_item.setPath(meta_url)
    list_item.setProperty("IsPlayable", "true")
    list_item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.setResolvedUrl(_handle, True, listitem=list_item)
    
    
def list_searches():
    searches = get_searches()
    (url,params) = get_url('None',1)
    imdb_url=urllib.quote_plus(url)
    prefix = __settings__.getSetting( "prefix" )
    if not prefix:
        name = 'Search'
    else:
        name = '%s Search' % prefix
    searches.append((name,imdb_url,params))
    listing = []
    for (name,imdb_url,params) in searches:
        list_item = xbmcgui.ListItem(label=name)
        genre_icon = get_genre_icon('Any')
        list_item.setArt({'thumb': genre_icon, 'icon': genre_icon, 'fanart': get_background()})
        plot = ""
        #params['server'] = server
        for param in sorted(params):
            plot = plot + "%s[COLOR=darkgray]=[/COLOR][B]%s[/B] " % (param, params[param])
        list_item.setInfo('video', {'title': name, 'genre': '', 'plot': plot})
        url = '{0}?action=categories&name={1}&imdb={2}'.format(_url, urllib.quote_plus(prefix), imdb_url)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(_handle)

    
def list_categories(prefix,category_url):
    categories = get_categories()
    listing = []
    for category in categories:
        cat = re.sub('_',' ',category)
        if prefix:
            name = "%s %s" % (prefix, re.sub('_',' ',cat))
        else:
            name = cat
        list_item = xbmcgui.ListItem(label=name)
        genre_icon = get_genre_icon(category)
        list_item.setArt({'thumb': genre_icon, 'icon': genre_icon, 'fanart': get_background()})
        if re.search(r'genres=,.*?&',category_url):
            imdb_url = re.sub(r'genres=,(.*?)&',r'genres=%s,\1&' % get_genre(category),category_url)
        else:
            imdb_url = "%s&genres=%s," % (category_url,get_genre(category))
        imdb_url=urllib.quote_plus(imdb_url)
        plot = ""
        list_item.setInfo('video', {'title': name, 'genre': category, 'plot': plot})
        url = '{0}?action=listing&category={1}&imdb={2}'.format(_url, category,imdb_url)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(_handle)


def list_videos(imdb_url):
    (videos,next_url) = get_videos(imdb_url)
    title_type = get_title_type(__settings__.getSetting( "title_type" ))
    type = ''
    content = ''
    info_type = ''
    trakt_type = ''
    if title_type == "tv_series" or title_type == "mini_series": 
        trakt_type = 'shows'
        info_type = 'extendedtvinfo'
        content = 'tvshows'
        type = 'tv'
        IsPlayable = 'false'
        is_folder = True
    elif title_type == "game":
        content = 'files'
        IsPlayable = 'false'
        is_folder = False
    elif title_type == 'tv_episode':
        trakt_type = 'episodes'
        info_type = ''
        content = 'episodes'
        type = 'episode'
        IsPlayable = 'true'
        is_folder = False
    else:
        trakt_type = 'movies'
        info_type = 'extendedinfo'
        content = 'movies'
        type = 'movies'
        IsPlayable = 'true'
        is_folder = False
    listing = []
    for video in videos:
        if title_type == "tv_episode":
            vlabel = "%s - %s" % (video['name'], video['episode'])
        else:
            vlabel = video['name']
        list_item = xbmcgui.ListItem(label=vlabel)
        list_item.setInfo('video', {'title': vlabel, 'genre': video['genre'],'code': video['code'], 
        'year':video['year'],'mediatype':'movie','rating':video['rating'],'plot': video['plot'],
        'mpaa': video['certificate'],'cast': video['cast'],'duration': video['runtime'], 'votes': video['votes']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['fanart']})
        list_item.setProperty('IsPlayable', IsPlayable)
        is_folder = is_folder
        context_items = []
        context_items.append(('Information', 'XBMC.Action(Info)'))
        if info_type:
            context_items.append(('Extended Info', "XBMC.RunScript(script.extendedinfo,info=%s,imdb_id=%s)" % (info_type,video['code'])))
        if type == 'movies' or type == 'tv' or type == 'episode':
            if __settings__.getSetting('trakt') == 'true':
                context_items.append(('Add to Trakt Watchlist', 
                "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=addtotraktwatchlist&type=%s&imdb_id=%s&title=%s)" % 
                (trakt_type, video['code'], urllib.quote_plus(vlabel.encode("utf8")))))
        if type == 'movies' or type == 'tv':
            run_str = "plugin://plugin.video.imdbsearch/?action=library&type=%s&imdb_id=%s" % (type,video['code'])
            context_items.append(('Add To Meta Library', "XBMC.RunPlugin(%s)" % run_str ))
        context_items.append(('Meta Settings', "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=meta_settings)"))
        try:
            if type == 'movies' and xbmcaddon.Addon('plugin.video.couchpotato_manager'):
                context_items.append(
                ('Add to Couch Potato', "XBMC.RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add-by-id/%s)" % (video['code'])))
        except:
            pass
        try:
            if type == 'tv' and xbmcaddon.Addon('plugin.video.sickrage'):
                context_items.append(
                ('Add to Sickrage', "XBMC.RunPlugin(plugin://plugin.video.sickrage?action=addshow&&show_name=%s)" % (video['name'])))
        except:
            pass
        if __settings__.getSetting('default_context_menu') == 'true':
            list_item.addContextMenuItems(context_items,replaceItems=False)
        else:
            list_item.addContextMenuItems(context_items,replaceItems=True)
        video_streaminfo = {'codec': 'h264'}
        video_streaminfo['aspect'] = round(1280.0 / 720.0, 2)
        video_streaminfo['width'] = 1280
        video_streaminfo['height'] = 720
        list_item.addStreamInfo('video', video_streaminfo)
        list_item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
        if title_type == "game": 
            here_url = "%s%s" % (sys.argv[0],sys.argv[2])
            listing.append((here_url, list_item, is_folder))
        else:
            listing.append((video['video'], list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    listing = []
    if next_url:
        url = '{0}?action=listing&imdb={1}'.format(_url, urllib.quote_plus(next_url))
        list_item = xbmcgui.ListItem(label='[B]Next Page >>[/B]')
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb': 'DefaultNetwork.png', 'icon': 'DefaultNetwork.png', 'fanart': get_background()})
        is_folder = True
        listing.append((url, list_item, is_folder))
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

        
    xbmcplugin.setContent(int(sys.argv[1]), content)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_MPAA_RATING)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    xbmcplugin.endOfDirectory(_handle)

    if title_type == "tv_episode":
        xbmc.executebuiltin("Container.SetViewMode(%s)" % __settings__.getSetting( "tv_view" ))
    else:
        xbmc.executebuiltin("Container.SetViewMode(%s)" % __settings__.getSetting( "video_view" ))

def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def on_token_refreshed(response):
        __settings__.setSetting( "authorization", dumps(response))

def authenticate():
        dialog = xbmcgui.Dialog()
        pin = dialog.input('Open a web browser at %s' % Trakt['oauth'].pin_url(), type=xbmcgui.INPUT_ALPHANUM)
        if not pin:
            return False
        authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')
        if not authorization:
            return False
        __settings__.setSetting( "authorization", dumps(authorization))
        return True

def add_to_trakt_watchlist(type,imdb_id,title):
    Trakt.configuration.defaults.app(
        id=8835
    )
    Trakt.configuration.defaults.client(
        id="aa1c239000c56319a64014d0b169c0dbf03f7770204261c9edbe8ae5d4e50332",
        secret="250284a95fd22e389b565661c98d0f33ac222e9d03c43b5931e03946dbf858dc"
    )
    Trakt.on('oauth.token_refreshed', on_token_refreshed)
    if not __settings__.getSetting('authorization'):
        if not authenticate():
            return
    authorization = loads(__settings__.getSetting('authorization'))
    with Trakt.configuration.oauth.from_response(authorization, refresh=True):
        result = Trakt['sync/watchlist'].add({
            type: [
                {
                    'ids': {
                        'imdb': imdb_id
                    }
                }
            ]
        })
        dialog = xbmcgui.Dialog()
        dialog.notification("Trakt: add to watchlist",title)
    
def find_crew(name=''):
    dialog = xbmcgui.Dialog()
    if not name:
        name = dialog.input('Search for crew (actor, director etc)', type=xbmcgui.INPUT_ALPHANUM)
    dialog.notification('IMDB:','Finding crew details...')
    if not name:
        dialog.notification('IMDB:','No name!')
        return
    url = "http://www.imdb.com/xml/find?json=1&nr=1&q=%s&nm=on" % urllib.quote_plus(name)
    r = requests.get(url)
    json = r.json()
    crew = []
    if 'name_exact' in json:
        pop = json['name_exact']
        for p in pop:
            crew.append((p['name'],p['id']))
    if 'name_popular' in json:
        pop = json['name_popular']
        for p in pop:
            crew.append((p['name'],p['id']))
    if 'name_approx' in json:
        approx = json['name_approx']
        for p in approx:
            crew.append((p['name'],p['id']))
    if 'name_substring' in json:
        pop = json['name_substring']
        for p in pop:
            crew.append((p['name'],p['id']))
    names = [item[0] for item in crew]
    if names:
        index = dialog.select('Pick crew member',names)
        id = crew[index][1]
        __settings__.setSetting('crew',id)
    else:
        dialog.notification('IMDB:','Nothing Found!')

def find_keywords(keyword=''):
    dialog = xbmcgui.Dialog()
    if not keyword:
        keyword = dialog.input('Search for keyword', type=xbmcgui.INPUT_ALPHANUM)
    dialog.notification('IMDB:','Finding keyword matches...')
    if not keyword:
        dialog.notification('IMDB:','No keyword!')
        return
    url = "http://www.imdb.com/xml/find?json=1&nr=1&q=%s&kw=on" % urllib.quote_plus(keyword)
    r = requests.get(url)
    json = r.json()
    keywords = []
    if 'keyword_exact' in json:
        pop = json['keyword_exact']
        for p in pop:
            keywords.append((p['description'],p['keyword']))    
    if 'keyword_popular' in json:
        pop = json['keyword_popular']
        for p in pop:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_approx' in json:
        approx = json['keyword_approx']
        for p in approx:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_substring' in json:
        approx = json['keyword_substring']
        for p in approx:
            keywords.append((p['description'],p['keyword']))
    names = [item[0] for item in keywords]
    if keywords:
        index = dialog.select('Pick keywords member',names)
        id = keywords[index][1]
        __settings__.setSetting('keywords',id)
    else:
        dialog.notification('IMDB:','Nothing Found!')
        

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'find_keywords':
            find_keywords()
        if params['action'] == 'find_crew':
            find_crew()
        if params['action'] == 'meta_settings':
            xbmcaddon.Addon(id='plugin.video.meta').openSettings()        
        elif params['action'] == 'library':
            if 'type' in params.keys():
                type = params['type']
            if 'imdb_id' in params.keys():
                imdb_id = params['imdb_id']
            if type == 'tv':
                id = get_tvdb_id(imdb_id)
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.meta/%s/add_to_library/%s)" % (type,id))
            else:
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.meta/%s/add_to_library/tmdb/%s)" % (type,imdb_id))
        elif params['action'] == 'categories':
            name = ''
            if 'name' in params.keys():
                name = params['name']
            if 'imdb' in params.keys():
                imdb = params['imdb']
                list_categories(urllib.unquote_plus(name),urllib.unquote_plus(imdb))
        elif params['action'] == 'listing':
            if 'imdb' in params.keys():
                imdb = params['imdb']
                list_videos(urllib.unquote_plus(imdb))
        elif params['action'] == 'addtotraktwatchlist':
            if 'type' in params.keys():
                type = params['type']
            if 'title' in params.keys():
                title = params['title']
                title = urllib.unquote_plus(title)
            if 'imdb_id' in params.keys():
                imdb_id = params['imdb_id']
                add_to_trakt_watchlist(type,imdb_id,title)
        elif params['action'] == 'episode':
            if 'imdb_id' in params.keys():
                imdb_id = params['imdb_id']
            if 'episode_id' in params.keys():
                episode_id = params['episode_id']
            if 'title' in params.keys():
                title = params['title']
                title = urllib.unquote_plus(title)
            find_episode(imdb_id,episode_id,title)
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        if __settings__.getSetting('open_settings') == 'true':
            __settings__.openSettings()
        list_searches()

    

if __name__ == '__main__':
    if __settings__.getSetting('trakt') == 'false':
        __settings__.setSetting( "authorization", '')
    router(sys.argv[2][1:])