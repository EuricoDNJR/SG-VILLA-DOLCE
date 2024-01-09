import { ref } from 'vue'
import { useCargosStore } from './store';

function searchByTitle(atributos, title){
    const atributosFlat = atributos.flat(Infinity);
    const atributo = atributosFlat.find((obj) => obj.title.toLowerCase() == title);

    return atributo;
}

export function isValidColaborador(atributos, pessoa){
    const nomeError = searchByTitle(atributos, "nome", false).error;
    const senhaError = searchByTitle(atributos, "senha", false).error;
    const telefoneError = searchByTitle(atributos, "telefone", false).error;
    const emailError = searchByTitle(atributos, "email", false).error;
    const cpfError = searchByTitle(atributos, "cpf", false).error;
    const dataNascimentoError = searchByTitle(atributos, "data de nascimento", false).error;
    const enderecoError = searchByTitle(atributos, "endereço", false).error;

    nomeError.value = (pessoa.nome.length <= 0);
    senhaError.value = (pessoa.senha.length <= 0);
    telefoneError.value = (pessoa.telefone.length <= 0);
    emailError.value = (pessoa.email.length <= 0);
    cpfError.value = (pessoa.cpf.length <= 0);
    dataNascimentoError.value = (pessoa.dataNascimento.length <= 0);
    enderecoError.value = (pessoa.endereco.length <= 0);

    const isValid = !(nomeError.value || 
                    senhaError.value ||
                    telefoneError.value ||
                    emailError.value ||
                    cpfError.value  ||
                    dataNascimentoError.value ||
                    enderecoError.value);

    return isValid;
}

export function createColaborador(atributos){
    const pessoa = {
        nome: searchByTitle(atributos, "nome").obj.value, 
        senha: searchByTitle(atributos, "senha").obj.value, 
        telefone: searchByTitle(atributos, "telefone").obj.value, 
        email: searchByTitle(atributos, "email").obj.value, 
        cpf: searchByTitle(atributos, "cpf").obj.value, 
        dataNascimento: searchByTitle(atributos, "data de nascimento").obj.value,
        endereco: searchByTitle(atributos, "endereço").obj.value,
        cargo: searchByTitle(atributos, "cargo").obj.value,
    };

    return pessoa;
}

export function createAtributosColaborador(){
    const atributos = [];
    const titulosArrays = [
        ["Nome", "Senha"],
        ["Telefone", "Email"],
        ["CPF",  "Data de Nascimento"],
        ["Endereço", "Cargo"],
    ];
    const cargoStore = useCargosStore();
    
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
    
    const dataNascimento = searchByTitle(atributos, "data de nascimento");
    dataNascimento.type = "date";

    const cargo = searchByTitle(atributos, "cargo");
    cargo.obj.value = cargoStore.getCargos[0];
    cargo.type = "select";
    cargo.items = cargoStore.getCargos;

    return atributos;
    
}