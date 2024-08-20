import { ref } from 'vue';
import { fetchData } from './api';

export function useFetchData() {
  const data = ref(null);
  const error = ref<Error | null>(null);
  const loading = ref(false);

  const getData = async () => {
    loading.value = true;
    try {
      data.value = await fetchData();
    } catch (err) {
      error.value = err as Error;
    } finally {
      loading.value = false;
    }
  };

  return { data, error, loading, getData };
}