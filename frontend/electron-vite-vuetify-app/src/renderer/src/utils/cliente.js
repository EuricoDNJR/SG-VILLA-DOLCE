import { ref } from 'vue'

function searchByTitle(atributos, title){
    const atributosFlat = atributos.flat(Infinity);
    const atributo = atributosFlat.find((obj) => obj.title.toLowerCase() == title);

    return atributo;
}

export function isValidCliente(atributos, pessoa){

    const nomeError = searchByTitle(atributos, "nome").error;
    const telefoneError = searchByTitle(atributos, "telefone").error;

    nomeError.value = (pessoa.nome.length <= 0);
    telefoneError.value = (pessoa.telefone.length <= 0);

    const isValid = !(nomeError.value || telefoneError.value);

    return isValid;
}

export function createCliente(atributos){
    const pessoa = {
        nome: searchByTitle(atributos, "nome").obj.value, 
        telefone: searchByTitle(atributos, "telefone").obj.value, 
        email: searchByTitle(atributos, "email").obj.value, 
        cpf: searchByTitle(atributos, "cpf").obj.value, 
        dataNascimento: searchByTitle(atributos, "data de nascimento").obj.value,
        endereco: searchByTitle(atributos, "endereço").obj.value,
        saldo: 0,
    };

    return pessoa;
}

export function createAtributosCliente(){
    const atributos = [];
    const titulosArrays = [
        ["Nome", "Telefone"],
        ["Email", "CPF"],
        ["Data de Nascimento", "Endereço"],
    ];
    
    for(let i=0; i < titulosArrays.length; i++){
        atributos.push([]);
        
        for(let j=0; j < titulosArrays[i].length; j++){
            atributos[i].push({
                title: titulosArrays[i][j],
                obj: ref(''),
                type: "text",
                error: ref(false),
            });
        }
    }
    
    searchByTitle(atributos, "data de nascimento").type = "date";

    return atributos;
    
}