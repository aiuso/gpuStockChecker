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
        print(f"EVGA 'Out of Stock' banner was not found.. checking add to cart. {send.timestamp()}")
        add_to_cart = g.driver.find_elements_by_class_name("AddToChat")

        if 'add' in add_to_cart[0].text.lower():
            g.stop_count += 1
            print(f"EVGA 'Add to Cart' button was found.. sending notification {send.timestamp()}.")
            print(send.discord_msg(f'{send.timestamp()}... {g.gpu}'
                                   f' may be in stock at EVGA! Check url: {url.get("evga")}'))
        else:
            print(f"EVGA 'Add to Cart' button was not found. {send.timestamp()}.")

    time.sleep(15)


def search_bestbuy():
    navigate.search(url.get('bestbuy'))
    button = g.driver.find_elements_by_class_name('add-to-cart-button')

    if button:
        if 'sold' in button[0].text.lower():
            print(f'Out of Stock at BestBuy. {send.timestamp()}')

        elif 'coming' in button[0].text.lower():
            print(f'Coming Soon at BestBuy. {send.timestamp()}')

        elif 'add' in button[0].text.lower():
            g.stop_count += 1
            print(f"Bestbuy 'Add To Cart' button was found... sending message{send.timestamp()}")
            print(send.discord_msg(f'{send.timestamp()}... {g.gpu}'
                                   f' may be in stock at BestBuy! Check url: {url.get("bestbuy")}'))

        else:
            print(f'Unfamiliar text on button. {send.timestamp()}')

    else:
        print(f'Could not locate the BestBuy button/banner. {send.timestamp()}')

    time.sleep(15)


def search_newegg():
    navigate.search(url.get('newegg'))
    banner = g.driver.find_elements_by_class_name('product-inventory')
    button = g.driver.find_elements_by_class_name('btn-wide')

    try:
        if 'out' in banner[0].text.lower():
            print(f'Out of Stock at Newegg. {send.timestamp()}')

        else:
            if 'add' in button[0].text.lower():
                g.stop_count += 1
                print(f"Newegg 'Add To Cart' button was found... sending message. {send.timestamp()}")
                print(send.discord_msg(f'{send.timestamp()}... {g.gpu}'
                                       f' may be in stock at Newegg! Check url: {url.get("newegg")}'))

            else:
                print(f'OoS banner not found. AtC button not found on Newegg... {send.timestamp()}')

    except IndexError:
        print('Unable to check Newegg site...')

    time.sleep(15)


def search_etailers():
    search_evga()
    search_bestbuy()
    search_newegg()


##### Searches

#send.discord_msg('')
#send.scheduled_msg()
navigate.open_browser()
schedule.every().day.at("16:00").do(send.scheduled_msg)

while g.stop_count < 1:
    schedule.run_pending()
    search_etailers()
    time.sleep(10)




