var awsIot = require('aws-iot-device-sdk');
var sys = require('sys')
var exec = require('child_process').exec;

// Define paramerters to publish a message
var device = awsIot.device({
    keyPath: './certs/private.pem',
    certPath: './certs/cert.pem',
    caPath: './certs/rootca.crt',
    clientId: 'pi_farm_client',
    region: 'ap-northeast-1'
});

// Connect to Message Broker
device.on('connect', function() {
    console.log('Connected to Message Broker.');

    // Loop every 10 sec
    setInterval(function() {

        exec("python /home/pi/pi_farm/collector.py", function (error, stdout, stderr) {
          if (error !== null) {
            console.log('exec error: ' + error);
            return
          }

          datas = stdout.split(",")
          // Compose records
          var record = {
              "deviceid": "pi_01",
              "timestamp": datas[0],
              "hum": datas[1],
              "temp": datas[2],
              "lx": datas[3],
              "moi": datas[4].replace(/[\n\r]/g,"")
          };

          // Serialize record to JSON format and publish a message
          var message = JSON.stringify(record);
          console.log("Publish: " + message);
          device.publish('pi_farm', message);
        });


    }, 10000);
});
