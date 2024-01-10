<script setup>
  import { ref, computed, watch } from 'vue'
  import { useSnackbarStore } from '../utils/store';
  

  const snackbarStore = useSnackbarStore();
  const snackbarIsVisible = ref(false);
  const snackbarText = computed(() => snackbarStore.getText);
  const snackbarMessageType = computed(() => snackbarStore.getMessageType);
  const snackbarWasActivated = computed(() => snackbarStore.getWasActivated);
  const snackbarWasClosed = computed(() => snackbarStore.getWasClosed);

  watch(snackbarWasActivated, async (newValue, oldValue) => {
    snackbarIsVisible.value = false;
    
    setTimeout(() => {
        snackbarIsVisible.value = true;
    }, 200);
  });

  watch(snackbarWasClosed, async (newValue, oldValue) => {
    snackbarIsVisible.value = false;
  });
  
  function closeSnackbar(){
    snackbarStore.close();
  }
</script>

<template>
    <v-snackbar
      v-model="snackbarIsVisible"
      :timeout="5000"
      elevation="21"
      >
          <v-alert
          :text="snackbarText"
          :type="snackbarMessageType"
          variant="tonal"
          density="compact"
          ></v-alert>

      <template v-slot:actions>
          <v-btn
          color="blue"
          variant="text"
          @click="closeSnackbar"
          >
          Fechar
          </v-btn>
      </template>
    </v-snackbar>
</template>

<style scoped>
</style>
