from django.shortcuts import render
import threading
import time
from .models import News1,Price, Arbscrypto
import ast
import datetime
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator

def manualreset(request):
  
  ThreadingExample()
  return render(request,'home.html',{'deletion':'reset completed'})

def home(request):
  news = News1.objects.order_by('-id')
  news = news[0:50]
  pricebasedatos = Price.objects.order_by('-id')
  pricebasedatos = pricebasedatos.values()
  pricebasedatos = pricebasedatos[0:1]

  pricebasedatos = pricebasedatos[0]['body']
  pricebasedatos = ast.literal_eval(pricebasedatos)
  pricebasedatos = pricebasedatos['RAW']

  context = {
    'news':news,
    'price':pricebasedatos
  }
  
  return render(request,'home.html', context)
 
    
def newsrepository(request):
  if request.method =='GET':
    news = News1.objects.filter(created_at__year=2019).order_by('-id')
    news = news[0:400]
    news= news
    paginator = Paginator(news, 21)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    # context = {
    #     'news':paged_listings
    #   }
    #   return render(request,'newsrepository.html', context)

    if len(news) == 0:
      notresultsfound = "Unfortunately, the date selected did not product any results. We only have news starting from May 2019."
      return render(request,'newsrepository.html', {'notresultsfound':notresultsfound})
    else:
      context = {
        'news':paged_listings,
      }
      return render(request,'newsrepository.html', context)

# def showdate(request):
#   # products = Product.objects.all()
#   if request.method=='POST':
    
#     fecha = request.POST['date']
 
#     #sampledate = datetime.date(2019, 4, 20)
#     #news = News1.objects.filter(created_at__year=fecha)
#     news = News1.objects.filter(created_at__date=fecha).order_by('-id')
#     news = news[0:400]

#     if len(news) == 0:
#       notresultsfound = "Unfortunately, the date selected did not product any results. We only have news starting from May 2019."
#       return render(request,'newsrepository.html', {'notresultsfound':notresultsfound})
#     else:
#       paginator = Paginator(news, 21)
#       page = request.POST.get('page')
#       paged_listings = paginator.get_page(page)

#       context = {
#         'news':paged_listings
#       }
#       return render(request,'newsrepository.html', context)
#   else:
#     selectadate = "Please use the filter provided abode to look up your news by day and keyword"
#     # news = News1.objects.filter(created_at__year=2019)
#     # news = news[0:1]
#     # paginator = Paginator(news, 21)
#     # page = request.GET.get('page')
#     # paged_listings = paginator.get_page(page)

#     context = {
#       'selectadate':selectadate
#     }
#     return render(request,'newsrepository.html', context)

def showdate(request):
  # products = Product.objects.all()
  queryset_list = News1.objects.order_by('-created_at')
  try:
    if request.GET['date'] == '' :
      context = {
        'nodataentered': 'Enter a valid data into the Data field'
      }
      return render(request,'newsrepository.html', context)
  except:
    pass

  if request.method =='GET':
      try:
        global date
        date = request.GET['date']
      except:
        pass
      try:
        queryset_list = queryset_list.filter(created_at__date= date)
      except Exception:
         context = {
        'error': 'No News for selected data. Oldest news are from May 2019'
         }
         return render(request,'newsrepository.html',context )
         
      news = queryset_list[0:400]
      paginator = Paginator(news, 21)
      page = request.GET.get('page')
      paged_listings = paginator.get_page(page)

      context = {
        'news':paged_listings 
      }
      return render(request,'newsrepository.html', context)
  else:
     selectadate = "Please use the filter provided abode to look up your news by day and keyword"
     context = {
        'selectadate':selectadate,
        
      }
     return render(request,'newsrepository.html', context)
    

def cryptoarbs(request):
  if request.method =='GET':
    arbitrage = Arbscrypto.objects.order_by('-created_at')
    arbitrage = arbitrage[0:30]
    
    #statistics
    hoyes = datetime.datetime.today().strftime('%Y-%m-%d')
    statistics = Arbscrypto.objects.filter(created_at__date= hoyes)
    # maximo = statistics['percentage'][0]
    maximo = Arbscrypto.objects.filter(created_at__date= hoyes).order_by('-percentage').values()
    maximo = maximo[0]
    statistics = {'counta':statistics.count(), 'maximo':maximo}
    
    context = {
            'arbs':arbitrage, 
            'statistics':statistics     
                } 
    return render(request,'arbs.html', context)

#filter for Cryptoarbs
def arborderbycoindown(request):
  if request.method =='GET':
    arbitragebycoin = Arbscrypto.objects.order_by('-pair')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)
  
def arborderbycoinup(request):
  if request.method =='GET':
    arbitragebycoin = Arbscrypto.objects.order_by('pair')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)

