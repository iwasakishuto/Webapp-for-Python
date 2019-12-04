function sendHttpPost(){
  const AWS_url = "http://ec2-AA-BBB-CCC-DDD.ap-northeast-1.compute.amazonaws.com/form"
  var payload = {
    "email" : "<EMAIL>",
    "password": "<PASSWAR>",
    "form_url": "<GOOGLE FORM URL>"
  };
  var options = {
    "method" : "post",
    "payload" : JSON.stringify(payload)
  };
  var response = UrlFetchApp.fetch(AWS_url, options);
  Logger.log(response);
}
