# 6obcy-cli
*stuff to add here*  After decrypting and analyzing the client code at [6obcy.org](https://6obcy.org/) I came across a websocket connection. After analyzing the order and content of packages I decided to write my own client.

## Usage
First i suggest install all required packets using command ``pip3 install -r requirements.txt
`` Then just run it using python3 or ``./6obcy-cli.py``

## Commands
There few commands which starts from dot. All other content are treated as messages.

- ``.join`` to start conversation with stranger
- ``.quit`` to close conversation with stranger
- ``.next`` technically fast quit, join
- ``.report`` to report a stranger during conversation
- ``.topic`` selects a randomized thread (server side implementation)
- ``.count`` shows a number of strangers
- ``.exit`` to close app


## Part of analyze
### Idea of that project
The idea to write the application was born while having fun at the chat. I noticed that there are always 1000 connected users in the page sourcecode. This way I found the source file scriptBoxEio.js.

Having experience in reverse engineering JavaScript code, with the help of available tools on the network, I developed an obfuscation array and replaced the calls in the code. Additionally, I had to figure out how to decrypt the array. Using the method which operates on the array I saw that was an Atbash cipher (alphabet written in reverse order). After analyzing the "engine" encapsulated in jQuery, I came across websocket connections. And that was a good lead.


### Server side packets
After a lot of conversations to generate traffic and hours of analysis of the generated traffic I managed to describe most of the packets.

Initialize connection (always first packet)
```
josn
0{"sid":"XXXXXXXXXXXXXXX","upgrades":[],"pingInterval":25000,"pingTimeout":40000}

```

Connection accept
```
4{"ev_name":"cn_acc","ev_data":{"conn_id":"XXXXXXXXXXXXXXX","hash":"127#0#0#1"}}
```

New chat proposal
```
4{"ev_name":"talk_s","ev_data":{"cid":000000000,"ckey":"0:000000000_XXXXXXXXXXXXX","flaged":false}}
```

Received message
```
4{"ev_name":"rmsg","ev_data":{"post_id":0,"cid":000000000,"msg":"message_content_here"}}
```

Stranger disconnect conversation
```
4{"ev_name":"sdis","ev_data":000000000}
```

Stranger is typing
```
4{"ev_name":"styp","ev_data":true}
4{"ev_name":"styp","ev_data":false}
```

Received random topic from server-side magic
```
4{"ev_name":"rtopic","ev_data":{"post_id":0,"cid":000000000,"topic":"topic_content_here","who": 0}}
```

Advertisement
```
4{"ev_name":"r_svmsg","ev_data":"Zaproś znajomych na 6obcy, kliknij [...]"}
```

### Client side packets
Client init parameters
```
4{"ev_name":"_cinfo","ev_data":{"cvdate":"2017-08-01","mobile":false,"cver":"v2.5","adf":"ajaxPHP","hash":"127#0#0#1","testdata":{"ckey":0,"recevsent":false}}}
```

Conversation request
```
4{"ev_name":"_sas","ev_data":{"channel":"main","myself":{"sex":0,"loc":0},"preferences":{"sex":0,"loc":0}},"ceid":0}
```

Accept of new chat
```
4{"ev_name":"_begacked","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX"},"ceid":0}
```

Client disconnection
```
4{"ev_name":"_distalk","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX"},"ceid":0}
```

Typing information
```
4{"ev_name":"_mtyp","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX","val":true}}
4{"ev_name":"_mtyp","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX","val":false}}
```

Send message
```
4{"ev_name":"_pmsg","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX","msg":"message_content_here","idn":1},"ceid":0}
```

Report stranger
```
4{"ev_name":"_reptalk","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX"},"ceid":0}
```

Random topic request
```
4{"ev_name":"_randtopic","ev_data":{"ckey":"0:000000000_XXXXXXXXXXXXX"},"ceid":0}
```

I really dont know, but i send it too
```
4{"ev_name":"_owack"}
```

### Packets leading number
Each package has a leading number. These numbers are in accordance with the [engine.io protcol](https://github.com/socketio/engine.io-protocol) documentation that was used on the site.

The code also includes the required "heartbeat" mechanism, which maintains the client-server connection. It consists of sending at equal intervals a message with code "2" to which the server responds with a message with code "3".
