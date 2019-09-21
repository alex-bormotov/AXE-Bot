
[What means ignore buy, sell signals?](#what-means-ignore-buy-sell-signals)

[What do I need to use for login?](#what-do-i-need-to-use-for-login)

[What limitation DEMO version has?](#what-limitation-demo-version-has)

[How much cost the FULL version?](#how-much-cost-the-full-version)

[I changed my api keys and bot tell me that it is DEMO again, do I need to buy a new licence?](#i-changed-my-api-keys-and-bot-tell-me-that-it-is-demo-again-do-i-need-to-buy-a-new-licence)

[How check my licence time?](#how-check-my-licence-time)

[My licence still valid and it time not ended, but I wish make payment, how will changed licence time?](#my-licence-still-valid-and-it-time-not-ended-but-i-wish-make-payment-how-will-changed-licence-time)

[I want to install the bot on Windows (Recommended use Linux VPS ONLY!)](#i-want-to-install-the-bot-on-windows-Recommended-use-linux-vps-only)

[Are you store and know my exchange api keys?](#are-you-store-and-know-my-exchange-api-keys)

[I have another problem](#i-have-another-problem)

---



#### What means ignore buy, sell signals?

> For instance, bot receive signal BUY at price 1000, buy it, and then price goes down much more, to 700. Ignore feature allow ignore one or more signals and therefore buy at 700.

> There are two types this feature - `ignore times` and `ignore time`, `times` means how much times signal will be ignored, `time` means how much time bot will be wait before buy or sell after receiving signal. The same situation with SELL.

> `ignore_buy_cooldown_sec` and `ignore_sell_cooldown_sec` - it is time in seconds between ignore attempts, for instance, if `ignore_buy_cooldown_sec` = 10, after first ignoring attempt bot will be sleep 10 seconds before processing next attempts.

#### What limitation DEMO version has?

> Demo version has no functional and time limitation, but trade limit equal 0.03 BTC and allow trading with BTC only.

#### How much cost the FULL version?

> Full version for FREE (open source) since 09.21.2019

#### What do I need to use for login?

> Login is equal bot_id, you can take it from notification on telegram or from config/config.json (last string).
> bot_id will automatically generated while first start and saving to config.json, keep in mind that all your payments and licence will be connected to this bot_id, if you change it then you need to buy a new licence.

#### I changed my api keys and bot tell me that it is DEMO again, do I need to buy a new licence?

> NO! You need visit [this link](https://axe-bot-payments.axe-dev.com/flush-bot-hash), enter your bot_id and login for reset api keys. After that bot will registered new keys automatically (need restart the bot) and will be FULL version again.

#### How check my licence time?

> Go to [your profile](https://axe-bot-payments.axe-dev.com/profile) and click licence-info, then enter your bot_id.

#### My licence still valid and it time not ended, but I wish make payment, how will changed licence time?

> New time will be equal end date of current licence + 1 month.

#### I want to install the bot on Windows (Recommended use Linux VPS ONLY!)

> AXE Bot written on Python3, you can run it at whatever OS which supports Python3 and Docker.

> Install [Docker](https://docs.docker.com/docker-for-windows/install/) for Windows and then use the guide for [Docker on VPS](https://github.com/axe-dev/AXE-Bot/blob/master/README.md#docker-installation-on-vps-server).

#### Are you store and know my exchange api keys?

> We do NOT receive and store your api keys, only [hash](https://en.wikipedia.org/wiki/Hash_function) of api key (NOT a secret)!

#### I have another problem

> Make the Issue here