def percentageup(request):
  if request.method =='GET':
    arbitragebycoin = Arbscrypto.objects.order_by('-percentage')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)

def arbsgreaterthan0(request):
  if request.method =='GET':
  
    arbitragebycoin = Arbscrypto.objects.filter(percentage__gte=0).order_by('-created_at')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)

def arbsgreaterthan1(request):
  if request.method =='GET':
  
    arbitragebycoin = Arbscrypto.objects.filter(percentage__gte=1).order_by('-created_at')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)

def arbsgreaterthan2(request):
  if request.method =='GET':
  
    arbitragebycoin = Arbscrypto.objects.filter(percentage__gte=2).order_by('-created_at')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)

def arbsgreaterthan5(request):
  if request.method =='GET':
  
    arbitragebycoin = Arbscrypto.objects.filter(percentage__gte=5).order_by('-created_at')
    arbitragebycoin = arbitragebycoin[0:30]
    
    
    context = {
            'arbs':arbitragebycoin,      
                } 
    return render(request,'arbs.html', context)

def searchanddate(request):
   try:
    if request.GET['keywords'] == '' or request.GET['date'] == '':
      context = {
        'nodataentered': 'Enter Both a valid date and Keyword into the field'
      }
      return render(request,'newsrepository.html', context)
   except:
      pass

   queryset_list = News1.objects.order_by('-created_at')
   if 'keywords' in request.GET and 'date' in request.GET:
      keywords = request.GET['keywords']
      fechacombinada = request.GET['date']
      queryset_list = queryset_list.filter(title__icontains=keywords)
      queryset_list = queryset_list.filter(created_at__date=fechacombinada)
      news = queryset_list[0:400]
      
      context ={
        'news':queryset_list,
        'createdorder':'Words ordered by publication date'
      }
      return render(request,'newsrepository.html',context)

def searchcrypto(request):
  try:
    if request.GET['keywords'] == '' :
      context = {
        'nodataentered': 'Enter a valid data into the Keyword field'
      }
      return render(request,'newsrepository.html', context)
  except:
      pass

  queryset_list = News1.objects.order_by('-created_at')
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(title__icontains=keywords)
      news = queryset_list[0:400]
      context ={
        'news':queryset_list,
        'createdorder':'Words ordered by publication date'
      }
      return render(request,'newsrepository.html',context)

def deletearbsfromdatabase(request):
  
  if request.method =='GET':
    Arbscrypto.objects.filter(created_at__lte=(datetime.datetime.now() - datetime.timedelta(days=1))).delete()
   

    return render(request,'home.html',{'deletion':'deletion completed'})
    
      
# def home(request):
#   import requests
#   import json

#   #grab crypto prices data
#   price_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,ENJ,NEO,EOS,XLM,LTC,DASH&tsyms=USD')
#   price = json.loads(price_request.content)


#   #grab crypto news
  
#   api_request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
#   api = json.loads(api_request.content)

#   return render(request, 'home.html', {'api':api, 'price':price})

def posttweet(request):
  import tweepy

  consumer_key = 'sOCtIn12MdBUekw7K8JW7Tm9p'
  consumer_secret = 'aasdfd'
  access_token = '1107203070998573056-WtHzQdR5Y1ZCS9hxZxGXFLYyr1dYLF'
  access_token_secret = 'asdda'

  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  api = tweepy.API(auth)

  arbitrage = Arbscrypto.objects.order_by('-created_at')
  arbitrage = arbitrage[0:30]
    
    #statistics
  hoyes = datetime.datetime.today().strftime('%Y-%m-%d')
  statistics = Arbscrypto.objects.filter(created_at__date= hoyes)
    # maximo = statistics['percentage'][0]
  maximo = Arbscrypto.objects.filter(created_at__date= hoyes).order_by('-percentage').values()
  maximo = maximo[0]
  
  public_tweets = api.home_timeline()
  # for tweet in public_tweets:
  #     print (tweet.text)
  
  procentaje = str(round(maximo['percentage'],2))
  tweettopublish = maximo['pair'] + ' buy in ' + maximo['exchangebuy'] +' sell in '+ maximo['exchangesell'] + ' and take a ' + procentaje + '% profit. Discover more crypto arbs in cryptonewsandprices.me'
  print(tweettopublish)  
  api.update_status(tweettopublish)
  return render(request,'home.html',{'deletion':'deletion completed or tweet posted'})


