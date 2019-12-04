# GAS(GoogleForm Answering SlackBot)
It is tiresome to repeat the same things in the daily life. One of them is replying the routine questioners, so I made an application to do it automatically!!

## Architecture
![Overview](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/308700/84f72447-f31f-f4ef-f992-0e8c35ffefff.png)

|Name|Explanation|
|:--|:--|
|[Google Forms](https://www.google.com/forms/about/)|Free Online Surveys for Personal Use.|
|[Slack](https://slack.com/)|Where work happens.|
|[Outgoing Webhooks](https://api.slack.com/custom-integrations/outgoing-webhooks)|Legacy method of sending notifications to an app about two specific activities.|
|[Google Apps Script](https://developers.google.com/apps-script)|Makes it easy to create and publish add-ons in an online store for Google Sheets, Docs, Slides, and Forms.|
|[Amazon EC2](https://aws.amazon.com/ec2/)|Web service that provides secure, resizable compute capacity in the cloud.|
|[Flask](http://flask.palletsprojects.com)|Lightweight WSGI web application framework.|

## [日本語版解説記事](https://qiita.com/cabernet_rock/items/1e2aa3ba48328025d0d8)

## Results
|Google Form posted to Slack|Answering Automatically|Notice to DM|
|:-:|:-:|:-:|
|![form.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/308700/e73ae3d7-b1f4-393b-5751-0a214bb537b9.png)|![form result.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/308700/39ea91ed-7946-0fcb-bccc-29bd063ba3d1.png)|![slack.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/308700/87733825-5d2b-0613-5cef-0ea675097dd1.png)|

## References
- [【Googleログイン自動化】Python×seleniumでGoogleにログインする](https://qiita.com/spark55/items/144c6cb7a7444f804564)
- [EC2 UbuntuでGoogle Chromeをヘッドレス実行してスクリーンショットを採取する手順](https://qiita.com/shinsaka/items/37436e256c813d277d6d)
- [PythonかければWebアプリぐらい作れる。](https://qiita.com/cabernet_rock/items/852fc7c5d382fdc422a3)
- [Slack BotをGASでいい感じで書くためのライブラリを作った](https://qiita.com/soundTricker/items/43267609a870fc9c7453)
- [Slack上のメッセージをGoogleAppsScriptで受け取ってよしなに使う](https://qiita.com/kyo_nanba/items/83b646357d592eb9a87b)
- [SlackのOutgoing WebHooksとGoogleAppsScriptで簡単な会話botを作ってみた](https://qiita.com/pistaman/items/a542119ea28871960477)
