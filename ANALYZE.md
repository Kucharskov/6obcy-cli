# 6obcy analyze

## The idea
On 6obcy.org chat I met a lot of people, including my ex-fiancée, who was supposed to support me in creating this project. From time to time I look there writing with people. One day I found out that I will make a day-long chart to know when there are most people to know.
That's how the analysis of the whole client side started.

## Legal aspect
*some stuff needs to be added here* but the Administrator was notified.

## Analyze
In the HTML code I noticed that the number of logged in users was always 1000, even though it was refreshed live on the page. It directed me to the JavaScript code and searching for the right request. When I found ``scriptBoxEio.js`` file, which was the only non-standard file besides default external libraries, I decided to analyze it.

The whole code was obfuscated, but it's nothing unusual. At the beginning of the file there was a large table containing 2341 elements. Unfortunately, content like ``lyqvxg``, ``vckligh``, ``ufmxgrlm`` didn't tell me much. Looking at the elements in the console, I noticed that they have more readable values. Deeper in the code I found the declared function ``_sz8x_dec`` and its calling on the array elements. I did a simple test, after calling the function on the value ``123abc`` and I got ``123zyx``. This led me to the Atbash - a monoalphabetic substitution cipher with reversed alphabet letters order. Thus, the above mentioned values turned into ``object``, ``exports``, ``function``, which meant that it is an array for mapping elements in the code.

I had to find decoders that can analyze over five thousand lines of semi-readable code. Finally I used [rumkin.com Atbash decoder](http://rumkin.com/tools/cipher/atbash.php), [JavaScript remapper](http://output.jsbin.com/hazevo/1) and lastly [JavaScript Beautifier](https://beautifier.io/), which made the code much easier to analyze. In this way I found the address and range of ports to the final endpoint and information about the engine.io used for communication. Unfortunately, the whole client code has been encapsulated so all I have to do is to run the developer console in Chrome and start the traffic analysis.

## Packets structure and leading number
Each package has a leading number. These numbers are in accordance with the [engine.io protcol](https://github.com/socketio/engine.io-protocol) documentation which i found on the web. The documentation found describes the required "heartbeat" mechanism, which maintains the client-server connection. It consists of sending at equal intervals a message with code ``2`` to which the server responds with a message with code ``3``.

## Server side packets
After a lot of conversations to generate traffic and hours of analysis of the generated traffic I managed to describe most of the packets.

Initialize connection (always first packet)
```
0{"sid":"XXXXXXXXXXXXXXX","upgrades":[],"pingInterval":25000,"pingTimeout":40000}
```

Connection accept (most second packet) - contains a hash used to sign a packet
```
4{"ev_name":"cn_acc","ev_data":{"conn_id":"XXXXXXXXXXXXXXX","hash":"127#0#0#1"}}
```

New chat proposal - ckey is used in almost all client packets
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

Conversation request - "loc" have a predefined values coressponding to voivodeships (Silesian is 7)
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

I really dont know (but in implementation I send it too as original client sends)
```
4{"ev_name":"_owack"}
```