def prices(request):
  pricebasedatos = Price.objects.order_by('-id')
  pricebasedatos = pricebasedatos.values()
  pricebasedatos = pricebasedatos[0:1]

  pricebasedatos = pricebasedatos[0]['body']
  pricebasedatos = ast.literal_eval(pricebasedatos)
  pricebasedatos = pricebasedatos['RAW']


  
  if request.method == 'POST':
    import requests
    import json
    quote = request.POST['quote']
    quote = quote.upper()
    crypto_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=' + quote +'&tsyms=USD')
    
    crypto = json.loads(crypto_request.content)
    context = {
      'price':pricebasedatos,
      'quote':quote,
      'crypto':crypto
    }

    return render(request, 'prices.html',context)
    
    # return render(request, 'prices.html',{'quote':quote, 'crypto':crypto})

  else:
    notfound = "Enter a crypto symbol into the search form in the top navbar."
    return render(request,'prices.html',{'notfound':notfound,'price':pricebasedatos })

     

#check if it works interval charging page

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """
    time.sleep(1)
    def __init__(self, interval=10):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        
        while True:
            # Do something
            print('Doing something imporant in the background')
            import requests
            import json
      #grab crypto prices data
            price_request = requests.get('https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,ENJ,NEO,EOS,XLM,LTC,ONT,NEM,ADA,BNB,KCS,TRX,DASH&tsyms=USD')
            price = json.loads(price_request.content)
         
            pricedb = Price()
            pricedb.body = price
            pricedb.save()
            


      #grab crypto news
      
            api_request = requests.get('https://min-api.cryptocompare.com/data/v2/news/?lang=EN')
            api = json.loads(api_request.content)
            api = api['Data']

            for x in api:
            
              # news = News1.objects.order_by('title')
              # title = x['title']
              # if news.objects.filter(title='title').exists():
              #   pass
              # else:
              news = News1()
              news.title = x['title']
              news.body = x['body']
              news.image = x['imageurl']
              # dateconvert= x['published_on']
              
              # dateconvert = datetime.datetime.fromtimestamp(dateconvert / 1e3)
              # news.pub_date = dateconvert
              news.url = x['url']
            
              try:
                news.save()
                print('it works')
              except:
                pass
          
          
            time.sleep(self.interval)
            

            def arbs(self):
                # COSS API
                import os
                import requests
                import json
                import urllib
                import hashlib
                import hmac
                import time
                from enum import Enum
                import datetime
                import http.client
                import urllib.parse
                from urllib.parse import urlencode, quote_plus

                symbol= ['NEO_ETH','ETH_BTC','NEO_BTC','LTC_BTC','XRP_ETH','EOS_ETH','DASH_BTC','XLM_BTC','ADA_ETH','XRP_BTC','ETC_BTC','TRX_ETH','ZEC_BTC','ETH_USDT','BTC_USDT','LTC_ETH','EOS_BTC','XLM_ETH','ONT_BTC','ONT_ETH','ATOM_BTC','ATOM_ETH',]
                case_list = []
                #pureba symbolo:
                #COSS   LTC-BTC
               
                for x in symbol:
                  moneda ="a"
                  symbol ="a"
                  symbolbitstamp="a"
                  marketpricecossbuy="a"
                  marketpricecosssell ="a"
                  marketpricekcsbuy="a"
                  marketpricekcssell="a"
                  marketpricebiboxbuy="a"
                  marketpricebiboxsell="a"
                  marketpricebinancebuy="a"
                  marketpricebinancesell="a"
                  marketpricekrakenbuy="a"
                  marketpricekrakensell="a"
                  marketpricecoinmatebuy="a"
                  marketpricecoinmatesell="a"
                  marketpricehitbtcbuy="a"
                  marketpricehitbtcsell="a"
                  marketpricekrakensell="a"
                  marketpricegeminibuy="a"
                  marketpricegeminisell ="a"
                  marketpricebitfinexbuy="a"
                  marketpricebitfinexsell="a"
                  marketpricebitstampbuy="a"
                  marketpricebitstampsell="a"
                  marketpricecoinbenesell="a"
                  marketpriceokexsell="a"
                  marketpricecoinbenebuy="a"
                  marketpriceokexbuy ="a"
                  marketpricehuboibuy ="a"
                  marketpricehuboisell ="a"
                  percentage="a"
                  ganancia="a"
                  pricecompra="a"
                  priceventa="a"
                  exchangecompra="A"
                  exchangeventa="A"
                  appa="a"
                  


                  
                  def Cossmarketdepthsymbol(symbol):
                    url = 'https://engine.coss.io/api/v1/dp?symbol='+symbol
                    response = requests.get(url)
                    res = response.json()

                    return res

                  moneda = x
                  try:
                    getinformation = Cossmarketdepthsymbol(moneda)
                    cossbuyprice = getinformation['asks'][0]
                    marketpricecossbuy = float(cossbuyprice[0])

                    marketpricecosssell = getinformation['bids'][0]
                    marketpricecosssell = float(marketpricecosssell[0])
                  except:
                    pass


                  #Kucoin
                  def kucoinbuyprice(symbol):
                    url = 'https://openapi-v2.kucoin.com/api/v1/market/orderbook/level2_20?symbol=' + symbol
                    response = requests.get(url)
                    res = response.json()
                    return res
                  
                  x = moneda
                
                  if x == 'ETH_BTC':
                    moneda = 'ETH-BTC'
                  if x == 'NEO_BTC':
                    moneda = 'NEO-BTC'
                  if x == 'LTC_BTC':
                    moneda = 'LTC-BTC'
                  if x == 'XRP_ETH':
                    moneda = 'XRP-ETH'
                  if x == 'EOS_ETH':
                    moneda = 'EOS-ETH' 
                  if x == 'DASH_BTC':
                    moneda = 'DASH-BTC' 
                  if x == 'XLM_BTC':
                    moneda = 'XLM-BTC'
                  if x == 'ADA_ETH':
                    moneda = 'ADA-ETH'
                  if x == 'XRP_BTC':
                    moneda = 'XRP-BTC'
                  if x == 'ETC_BTC':
                    moneda = 'ETC-BTC'
                  if x == 'TRX_ETH':
                    moneda = 'TRX-ETH'
                  if x == 'ZEC_BTC':
                    moneda = 'ZEC-BTC'
                  if x == 'ETH_USDT':
                    moneda = 'ETH-USDT'
                  if x == 'BTC_USDT':
                    moneda = 'BTC-USDT'
                  if x == 'LTC_ETH':
                    moneda = 'LTC-ETH'
                  if x == 'EOS_BTC':
                    moneda = 'EOS-BTC'
                  if x == 'XLM_ETH':
                    moneda = 'XLM-ETH'
                  if x == 'ONT_BTC': 
                    moneda= 'ONT-BTC'
                  if x == 'ONT_ETH': 
                    moneda= 'ONT-ETH'
                  if x == 'NEO_ETH': 
                    moneda= 'NEO-ETH' 
                  if x == 'ATOM_BTC': 
                    moneda= 'ATOM-BTC'
                  if x == 'ATOM_ETH': 
                    moneda= 'ATOM-ETH'

                  try:
                    getkcs = kucoinbuyprice(moneda)

                    kcsbuyprice = getkcs['data']['asks'][0][0]

                    marketpricekcsbuy = float(kcsbuyprice)

                    kcssellprice = getkcs['data']['bids'][0][0]
                    marketpricekcssell = float(kcssellprice)
                  except:
                    pass

                #OKEX USES SAME SYMBOLS AS KUCOINS BTC-USDT
                  

                  def okex(moneda):
                    url= 'https://www.okex.com/api/spot/v3/instruments/'+moneda+'/book?size=5'
                    response = requests.get(url)
                    res = response.json()
                    return res

                  try:
                    getokex = okex(moneda)
                    marketpriceokexbuy = float(getokex['asks'][0][0])
                    marketpriceokexsell = float(getokex['bids'][0][0])
                  except:
                    pass
                


                  def biboxbuyprice(symbol):
                      url = "https://api.bibox.com/v1/mdata?cmd=depth&pair=" + symbol + "&size=10" 
                      response = requests.get(url)
                      res = response.json()
                      return res

                  moneda = x
                  try:
                    getprices = biboxbuyprice(moneda)

                    biboxbuyprice = getprices['result']['asks'][0]['price']
                    marketpricebiboxbuy = float(biboxbuyprice)

                    biboxsellingprice = getprices['result']['bids'][0]['price']
                    marketpricebiboxsell = float(biboxsellingprice)
                  except: 
                    pass
                  # print (marketpricebiboxsell)



                  #####BINANCE
                  if x == 'ETH_BTC':
                    symbol = 'ETHBTC'
                  if x == 'NEO_BTC':
                    symbol = 'NEOBTC'
                  if x == 'LTC_BTC':
                    symbol = 'LTCBTC'
                  if x == 'XRP_ETH':
                    symbol = 'XRPETH'
                  if x == 'EOS_ETH':
                    symbol = 'EOSETH'
                  if x == 'DASH_BTC':
                    symbol = 'DASHBTC' 
                  
                  if x == 'XLM_BTC':
                    symbol = 'XLMBTC'
                  if x == 'ADA_ETH':
                    symbol = 'ADAETH'
                  if x == 'XRP_BTC':
                    symbol = 'XRPBTC'
                  if x == 'ETC_BTC':
                    symbol = 'ETCBTC'
                  if x == 'TRX_ETH':
                    symbol = 'TRXETH'
                  if x == 'ZEC_BTC':
                    symbol = 'ZECBTC'
                  if x == 'ETH_USDT':
                    symbol = 'ETHUSDT'
                  if x == 'BTC_USDT':
                    symbol = 'BTCUSDT'
                  if x == 'LTC_ETH':
                    symbol = 'LTCETH'
                  if x == 'EOS_BTC':
                    symbol = 'EOSBTC'
                  if x == 'XLM_ETH':
                    symbol = 'XLMETH'
                  if x == 'ONT_BTC': 
                    symbol= 'ONTBTC'
                  if x == 'ONT_ETH': 
                    symbol= 'ONTETH'
                  if x == 'NEO_ETH': 
                    symbol= 'NEOETH'
                  if x == 'ATOM_BTC': 
                    symbol= 'ATOMBTC'
                  if x == 'ATOM_ETH': 
                    symbol= 'ATOMETH'

                  def binancebuyprice(symbol):
                      url = "https://api.binance.com/api/v1/depth?symbol=" + symbol +"&limit=5"
                      response = requests.get(url)
                      res = response.json()
                      return res
                  try:
                    getpricesbinance = binancebuyprice(symbol)

                    binancebuyprice = getpricesbinance['asks'][0][0]
                    marketpricebinancebuy = float(binancebuyprice)

                    binancesellingprice = getpricesbinance['bids'][0][0]
                    marketpricebinancesell = float(binancesellingprice)
                  except:
                    pass
                  # print (marketpricebinancebuy)

                  #coinbene same as Binance
                  def coinbene(symbol):
                    url = 'https://api.coinbene.com/v1/market/orderbook?symbol='+symbol+'&depth=2'

                    response = requests.get(url)
                    res = response.json()
                    return res
                  # marketpricebitfinexbuy = float(res[0][3])
                  # marketpricebitfinexsell = float(res[0][1])
                  try:
                    getpricecoinbene = coinbene(symbol)
                    marketpricecoinbenebuy = float(getpricecoinbene['orderbook']['asks'][0]['price'])
                    marketpricecoinbenesell = float(getpricecoinbene['orderbook']['bids'][0]['price'])

                  except:
                    pass

                  #huboi same as binance

                  def huboi(symbol):
                    
                    url = 'https://api.huobi.com/market/depth?symbol='+symbol+'&type=step1&depth=5'
                    response = requests.get(url)
                    res = response.json()
                    return res

                  try:
                
                    getpricehuboi = huboi(symbol.lower())
                    marketpricehuboibuy = float(getpricehuboi['tick']['asks'][0][0])
                    marketpricehuboisell = float(getpricehuboi['tick']['bids'][0][0])
                  
                  except:
                    pass

                  def bitstamp(symbolbitstamp):
                  #ethbtc,ltcbtc,xrpbtc use sim as binance
                    url = 'https://www.bitstamp.net/api/v2/ticker/'+symbolbitstamp
                    response = requests.get(url)
                    res = response.json()
                  
                    return res
                  symbolbitstamp="a"
                  if x == 'ETH_BTC':
                    symbolbitstamp = 'ethbtc'
                  if x == 'LTC_BTC':
                    symbolbitstamp = 'ltcbtc'
                  if x == 'XRP_BTC':
                    symbolbitstamp = 'xrpbtc'

                  try:
                    getpricesbitstamp = bitstamp(symbolbitstamp)
                    marketpricebitstampbuy = float(getpricesbitstamp['ask'])
                    marketpricebitstampsell = float(getpricesbitstamp['ask'])
                  except:
                    pass
                
                  ###GEMINI
                  def gemini(symbol):
                    url = 'https://api.gemini.com/v1/book/'+symbol+'?limit_asks=2&limit_bids=2'
                      # url = 'https://api.hitbtc.com/api/2/public/symbol'
                    response = requests.get(url)
                    res = response.json()
                    return res

                  try:
                    gemini = gemini(symbol)
                    marketpricegeminibuy = float(gemini['asks'][0]['price'])
                    marketpricegeminisell= float(gemini['bids'][0]['price'])
                  except:
                    pass
                  #####KRAKEN
                  
                  if x == 'ETH_USDT':
                    symbol = 'ETHUST'
                  if x == 'BTC_USDT':
                    symbol = 'BTCUST'
                  if x == 'ATOM_BTC':
                    symbol = 'ATOBTC'
                  if x == 'ATOM_ETH':
                    symbol = 'ATOETH'

                  def bitfinex(symbol):
                    #we can use binance symbol for bitfinex
                    url = 'https://api-pub.bitfinex.com/v2/tickers?symbols=t'+symbol

                    # url = 'https://api.hitbtc.com/api/2/public/symbol'
                    response = requests.get(url)
                    res = response.json()
                    return res

                  try:
                    getpricesbitfinex = bitfinex(symbol)
                    marketpricebitfinexbuy = float(getpricesbitfinex[0][3])
                    marketpricebitfinexsell = float(getpricesbitfinex[0][1])
                  except:
                    pass

                  def krakenbuyprice(symbol):
                      url = "https://api.kraken.com/0/public/Depth?pair=" + symbol +"&count=10"
                      response = requests.get(url)
                      res = response.json()
                      return res

                  if x == 'ETH_BTC':
                    symbol = 'ETHXBT'
                
                  if x == 'EOS_ETH':
                    symbol = 'EOSETH'
                  if x == 'DASH_BTC':
                    symbol='DASHXBT'
                  if x == 'XLM_BTC':
                    symbol='XLMXBT'
                  if x =='ADA_ETH':
                    symbol='ADAETH'
                  if x =='XRP_BTC':
                    symbol='XRPXBT'
                  if x == 'ETC_BTC':  
                    symbol='ETCXBT' 
                  if x == 'TRX_ETH':
                    symbol = 'TRXETH'
                  if x == 'ZEC_BTC':
                    symbol = 'ZECXBT'
                  if x == 'ETH_USDT':
                    symbol = 'ETHUSDT'
                  if x == 'BTC_USDT':
                    symbol = 'BTCUSDT'
                  if x == 'LTC_BTC':
                    symbol = 'LTCBTC'
                  if x == 'LTC_ETH':
                    symbol = 'LTCETH'
                  if x == 'EOS_BTC':
                    symbol = 'EOSBTC'
                  if x == 'XLM_ETH':
                    symbol='XLMETH'
                  if x == 'ONT_BTC': 
                    symbol= 'ONTBTC'
                  if x == 'ONT_ETH': 
                    symbol= 'ONTETH'
                  if x == 'NEO_ETH': 
                    symbol= 'NEOETH'
                  if x == 'ATOM_BTC': 
                    symbol= 'ATOMXBT'
                  if x == 'ATOM_ETH': 
                    symbol= 'ATOMETH'

                  try:
                    getkrakenprice = krakenbuyprice(symbol)
                    if x == 'ETH_BTC':
                      symbol = 'XETHXXBT'
                    if x == 'XLM_BTC':
                      symbol = 'XXLMXXBT'
                    if x == 'XRP_BTC':
                      symbol = 'XXRPXXBT'
                    if x == 'ETC_BTC':  
                      symbol = 'XETCXXBT'
                    if x == 'ZEC_BTC':
                      symbol = 'XZECXXBT'
                    

                    krakenbuyprice = getkrakenprice['result'][symbol]['asks'][0][0]
                    marketpricekrakenbuy = float(krakenbuyprice)

                    krakensellingprice = getkrakenprice['result'][symbol]['bids'][0][0]
                    marketpricekrakensell = float(krakensellingprice)
                  except:
                    pass
                  def coinmate(symbol):
                    url = 'https://coinmate.io/api/orderBook?currencyPair='+ symbol +'&groupByPriceLimit=False'
                    response = requests.get(url)
                    res = response.json()
                    return res

                  moneda = x
                  try:
                    getcoinmate = coinmate(moneda)
                    marketpricecoinmatebuy= float(getcoinmate['data']['asks'][0]['price'])
                    marketpricecoinmatesell = float(getcoinmate['data']['bids'][0]['price'])
                  except: 
                    pass

                  #HITBTC

                  if x == 'ETH_BTC':
                    symbol = 'ETHBTC'
                  if x == 'NEO_BTC':
                    symbol = 'NEOBTC'
                  if x == 'LTC_BTC':
                    symbol = 'LTCBTC'
                  if x == 'XRP_ETH':
                    symbol = 'XRPETH'
                  if x == 'EOS_ETH':
                    symbol = 'EOSETH'
                  if x == 'DASH-BTC':
                    symbol = 'DASHBTC' 
                  if x == 'XLM_BTC':
                    symbol = 'XLMBTC'
                  if x == 'ADA_ETH':
                    symbol = 'ADAETH'
                  if x == 'XRP_BTC':
                    symbol = 'XRPBTC'
                  if x == 'ETC_BTC':
                    symbol = 'ETCBTC'
                  if x == 'TRX_ETH':
                    symbol = 'TRXETH'
                  if x == 'ZEC_BTC':
                    symbol = 'ZECBTC'
                  if x == 'ETH_USDT':
                    symbol = 'ETHUSD'
                  if x == 'BTC_USDT':
                    symbol = 'BTCUSD'
                  if x == 'LTC_ETH':
                    symbol = 'LTCETH'
                  if x == 'EOS_BTC':
                    symbol = 'EOSBTC'
                  if x == 'XLM_ETH':
                    symbol = 'XLMETH'
                  if x == 'ONT_BTC': 
                    symbol= 'ONTBTC'
                  if x == 'ONT_ETH': 
                    symbol= 'ONTETH'
                  if x == 'NEO_ETH': 
                    symbol= 'NEOETH'
                  if x == 'ATOM_BTC': 
                    symbol= 'ATOMBTC'
                  if x == 'ATOM_ETH': 
                    symbol= 'ATOMETH'

                  def hitbtc(symbol):
                    url = 'https://api.hitbtc.com/api/2/public/ticker/'+symbol
                    response = requests.get(url)
                    res = response.json()
                    return res
                  
                  try:
                    getpricesbithtc = hitbtc(symbol)

                    hitbtcbuyprice = getpricesbithtc['ask']
                    marketpricehitbtcbuy = float(hitbtcbuyprice)

                    hitbtcsellprice = getpricesbithtc['bid']
                    marketpricehitbtcsell = float(hitbtcsellprice)
                  except:
                    pass

                  dictionariopreciocompra = {}
                  dictionarioprecioventa = {}
                  moneda = x
                  print(x)
                  print('coss:'+ str(marketpricecossbuy),'bibox:'+ str(marketpricebiboxbuy),'binance:'+str(marketpricebinancebuy),'kraken:'+str(marketpricekrakenbuy),'coinmate:'+str(marketpricecoinmatebuy),'kcs:'+str(marketpricekcsbuy),'hitbtc:'+str(marketpricehitbtcbuy),'gemini:'+str(marketpricegeminibuy),'bitfinex:'+str(marketpricebitfinexbuy),'bitstamp:'+str(marketpricebitstampbuy),'okex:'+str(marketpriceokexbuy),'coinbene:'+str(marketpricecoinbenebuy),'huboi:'+str(marketpricehuboibuy))

                  if x == 'ETH_BTC':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy,'coinmate':marketpricecoinmatebuy, 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'gemini':marketpricegeminibuy,'bitfinex':marketpricebitfinexbuy,'bitstamp':marketpricebitstampbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kraken':marketpricekrakensell,'coinmate': marketpricecoinmatesell,'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'gemini':marketpricegeminisell,'bitfinex':marketpricebitfinexsell,'bitstamp':marketpricebitstampsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}
                  if x == 'NEO_BTC':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy }
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell}
                  if x == 'NEO_ETH':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy }
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,}
                  if x == 'LTC_BTC':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'coinmate':marketpricecoinmatebuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'gemini':marketpricegeminibuy,'bitfinex':marketpricebitfinexbuy,'bitstamp':marketpricebitstampbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'coinmate': marketpricecoinmatesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'gemini':marketpricegeminisell,'bitfinex':marketpricebitfinexsell,'bitstamp':marketpricebitstampsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}
                  if x == 'XRP_ETH':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'okex':marketpriceokexbuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'okex':marketpriceokexsell}
                  if x == 'EOS_ETH':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kraken':marketpricekrakensell,'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell}
                  if x == 'DASH_BTC':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy,'coinmate':marketpricecoinmatebuy, 'kucoin': marketpricekcsbuy,'okex':marketpriceokexbuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kraken':marketpricekrakensell,'coinmate': marketpricecoinmatesell,'kucoin': marketpricekcssell,'okex':marketpriceokexsell,'huboi':marketpricehuboisell}
                  if x == 'XLM_BTC':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy, 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell, 'binance':marketpricebinancesell, 'kraken':marketpricekrakensell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}

                  if x == 'ADA_ETH':
                    dictionariopreciocompra = {'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy, 'hitbtc':marketpricehitbtcbuy,'okex':marketpriceokexbuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'binance':marketpricebinancesell, 'kraken':marketpricekrakensell, 'hitbtc':marketpricehitbtcsell,'okex':marketpriceokexsell,'huboi':marketpricehuboisell}

                  if x == 'XRP_BTC':
                  
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy,'coinmate':marketpricecoinmatebuy, 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'bitstamp':marketpricebitstampbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kraken':marketpricekrakensell,'coinmate': marketpricecoinmatesell,'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'bitstamp':marketpricebitstampsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}

                  if x == 'ETC_BTC':
                    
                    dictionariopreciocompra = {'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kraken':marketpricekrakensell,'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}

                  if x == 'TRX_ETH':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell}
                  if x == 'ZEC_BTC':
                    dictionariopreciocompra = {'binance': marketpricebinancebuy , 'kraken':marketpricekrakenbuy,'hitbtc':marketpricehitbtcbuy,'gemini':marketpricegeminibuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'binance':marketpricebinancesell, 'kraken':marketpricekrakensell,'hitbtc':marketpricehitbtcsell,'gemini':marketpricegeminisell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}
                  if x == 'ETH_USDT':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy ,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}
                  if x == 'BTC_USDT':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy ,  'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell,'huboi':marketpricehuboisell}
                  if x == 'LTC_ETH':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy , 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'gemini':marketpricegeminibuy,'okex':marketpriceokexbuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'gemini':marketpricegeminisell,'okex':marketpriceokexsell}
                  if x == 'EOS_BTC':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'bibox':marketpricebiboxbuy, 'binance': marketpricebinancebuy, 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'coinbene':marketpricecoinbenebuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell,'bibox':marketpricebiboxsell, 'binance':marketpricebinancesell,'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'coinbene':marketpricecoinbenesell}
                  if x == 'XLM_ETH':
                    dictionariopreciocompra = {'coss':marketpricecossbuy, 'binance': marketpricebinancebuy, 'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'coss':marketpricecosssell, 'binance':marketpricebinancesell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell,'huboi':marketpricehuboisell}
                  if x == 'ONT_BTC':
                    dictionariopreciocompra = {'binance': marketpricebinancebuy,'bibox':marketpricebiboxbuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'okex':marketpriceokexbuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'binance':marketpricebinancesell,'bibox':marketpricebiboxsell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'okex':marketpriceokexsell,'huboi':marketpricehuboisell}
                  if x == 'ONT_ETH':
                    dictionariopreciocompra = {'binance': marketpricebinancebuy,'bibox':marketpricebiboxbuy,'kucoin': marketpricekcsbuy,'hitbtc':marketpricehitbtcbuy,'okex':marketpriceokexbuy,'huboi':marketpricehuboibuy}
                    dictionarioprecioventa = {'binance':marketpricebinancesell,'bibox':marketpricebiboxsell, 'kucoin': marketpricekcssell,'hitbtc':marketpricehitbtcsell,'okex':marketpriceokexsell,'huboi':marketpricehuboisell}
                  if x == 'ATOM_BTC':
                    dictionariopreciocompra = {'binance': marketpricebinancebuy,'kraken':marketpricekrakenbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy}
                    dictionarioprecioventa = {'binance': marketpricebinancesell,'kraken':marketpricekrakensell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell}
                  if x == 'ATOM_ETH':
                    dictionariopreciocompra = {'bibox': marketpricebiboxbuy,'kraken':marketpricekrakenbuy,'bitfinex':marketpricebitfinexbuy,'okex':marketpriceokexbuy}
                    dictionarioprecioventa = {'bibox': marketpricebiboxsell,'kraken':marketpricekrakensell,'bitfinex':marketpricebitfinexsell,'okex':marketpriceokexsell}

                  minpricecompra = (min(dictionariopreciocompra.items(), key=lambda k: k[1]))
                  exchangecompra = minpricecompra[0]
                  pricecompra= minpricecompra[1]

                  maxpriceventa = (max(dictionarioprecioventa.items(), key=lambda k: k[1]))
                  exchangeventa = maxpriceventa[0]
                  priceventa= maxpriceventa[1]

                  percentage = ((priceventa - pricecompra)/pricecompra)*100
                  print(percentage)
                  
                  #check for percentage to be at least 0.5%
                  if percentage > 0.2:
                    if pricecompra < priceventa:
                            
                            # print (percentage)
                            difference = pricecompra - priceventa
                            
                            compra = ((pricecompra) + ((pricecompra)*0.0015))
                            venta = (priceventa  - ((priceventa)*0.0015))
                            ganancia = venta - compra

                          
                            # print(exchangecompra)
                            # print(exchangeventa)
                            # print(ganancia)
                            # print(pricecompra)
                            # print(priceventa)
                          
                            # pair = x
                            # dictforwebsite['pair'] = x
                            # dictforwebsite['exchangecompra'] = exchangecompra
                            # dictforwebsite['exchangeventa'] = exchangeventa
                            
                            
                            
                            case = {'pair': x, 'exchangecompra': exchangecompra, 'exchangeventa':exchangeventa,'percentage':percentage,'pricecompra':pricecompra,'priceventa':priceventa,'ganancia':ganancia }
                            case_list.append(case)

                # context = {
                #   'arbs':case_list,
                #   'len': len(case_list)
                # } 
                # return render(request,'arbs.html', context)


                #CASELIST is what I send in the View function to website

                  for item in case_list:
                    
                    arbsfound = Arbscrypto()
                    arbsfound.pair = item['pair']
                    arbsfound.exchangebuy = item['exchangecompra']
                    arbsfound.exchangesell = item['exchangeventa']
                    arbsfound.percentage = item['percentage']
                    arbsfound.buyprice = item['pricecompra']
                    arbsfound.sellingprice = item['priceventa']
                    arbsfound.gain = item['ganancia']

                    
                    try:
                      arbsfound.save()
                      print('arbs works')
                    except:
                      pass

            
            arbs(self)
           
    
      
example = ThreadingExample()
# # time.sleep(20)

# # time.sleep(20)



            


#proband
#ctrol z