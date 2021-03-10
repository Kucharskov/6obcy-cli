# 6obcy-cli
The repository contains a program that was developed as part of the Engineer's Thesis.

The presentation of the work took place on the day: **19.06.2020**

The code was made public in this repository on the day: **10.03.2021** due to minor changes on 6obcy that cause the script to not work.

<p align="center">
<img src="https://github.com/Kucharskov/6obcy-cli/blob/master/images/interface.png?raw=true"><br>
</p>

After decrypting and analyzing the client code at [6obcy.org](https://6obcy.org/) I came across to a websocket connection. Then I analyzed the network traffic. When I got to know the structure and data kept in packets I decided to write my own terminal client.

Analysis and legal aspect to read [here](https://github.com/Kucharskov/6obcy-cli/blob/master/ANALYZE.md)

## The idea
On 6obcy.org chat I met a lot of people, including my ex-fiancée, who was supposed to support me in creating this project. From time to time I look there writing with people. One day, I thought to make a one day long chart to know when there are most people to talk to.
That's how the analysis of the whole client side started.

## Usage
For legal reasons, the application should not work any more. But to run that program firstly I suggest install all required packets using command:

``pip3 install -r requirements.txt``

Then just run it using:

``python3 6obcy-cli.py`` or ``./6obcy-cli.py``

## Commands
There few commands which starts from dot. At first I implemented basic commands reflecting the buttons on the page:
- ``.help`` to show help menu
- ``.join`` to start conversation with stranger
- ``.quit`` to close conversation with stranger
- ``.next`` technically fast quit, join
- ``.count`` shows a number of strangers
- ``.report`` to report a stranger during conversation
- ``.topic`` selects a randomized thread (server side implementation)
- ``.exit`` to close app

I also provided some of my external commands to do some usefull stuff:
- ``.impersonate`` establishes a connection through a trusted random proxy server
- ``.reconnect`` re-establish direct connection
- ``.obfuscate`` enables/disables the obfuscation of words using homoglyphs
- ``.debug`` displays technical data

## Acknowledgements
Due to the lack of any control over the selected person and the repetition of the interlocutor, I had to spend a lot of time just looking for people who understood my need to test this software.

I asked each of the testers, if I could, if they wanted to be mentioned in the acknowledgments. In order to avoid legal problems concerning publication of personal data of third parties, in case of consent, I asked for any pseudonym.

At this point, I would like to thank very much, above all to testers who introduced themselves as: **AMI**, **Antkovsky**, **Milka**, **MiłySeba**, **Nesska**, **PasGGuda**, **Talib22** and **Venour**, because without them I wouldn't be able to perform such detailed tests of the created application. Apart from the above mentioned, thanks are also for the administration of the 6obcy and to those who did not manage or did not want to be mentioned.

Thank you for the many good words, the jokes and the multitude of symbols they sent out, because in that way I got the support that someone else was supposed to give me.