app = require('express')();
bodyParser = require('body-parser');
request = require('request');
targetListId = process.env.TARGET_LIST_ID;
togglToken = process.env.TOGGL_TOKEN;

var currentId = null;
var currentName = null;
var inExecution = false;

app.use(bodyParser.json());

app.get('/', function(req, res){
  res.status(200).send('Hello World: Get');
});

app.post('/', function(req, res) {
  if(inExecution){
    res.status(200).send('Hello World: Post');
    return;
  }
  manageFlg();
  const display = req.body.action.display;
  if(isStarted(display)) {
    const card = display.entities.card.text;
    start(card);
  } else if (isFinished(display)) {
    finish();
  }
  res.status(200).send('Hello World: Post');
});

app.listen(process.env.PORT || 3000);

function isStarted(display) {
  const key = display.translationKey;
  var listId = "";
  if(key == "action_move_card_from_list_to_list") {
    listId = display.entities.listAfter.id;
  }
  if(key == "action_create_card") {
    listId = display.entities.list.id;
  }
  return listId == targetListId;
}

function isFinished(display) {
  const key = display.translationKey;
  if(key == "action_move_card_from_list_to_list") {
    const listId = display.entities.listBefore.id;
    const card = display.entities.card.text;
    return listId == targetListId && card == currentName;
  }
  if(key == "action_archived_card") {
    const card = display.entities.card.text;
    return card == currentName;
  }
}

function start(name){
  const options = {
    url: 'https://www.toggl.com/api/v8/time_entries/start',
    headers: {'Content-type': 'application/json'},
    auth: {user: togglToken, password: 'api_token'},
    json: {time_entry: {description: name, created_with: "curl"}}
  };
  request.post(options, function(error, response, body){
    if(!error) {
      currentName = name;
      currentId = body.data.id;
    }
  });
}

function finish(){
  if(!currentId) return;
  const options = {
    url: 'https://www.toggl.com/api/v8/time_entries/' + currentId + '/stop',
    method: 'PUT',
    headers: {'Content-type': 'application/json'},
    auth: {user: togglToken, password: 'api_token'},
    json: {}
  };
  request(options, function(error, response, body){
    if(!error) {
      currentName = null;
      currentId = null;
    }
  });
}

function manageFlg(){
  inExecution = true;
  setTimeout(function(){
    inExecution = false;
  }, 500);
}
