from dotenv import load_dotenv
import http.client
import datetime
import os


load_dotenv()


##### Timestamp

def timestamp():
    return datetime.datetime.now().strftime("%c")


##### Discord Messages

def discord_msg(message):   # Code Credit: Chris Garrett
    webhookurl = os.getenv('webhookurl')

    # compile the form data (BOUNDARY can be anything)
    formdata = "------:::BOUNDARY:::\r\nContent-Disposition: form-data; name=\"content\"\r\n\r\n"\
               + message + "\r\n------:::BOUNDARY:::--"

    # get the connection and make the request
    connection = http.client.HTTPSConnection("discordapp.com")
    connection.request("POST", webhookurl, formdata, {
        'content-type': "multipart/form-data; boundary=----:::BOUNDARY:::",
        'cache-control': "no-cache",
    })
    # get response
    response = connection.getresponse()
    result = response.read()

    # return back to the calling function with the result
    return result.decode("utf-8")


def scheduled_msg():
    print(discord_msg("Hope you're having a great day. I'm still actively searching for your 3080... Stand by."))








