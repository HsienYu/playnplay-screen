const { Server, Client, Message } = require('node-osc');
const { PythonShell } = require('python-shell');
const axios = require('axios')

const oscServer = new Server(3333, '0.0.0.0');


let pyshell = new PythonShell('./main.py');
let msg_arr = [];
let profile_arr_a = [];
let profile_arr_b = [];
let profile_arr_c = [];

function printer_a_request() {
    axios
        .get('http://192.168.168.87:8090/print')
        .then(res => {
            console.log(res.data)
            update_profile_a(res.data)
        })
        .catch(err => {
            console.log(err)
        })
}

function printer_b_request() {
    axios
        .get('http://192.168.168.91:8090/print')
        .then(res => {
            console.log(res.data)
            update_profile_b(res.data)
        })
        .catch(err => {
            console.log(err)
        })
}

function printer_c_request() {
    axios
        .get('http://192.168.168.92:8090/print')
        .then(res => {
            console.log(res.data)
            update_profile_c(res.data)
        })
        .catch(err => {
            console.log(err)
        })
}

function update_profile_a(data) {
    profile_arr_a.push(data);
    console.log(profile_arr_a);
    if (profile_arr_a.length > 1) {
        profile_arr_a.shift();
    }
}

function update_profile_b(data) {
    profile_arr_b.push(data);
    console.log(profile_arr_b);
    if (profile_arr_b.length > 1) {
        profile_arr_b.shift();
    }
}
function update_profile_c(data) {
    profile_arr_c.push(data);
    console.log(profile_arr_c);
    if (profile_arr_c.length > 1) {
        profile_arr_c.shift();
    }
}

function update_msg(msg) {
    msg_arr.push(msg);
    //console.log(msg_arr);
    if (msg_arr.length > 15) {
        msg_arr.shift();
    }
    document.getElementsByClassName('msg1')[0].innerHTML = msg_arr[0];
    document.getElementsByClassName('msg2')[0].innerHTML = msg_arr[1];
    document.getElementsByClassName('msg3')[0].innerHTML = msg_arr[2];
    document.getElementsByClassName('msg4')[0].innerHTML = msg_arr[3];
    document.getElementsByClassName('msg5')[0].innerHTML = msg_arr[4];
    document.getElementsByClassName('msg6')[0].innerHTML = msg_arr[5];
    document.getElementsByClassName('msg7')[0].innerHTML = msg_arr[6];
    document.getElementsByClassName('msg8')[0].innerHTML = msg_arr[7];
    document.getElementsByClassName('msg9')[0].innerHTML = msg_arr[8];
    document.getElementsByClassName('msg10')[0].innerHTML = msg_arr[9];
    document.getElementsByClassName('msg11')[0].innerHTML = msg_arr[10];
    document.getElementsByClassName('msg12')[0].innerHTML = msg_arr[11];
    document.getElementsByClassName('msg13')[0].innerHTML = msg_arr[12];
    document.getElementsByClassName('msg14')[0].innerHTML = msg_arr[13];
    document.getElementsByClassName('msg15')[0].innerHTML = msg_arr[14];
}


function update_ui_a() {
    let file_path_a = profile_arr_a[0].file_path;
    let temp_arr_a = file_path_a.split('/');
    let final_path_a = 'view' + '/' + temp_arr_a[4] + '/' + temp_arr_a[5];
    document.getElementsByClassName('pic_a')[0].innerHTML = `<img width="100" height="100" src=${final_path_a}>`;
    document.getElementsByClassName('ip_address_a')[0].innerHTML = profile_arr_a[0].ip_address;
    document.getElementsByClassName('name_a')[0].innerHTML = profile_arr_a[0].name;
    document.getElementsByClassName('phone_a')[0].innerHTML = profile_arr_a[0].phone;
    document.getElementsByClassName('email_a')[0].innerHTML = profile_arr_a[0].email;
}

function update_ui_b() {
    let file_path_b = profile_arr_b[0].file_path;
    let temp_arr_b = file_path_b.split('/');
    let final_path_b = 'view' + '/' + temp_arr_b[4] + '/' + temp_arr_b[5];
    document.getElementsByClassName('pic_b')[0].innerHTML = `<img width="100" height="100" src=${final_path_b}>`;
    document.getElementsByClassName('ip_address_b')[0].innerHTML = profile_arr_b[0].ip_address;
    document.getElementsByClassName('name_b')[0].innerHTML = profile_arr_b[0].name;
    document.getElementsByClassName('phone_b')[0].innerHTML = profile_arr_b[0].phone;
    document.getElementsByClassName('email_b')[0].innerHTML = profile_arr_b[0].email;
}

function update_ui_c() {
    let file_path_c = profile_arr_c[0].file_path;
    let temp_arr_c = file_path_c.split('/');
    let final_path_c = 'view' + '/' + temp_arr_c[4] + '/' + temp_arr_c[5];
    document.getElementsByClassName('pic_c')[0].innerHTML = `<img width="100" height="100" src=${final_path_c}>`;
    document.getElementsByClassName('ip_address_c')[0].innerHTML = profile_arr_c[0].ip_address;
    document.getElementsByClassName('name_c')[0].innerHTML = profile_arr_c[0].name;
    document.getElementsByClassName('phone_c')[0].innerHTML = profile_arr_c[0].phone;
    document.getElementsByClassName('email_c')[0].innerHTML = profile_arr_c[0].email;
}

oscServer.on('message', function (msg) {
    console.log(`Message: ${msg}`);
    if (msg == '/printer_a') {
        printer_a_request();
        update_ui_a();
    }
    if (msg == '/printer_b') {
        printer_b_request();
        update_ui_b();
    }
    if (msg == '/printer_c') {
        printer_c_request();
        update_ui_c();
    }
});

pyshell.on('message', function (message) {
    console.log(message);
    update_msg(message);
});
