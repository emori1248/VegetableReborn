var webSocket;

var guildsList;
var textChannelsList;

var selectedGuild;
var selectedTextChannel;

function updateGuilds()
{
    var request = {TYPE:'GETGUILDS'}
    webSocket.send(JSON.stringify(request));
}

function tcsButtonFunc()
{
    var request = {TYPE:'GETTEXT', GUILD:selectedGuild.id}
    webSocket.send(JSON.stringify(request));
}

function vcsButtonFunc()
{
    var request = {TYPE:'GETVOICE', GUILD:'217495235721297920'}
    webSocket.send(JSON.stringify(request));
}

function sendMessageFunc()
{
    var request = {TYPE:'SENDTEXT', CHANNEL:selectedTextChannel.id, MESSAGE:'shut the fuck up'}
    webSocket.send(JSON.stringify(request));
}

function speakMessageFunc() // Bot's TTS in a VC, not built in Discord TTS.
{
    var messageContent = document.getElementById('speakMessageInput').value;
    var request = {TYPE:'SPEAKTEXT', CHANNEL:'217495235721297921', MESSAGE:messageContent}
    webSocket.send(JSON.stringify(request));
}

function writeMessageFunc()
{
    var messageContent = document.getElementById('writeMessageInput').value;
    var request = {TYPE:'SENDTEXT', CHANNEL:selectedTextChannel.id, MESSAGE:messageContent}
    webSocket.send(JSON.stringify(request));
}

function stopSoundsFunc()
{
    var request = {TYPE:'STOPSOUNDS', GUILD:selectedGuild.id};
    webSocket.send(JSON.stringify(request));
}

function onGuildChange()
{
    // update selected guild
    var e = document.getElementById("guildsDropdown");
    var selectedStr = e.options[e.selectedIndex].text;
    for(var i = 0; i < guildsList.length; i++) {
        if(guildsList[i].displayName == selectedStr){
            selectedGuild = guildsList[i];
            console.log(selectedGuild.id);
        }
    }
    // repopulate text channels list
    tcsButtonFunc();
}

function onTextChannelChange()
{
    var e = document.getElementById("tcsDropdown");
    var selectedStr = e.options[e.selectedIndex].text;
    for(var i = 0; i < textChannelsList.length; i++) {
        if(textChannelsList[i].displayName == selectedStr){
            selectedTextChannel = textChannelsList[i];
            console.log(selectedTextChannel.id);
        }
    }
}

function onSpeakForm()
{
    document.getElementById("speakMessageInput").focus();
}

function loadFunc()
{
    var url = "ws://localhost:8080/botWS"
    
    webSocket = new WebSocket(url);

    webSocket.onopen = function (event) {
        console.log("opened");
        // get guilds list, populate dropdown
        updateGuilds();
        //tcsButtonFunc();
        
    };

    webSocket.onmessage = function (event) {
        console.log(event.data);
        var obj = JSON.parse(event.data)
        if("guilds" in obj.response){
            guildsList = obj.response.guilds;
            populateGuildsDropdown(guildsList);
            selectedGuild = guildsList[0];
            tcsButtonFunc();
        }
        if("textChannels" in obj.response){
            textChannelsList = obj.response.textChannels;
            populateTextChannelsDropdown(textChannelsList);
            selectedTextChannel = textChannelsList[0];
        }

    }

    webSocket.onerror = function (event) {
        document.getElementById("subheader").innerHTML += " (Bot is down)"
    }


}

function populateGuildsDropdown(guilds)
{
    var dropdown = document.getElementById("guildsDropdown");
    dropdown.innerHTML = null;
    for(var i = 0; i < guilds.length; i++){
        var option = document.createElement("option");
        option.text = guilds[i].displayName;
        dropdown.add(option);
    }

    
}

function populateTextChannelsDropdown(tcs)
{
    var dropdown = document.getElementById("tcsDropdown");
    dropdown.innerHTML = null;
    for(var i = 0; i < tcs.length; i++){
        var option = document.createElement("option");
        option.text = tcs[i].displayName;
        dropdown.add(option);
    }
}

