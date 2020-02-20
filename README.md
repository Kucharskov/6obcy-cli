# 6obcy-cli
*some stuff needs to be added here* 

After decrypting and analyzing the client code at [6obcy.org](https://6obcy.org/) I came across to a websocket connection. Then I analyzed the network traffic. When I got to know the structure and data kept in packets I decided to write my own terminal client.

Part of the analysis to read [here](https://github.com/Kucharskov/6obcy-cli/blob/master/ANALYZE.md)

## Usage
First i suggest install all required packets using command:

``pip3 install -r requirements.txt``

Then just run it using:

``python3 6obcy-cli.py`` or ``./6obcy-cli.py``

## Commands
There few commands which starts from dot. All other content are treated as messages.
- ``.join`` to start conversation with stranger
- ``.quit`` to close conversation with stranger
- ``.next`` technically fast quit, join
- ``.report`` to report a stranger during conversation
- ``.topic`` selects a randomized thread (server side implementation)
- ``.count`` shows a number of strangers
- ``.exit`` to close app
