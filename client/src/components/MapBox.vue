<template>
  <v-card class="map-box">
    <v-card-title @click="toggleMap" style="cursor: pointer;">
      World Map <v-icon>{{ isMapVisible ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
    </v-card-title>
    <v-expand-transition>
      <div v-show="isMapVisible" class="map-container">
        <l-map ref="mapRef" :zoom="zoom" :center="center" style="height: 500px; width: 100%;">

          <l-geo-json ref="geoJsonRef" :geojson="countriesData" :options-style="styleCountries"
            :options="geoJsonOptions" @geojson-feature-click="onCountryClicked"
            @geojson-feature-mouseover="onCountryMouseOver" @geojson-feature-mouseout="onCountryMouseOut" />
          <v-btn class="reset-btn" @click="resetMap" title="Reset selected countries">
            <span class="mdi mdi-restore" />
          </v-btn>
        </l-map>

      </div>
    </v-expand-transition>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { LMap, LTileLayer, LGeoJson } from '@vue-leaflet/vue-leaflet';
import { useGameStore } from '../stores/game';
import L, { GeoJSON, LeafletMouseEvent } from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default defineComponent({
  name: 'MapBox',
  components: {
    LMap,
    LTileLayer,
    LGeoJson,
  },
  setup() {
    const gameStore = useGameStore();

    const geoJsonRef = ref<InstanceType<typeof LGeoJson> | null>(null);
    const zoom = ref(2);
    const center = ref<[number, number]>([20, 0]);
    const isMapVisible = ref(true);
    const toggleMap = () => {
      isMapVisible.value = !isMapVisible.value;
    }
    const countriesData = ref<any>(null);

    // Load the countries GeoJSON data
    const loadCountriesData = async () => {
      try {
        const response = await fetch('/countries_50m.geojson');
        countriesData.value = await response.json();
      } catch (error) {
        console.error('Error loading countries data:', error);
      }
    };

    // Style each country
    const styleCountries = (feature: GeoJSON.Feature) => {
      const countryName = feature.properties.SOVEREIGNT; // Adjust property name if needed
      // const isGuessed = gameStore.guessedCountries.includes(countryName);
      const isSelected = gameStore.selectedCountries.includes(countryName.toUpperCase());
      return {
        fillColor: isSelected ? '#cc2222' : '#22222',
        weight: 1,
        opacity: 1,
        color: 'white',
        fillOpacity: 0.7,
      };
    };

    // Handle country click events
    const onCountryClicked = (event: LeafletMouseEvent) => {
      const countryName = event.target.feature.properties.SOVEREIGNT.toUpperCase(); // Adjust property name if needed
      const isSelected = gameStore.handleCountryClick(countryName);

      if (!geoJsonRef.value) return;

      for (const layer of Object.values(geoJsonRef.value.leafletObject._layers)) {
        const l = layer as L.Path & { feature: GeoJSON.Feature };
        if (!l.feature || l.feature.properties.SOVEREIGNT.toUpperCase() !== countryName) continue;
        l.setStyle({
          fillColor: isSelected ? '#cc2222' : '#22222',
        });
      }

    };

    const onCountryMouseOut = (event: LeafletMouseEvent) => {
      const layer = event.target;
      layer.setStyle(styleCountries(layer.feature));
      layer.closeTooltip();
    };

    const onCountryMouseOver = (event: LeafletMouseEvent) => {
      const layer = event.target;
      const sovereigntName = layer.feature.properties.SOVEREIGNT; // Adjust property name if needed
      const countryName = layer.feature.properties.ADMIN; // Adjust property name if needed
      let tooltip = `<b>${countryName}</b>`;
      if (sovereigntName !== countryName) tooltip = `<b>${sovereigntName}</b><br/>${countryName}`
      layer.setStyle({
        weight: 2,
        color: '#666666',
        fillOpacity: 0.7,
      });
      layer.bindTooltip(tooltip).openTooltip();
    };
    const geoJsonOptions = {
      style: styleCountries,
      onEachFeature: (_: any, layer: any) => {
        layer.on({
          click: onCountryClicked,
          mouseover: onCountryMouseOver,
          mouseout: onCountryMouseOut,
        });
      },
    };

    const resetMap = () => {
      gameStore.selectedCountries = [];
      if (!geoJsonRef.value) return;
      
      for (const layer of Object.values(geoJsonRef.value.leafletObject._layers)) {
        const l = layer as L.Path & { feature: GeoJSON.Feature };
        if (!l.feature) continue;
        l.setStyle({
          fillColor: '#22222',
        });
      }
    }

    onMounted(() => {
      loadCountriesData();
    });

    return {
      geoJsonRef,
      zoom,
      center,
      geoJsonOptions,
      countriesData,
      isMapVisible,
      toggleMap,
      styleCountries,
      onCountryClicked,
      onCountryMouseOver,
      onCountryMouseOut,
      resetMap
    };
  },
});
</script>

<style>
@import 'leaflet/dist/leaflet.css';

.map-box {
  height: 100%;
  padding: 20px;
}

.l-map {
  width: 100%;
  height: 100%;
}



*,
*:focus,
*:hover {
  outline: none;
}
</style>

<style>
.reset-btn {
  position: relative;
  padding: 0 !important;
  width: 32px !important;
  height: 32px !important;
  min-width: 10px !important;
  top: 80px;
  left: 11px;
  background-color: white !important;
  color: black !important;
  font-size: 22px !important;
  border: 2px solid rgba(0, 0, 0, 0.3) !important;
  border-radius: 3px !important;
  z-index: 1000;
}
</style>