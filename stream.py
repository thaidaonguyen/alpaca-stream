import my_config as config
#import config
import websocket, json  
import boto3



STREAM_NAME = 'alpaca-firehose'  #Replace this name with the Kinesis Firehose you created in your account.

def on_open(ws):
    print("Opened Connection")
    auth_data = {"action": "auth", "key": config.API_KEY, "secret": config.SECRET_KEY}
    ws.send(json.dumps(auth_data))
    
    #subscribe to minute bars for all stocks
    #listen_message = {"action": "subscribe", "bars": ["*"]}

    #subscribe to daily bars for all stocks
    listen_message = {"action": "subscribe", "dailyBars": ["*"]}


    ws.send(json.dumps(listen_message))
    
def on_message(ws, message):
    data = json.loads(message)

    if data[0]['T'] not in ['error', 'success', 'subscription']:
        #print("Transaction message:")
        for i in data: 
            item={
                "type": i["T"],
                "ticker": i["S"],
                "open": i["o"],
                "high": i["h"],
                "low": i["l"],
                "close": i["c"], 
                "volume": i["v"],
                "timestamp": i["t"]
            }
            print(json.dumps(item)+ '\n')
            response = firehose_client.put_record(
                DeliveryStreamName=STREAM_NAME ,
                Record={
                        'Data': json.dumps(item)+ '\n'
                    }
                )
            # print("Firehose response:")
            # print(response)

def on_close(ws):
    print("Closed Connection")

def on_error(ws, error):
    print(error)

if __name__ == '__main__':
    session = boto3.Session(profile_name='default')
    firehose_client = session.client('firehose')

    socket = config.SOCKET_URL
    ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_error=on_error,on_close=on_close)
    ws.run_forever()