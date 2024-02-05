<script setup>
  import { ref, computed, reactive, onMounted } from 'vue'
  import { fetchGet, getAuthToken, setMessageSnackbar, getFormatedDatetime } from '../utils/common';
  import Snackbar from '../components/Snackbar.vue';

  defineOptions({
    inheritAttrs: false
  });

  const caixas = ref([]);
  const calculatedRows = computed(() => {
    const matrix = [[]];

    const limiteCaixasPorLinha = 3;
    let qtdDeCaixasNessaLinha = 0;
    let indiceDaLinhaAtual = 0;

    caixas.value.forEach((caixa) => {
      matrix[indiceDaLinhaAtual].push(caixa);

      qtdDeCaixasNessaLinha += 1;
      if(qtdDeCaixasNessaLinha == limiteCaixasPorLinha){
        matrix.push([]);
        qtdDeCaixasNessaLinha = 0;
        indiceDaLinhaAtual += 1;
      }
    });

    return matrix;
  });

  async function requestAllCaixas(){
    try{
      const url = "http://127.0.0.1:8000/v1/caixa/get_all_caixa/";
      const token = getAuthToken();
      
      const response = await fetchGet(url, token);

      if(response.status != 204){
        const responseJson = await response.json();

        if(response.status === 200){
          caixas.value = responseJson;
          console.log(responseJson);
        }else{
          setMessageSnackbar(responseJson.message, 'warning');
        }
      }
    }catch(e){
      console.log(e);
      setMessageSnackbar("Falha ao carregar caixas", 'warning');
    }
  }

  onMounted(() => {
    requestAllCaixas();
  });
</script>

<template>
  <Snackbar/>    
  
  <v-app-bar  color="deep-purple" :elevation="2" density="compact">
    <v-app-bar-title>Caixas</v-app-bar-title>

    <template v-slot:prepend>
      <v-icon>mdi-menu-right</v-icon>
    </template>
  </v-app-bar>

  <div class="pa-4">
    <v-row v-for="(rowCaixas, rowIndex) in calculatedRows" :key="rowIndex">
      <v-col
        v-for="caixa in rowCaixas"
        :key="caixa.idCaixa"
        cols="12"
        sm="6"
        md="4"
      >
        <v-card
          class="mb-4 border-start-card"
          @click="() => toEditarPedido(pedido)"
        >
        <v-card-item>
          <v-card-title><span class="text-green">R$ {{ caixa.SaldoFinal.replace('.', ',') }}</span> de vendas</v-card-title>

          <v-card-subtitle>
            <span class="me-1">Status: {{ caixa.aberto ? "Aberto" : "Fechado" }}</span>

           
          </v-card-subtitle>
        </v-card-item>

        <v-card-text class="py-2">
          <v-chip color="blue" class="mb-1">
            <p>
              <strong>{{ caixa.nomeUsuarioAbertura }}</strong> abriu o caixa
            </p>
          </v-chip>

          <v-chip color="green">
            <p>
              <strong>{{ caixa.nomeUsuarioAbertura }}</strong> fechou o caixa
            </p>
          </v-chip>

          <p class="mt-6">
            Caixa fechado em {{ getFormatedDatetime(caixa.dataFechamento) }}
          </p>
        </v-card-text>
         
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<style scoped>
.border-start-card {
  border-left: 4px solid #18b49f; /* Cor e largura da borda */
}
</style>