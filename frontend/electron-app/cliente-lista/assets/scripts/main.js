async function loadData(){
    const response = await fetch("http://127.0.0.1:8000/v1/cliente/get_all_clients/");
    const responseJson = await response.json();

    console.log(responseJson);
}

loadData();