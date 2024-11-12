

async function Start_Server() {
    port_item = document.getElementById("input_port")
    path_item = document.getElementById("input_path")
    
    ip_text = document.querySelector(".ip")

    port = port_item.value
    path = path_item.value

    const response = await eel.Get_Info(port, path)();
    console.log(response)
    ip_text.innerHTML = "Server link: " + response

    await eel.Start_Server();

}

async function Syn() {
    ip_item = document.getElementById("input_link")
    path_item = document.getElementById("input_client_path")
    
    ip = ip_item.value
    path = path_item.value

    
    console.log(path)
    res = await eel.Synchronizate_Fun(ip, path)();
    Add_elements(res["Add elements"], ".client .log .Add_elements")
    Add_elements(res["Remove elements"], ".client .log .Remove_elements")
    Add_elements(res["Change elements"], ".client .log .Change_elements")


}

function Add_elements(el, path){
    var parrent = document.querySelector(path)

    while (parrent.firstChild) {
        parrent.removeChild(parrent.firstChild);
    }
    
    for (i in el){
        console.log(el[i])
        var newDiv = document.createElement('div');
        newDiv.classList.add('Add');
        newDiv.classList.add('contain');

        var file_name = document.createElement('h1')
        var file_wei = document.createElement('h1')

        file_wei.classList.add("wei")
        file_name.innerHTML = el[i][0]

        adder = "Mb"
        size = (el[i][1] / 1000)
        console.log(size)
        if (size > 100){
            size /= 1000
            adder = "Gb"
        }
        file_wei.innerHTML = size.toFixed(2) + adder

        newDiv.appendChild(file_name)
        newDiv.appendChild(file_wei)

        parrent.appendChild(newDiv)
    }

}

function Hide_List(path){
    class_d = document.querySelector(path)
    if (class_d.classList.contains("hide")){
        class_d.classList.remove("hide")

    }
    else{
        class_d.classList.add("hide")
    }
}




type_work = 0

function change_type(type){
    server_button = document.getElementById("server")
    client_button = document.getElementById("client")

    server_class = document.querySelector(".server")
    client_class = document.querySelector(".client")


    server_button.classList.remove('active_button')
    client_button.classList.remove('active_button')

    server_class.classList.add('remove_class')
    client_class.classList.add('remove_class')


    if (type == 0){
        server_button.classList.add('active_button')
        server_class.classList.remove('remove_class')


    }
    if (type == 1){
        client_button.classList.add('active_button')
        client_class.classList.remove('remove_class')

    }

    type_work = type
}




