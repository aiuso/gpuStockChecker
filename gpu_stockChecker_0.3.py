import global_vars as g
import navigate
import time
import send
import schedule


##### URLs

url = {'evga'   : 'https://www.evga.com/products/product.aspx?pn=10G-P5-3885-KR',
       'bestbuy': 'https://www.bestbuy.com/site/evga-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card/6432400.p?skuId=6432400',
       'newegg' : 'https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3883-kr/p/N82E16814487521?Description=rtx%203080&cm_re=rtx_3080-_-14-487-521-_-Product&quicklink=true',
       'amazon' : 'https://www.amazon.com'
       }


##### GPU

g.gpu = 'EVGA RTX 3080 XC3 Ultra'
g.stop_count = 0
print(f'Started searching for {g.gpu} at {send.timestamp()}...')
print('____________\n')


##### Search Functions

def search_evga():
    navigate.search(url.get('evga'))
    out_of_stock = g.driver.find_elements_by_id("LFrame_pnlOutOfStock") # elements will return empty list [] if element absent
    if out_of_stock:
        print(f'Out of Stock at EVGA. {send.timestamp()}')
    else:
        print(f'{send.timestamp()}... {g.gpu} may be in stock at EVGA! Check url: {url.get("evga")}')
        print(send.discord_msg(f'{send.timestamp()}... {g.gpu}'
                               f' may be in stock at EVGA! Check url: {url.get("evga")}'))
        g.stop_count += 1

    time.sleep(5)


def search_bestbuy():
    navigate.search(url.get('bestbuy'))
    out_of_stock = g.driver.find_elements_by_class_name('add-to-cart-button')
    if out_of_stock:
        if 'sold' in out_of_stock[0].text.lower():
            print(f'Out of Stock at BestBuy. {send.timestamp()}')
        else:
            print(f'{send.timestamp()}... {g.gpu} may be in stock at BestBuy! Check url: {url.get("bestbuy")}')
            print(send.discord_msg(f'{send.timestamp()}... {g.gpu}'
                                   f' may be in stock at BestBuy! Check url: {url.get("bestbuy")}'))
            g.stop_count += 1
    time.sleep(5)


def search_newegg():
    navigate.search(url.get('newegg'))
    pointer = g.driver.find_elements_by_class_name('product-inventory')
    out_of_stock_msg = pointer[0].text.lower()
    if 'out' in out_of_stock_msg:
        print(f'Out of Stock at Newegg. {send.timestamp()}')
    else:
        print(f'{send.timestamp()}... {g.gpu} may be in stock at Newegg! Check url: {url.get("newegg")}')
        print(send.discord_msg(f'{send.timestamp()}... {g.gpu}'
                               f' may be in stock at Newegg! Check url: {url.get("newegg")}'))
        g.stop_count += 1
    time.sleep(5)


def search_etailers():
    search_evga()
    search_bestbuy()
    search_newegg()


##### Searches

navigate.open_browser()
schedule.every(1).minutes.do(send.scheduled_msg)

while g.stop_count < 2:
    schedule.run_pending()
    search_etailers()
    time.sleep(1)




