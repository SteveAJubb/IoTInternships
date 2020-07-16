const mqtt=require('mqtt');

module.exports = class Mqtt {
    constructor(hostname){
        this.hostname = hostname;
    }

    //Connec to mqtt broker
    connect(){
        let mqttClient = mqtt.connect(this.hostname)
        mqttClient.on("connect",function(){	
            console.log("connected");
            //Subscribe to pitch-in topic
            mqttClient.subscribe("pitch-in")
            //On message, console log it
            mqttClient.on('message',function(topic, message, packet){
                console.log("message is "+ message);
                console.log("topic is "+ topic);
            });
        })
        this.mqttClient = mqttClient;
    }
}