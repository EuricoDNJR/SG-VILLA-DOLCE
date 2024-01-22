<script setup>
  import { ref, computed, watch, onMounted, reactive, toRef,  onBeforeUnmount } from 'vue'
  import { fetchGet, fetchPost, fetchPatch, confirmDialog, getFormatedDate } from '../utils/common';
  import { useAuthStore, useSnackbarStore, useCaixaStore, usePedidoStore } from '../utils/store';

  const props = defineProps(['pedido', 'saldoCliente']);
  console.log(props);
  const snackbarStore = useSnackbarStore();

  const pedido = computed(() => props.pedido);

  const qtdDescontosAplicadosGeral = computed(() => {
    return props.pedido.reduce((somatorio, produto) => {
      if(produto.id == -1){
        return somatorio;
      }
      return somatorio + Math.ceil(Number(produto.desconto) / 15);
    }, 0);
  });

  const saldoRetorna = computed(() => {
    return props.pedido.reduce((somatorio, produto) => {
      const qtdDescontos = Math.ceil(Number(produto.desconto)/15);

      return somatorio + (qtdDescontos*15) - Number(produto.desconto);
    }, 0);
  });

  const desconto = reactive({
    item: pedido.value[0],
    status: computed(() => Number(desconto.item.desconto) > 0 ? "Remover" : "Aplicar"),
    color: computed(() => Number(desconto.item.desconto) > 0 ? "grey-darken-3" : "deep-purple"),
    // qtdDescontosAplicados: computed({
    //   get(){
    //     return Math.ceil(Number(desconto.item.desconto)/15);
    //   },
    //   set(qtdDescontos){
    //     if(desconto.item.id != -1){
    //         const valorTotal = Number(desconto.item.quantidade) * Number(desconto.item.valorVendaUnd);

    //         desconto.item.desconto = "0.00";

    //         qtdDescontos = Math.min(qtdDescontos, desconto.descontosRestantes);
    //         qtdDescontos = Math.max(0, qtdDescontos);
            
    //         desconto.item.desconto = Math.min(qtdDescontos*15, valorTotal).toFixed(2);
    //     }else{
    //       snackbarStore.set("Por enquanto não é possivel aplicar descontos em itens adicionados anteriormente", 'warning');
    //     }
    //   }
    // }),
    saldoCliente: computed(() => props.saldoCliente - (150*qtdDescontosAplicadosGeral.value) + saldoRetorna.value),
    descontosRestantes: computed(() => Math.floor(Number(desconto.saldoCliente)/150)),
    valorTotalItem: computed(() => (Number(desconto.item.quantidade) * Number(desconto.item.valorVendaUnd) - Number(desconto.item.desconto)).toFixed(2)),
  });
  
  const dialogIsVisible = reactive({
    desconto: false,
  });
  

  function closeDialog(nome){
    dialogIsVisible[nome] = false;

    if(nome == "desconto"){
      pedido.value.forEach((produto) => {
        if(produto.id != -1){
          produto.desconto = "0.00";
        }
      });
    }
  }

  function saveDiscount(){
    dialogIsVisible["desconto"] = false;
  }

  function applyDiscount(){
    if(desconto.item.id != -1){
      if(desconto.status == "Aplicar"){
        const valorTotal = Number(desconto.item.quantidade) * Number(desconto.item.valorVendaUnd);
        const valorDesconto = 15;
      
        desconto.item.desconto = "0.00";

        if(desconto.descontosRestantes > 0){
          desconto.item.desconto = Math.min(valorDesconto, valorTotal).toFixed(2);

        }else{
          snackbarStore.set("O cliente não possui descontos", 'warning');
        }
      }else if(desconto.status == "Remover"){
        desconto.item.desconto = "0.00";
      }
    }else{
      snackbarStore.set("Por enquanto não é possivel aplicar ou remover descontos em itens adicionados anteriormente", 'warning');
    }
  }

  function discountItemProps(item){
    return {
      title: item.nome,
      subtitle: `${item.quantidade.replace('.', ',')} x ${item.valorVendaUnd.replace('.', ',')}`
    };
  }

</script>

<template>
  <v-dialog id=descontos 
    v-model="dialogIsVisible.desconto"
    persistent
    width="512"
  > 
    <template v-slot:activator="{ props }">
      <v-btn
        block
        color="deep-purple"
        prepend-icon="mdi-sale"
        :disabled="Number(props.saldoCliente)/150 <= 0"
        v-bind="props"
      >
        Descontos ({{ Math.floor(desconto.saldoCliente/150) }})
      </v-btn>
    </template>

    <v-card>
      <v-card-title>
          <span class="text-h5">Descontos</span>
      </v-card-title>

      <v-divider></v-divider>

      <v-card-text>
        <v-container>
          <v-row>
            <v-col>
              <v-select
                v-model="desconto.item"
                label="Itens do Pedido"
                hide-details="auto"
                density="comfortable"
                :items="pedido"
                :item-props="discountItemProps"
                :hint="`${desconto.item.quantidade.replace('.', ',')} x ${desconto.item.valorVendaUnd.replace('.', ',')}`"
                persistent-hint
                return-object
              ></v-select>
            </v-col>

            <v-col>
              <v-text-field
                v-model.number="desconto.valorTotalItem"
                label="Valor do Item"
                type="number"
                hide-details="auto"
                :readonly="true"
                density="comfortable"
              ></v-text-field>
            </v-col>
            
          </v-row>
          <v-row>
            <v-col>
              <!-- <v-text-field
                v-model.number="desconto.qtdDescontosAplicados"
                label="Quantidade de Descontos Aplicados no Item"
                type="number"
                hide-details="auto"
                density="comfortable"
              ></v-text-field> -->
              <v-btn
                block
                :color="desconto.color"
                prepend-icon="mdi-sale"
                @click="applyDiscount"
              >
                {{ desconto.status }} Desconto
              </v-btn>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-text-field
                v-model.number="desconto.descontosRestantes"
                label="Quantidade de Descontos Restantes"
                type="number"
                hide-details="auto"
                :readonly="true"
                density="comfortable"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>

      <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn   
              variant="text"
              @click="() => closeDialog('desconto')"
          >
              Resetar
          </v-btn>
          <v-btn   
              variant="text"
              color="green-darken-1"
              @click="() => saveDiscount()"
          >
              Salvar
          </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped>
</style>