function post2AWS(aws_url, email, password, form_url){
  var payload = {
    "email" : email,
    "password": password,
    "form_url": form_url
  };
  var options = {
    "method" : "post",
    "payload" : JSON.stringify(payload)
  };
  var image = UrlFetchApp.fetch(aws_url, options).getBlob();
  return image;
}

function noticeFormURL(incoming_url, form_url, channel_id){
  var payload = {
    "text"     : "form: `" + form_url + "`",
    "channel"  : channel_id,
    "username" : "木村文乃"
  }
  var options = {
    "method" : "POST",
    "contentType" : "application/json",
    "payload" : JSON.stringify(payload)
  };
  var response = UrlFetchApp.fetch(incoming_url, options);
  return response;
}

function postImage(slack_token, image, channel_id){
  var payload = {
    token: slack_token,
    file: image,
    channels: channel_id,
    title: 'image'
  };
  var option={
    'method':'POST',
    'payload': JSON.stringify(payload)
  };
  var res = UrlFetchApp.fetch('https://slack.com/api/files.upload', option);
  return res
}

function doPost(e) {
  const P = PropertiesService.getScriptProperties();

  const slack_token  = P.getProperty('SLACK_ACCESS_TOKEN');
  const outgoing_url = P.getProperty('OUTGOING_WEBHOOKS_TOKEN');
  const incoming_url = P.getProperty('INCOMING_WEBHOOKS_TOKEN');
  const channel_id   = P.getProperty('SLACL_DM_URL');

  const aws_url  = P.getProperty('AWS_URL');
  const email    = P.getProperty('EMAIL');
  const password = P.getProperty('PASSWORD');
  const form_url = e.parameter.text.match(/https:\/\/.*/g)[0].slice(0, -1)// Remove ">"

  var image = post2AWS(aws_url, email, password, form_url);
  var res   = noticeFormURL(incoming_url, form_url, channel_id);
  var res   = postImage(slack_token, image, channel_id); // うまく動作していません。
}
