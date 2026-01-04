export const fetchers = {
    /** @return {Promise<RealbotApi.GetStatsResponse>} */
    stats: () => fetch("/stats").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetMapResponse>} */
    map: () => fetch("/map").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetMapEncountersResponse>} */
    mapEncounters: () => fetch("/map_encounters").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetShinyLogResponse>} */
    shinyLog: () => fetch("/shiny_log").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetEncounterLogResponse>} */
    encounterLog: () => fetch("/encounter_log").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetPlayerAvatarResponse>} */
    playerAvatar: () => fetch("/player_avatar").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetPartyResponse>} */
    party: () => fetch("/party").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetEmulatorResponse>} */
    emulator: () => fetch("/emulator").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetEventFlagsResponse>} */
    eventFlags: () => fetch("/event_flags").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetEncounterRateResponse>} */
    encounterRate: () => fetch("/encounter_rate").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetGameStateResponse>} */
    gameState: () => fetch("/game_state").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetPokemonStorageResponse>} */
    pokemonStorage: () => fetch("/pokemon_storage").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetPokemonStorageSizeResponse>} */
    pokemonStorageSize: () => fetch("/pokemon_storage?format=size-only").then(response => response.json()),

    /** @return {Promise<RealbotApi.GetDaycareResponse>} */
    daycare: () => fetch("/daycare").then(response => response.json()),

    /** @return {Promise<object>} */
    customState: () => fetch("/custom_state").then(response => response.json()),
};

/**
 * @param {OverlayState} state
 * @return {Promise<object>}
 */
export function loadAllData(state) {
    return new Promise((resolve, reject) => {
            Promise.all([
                fetchers.stats(),
                fetchers.map(),
                fetchers.mapEncounters(),
                fetchers.shinyLog(),
                fetchers.encounterLog(),
                fetchers.playerAvatar(),
                fetchers.party(),
                fetchers.emulator(),
                fetchers.eventFlags(),
                fetchers.encounterRate(),
                fetchers.gameState(),
                fetchers.pokemonStorage(),
                fetchers.daycare(),
                fetchers.customState(),
            ]).then(
                data => {
                    state.stats = data[0];
                    state.map = data[1];
                    state.mapEncounters = data[2];
                    state.shinyLog = data[3];
                    state.encounterLog = data[4];
                    state.playerAvatar = data[5];
                    state.party = data[6];
                    state.emulator = data[7];
                    state.eventFlags = data[8];
                    state.encounterRate = data[9].encounter_rate;
                    state.gameState = data[10];
                    state.pokemonStorage = data[11];
                    state.daycare = data[12];
                    state.reset();
                    resolve(data[13]);
                },
                reject);
        }
    );
}

/**
 * @param {{[k: string]: (MessageEvent) => any}} listeners
 * @return {EventSource}
 * */
export function getEventSource(listeners) {
    const url = new URL(window.location.origin + "/stream_events");
    url.searchParams.append("topic", "PerformanceData");
    url.searchParams.append("topic", "BotMode");
    url.searchParams.append("topic", "GameState");
    url.searchParams.append("topic", "Party");
    url.searchParams.append("topic", "WildEncounter");
    url.searchParams.append("topic", "Map");
    url.searchParams.append("topic", "MapEncounters");
    url.searchParams.append("topic", "Player");
    url.searchParams.append("topic", "PlayerAvatar");
    url.searchParams.append("topic", "Inputs");
    url.searchParams.append("topic", "PokenavCall");
    url.searchParams.append("topic", "FishingAttempt");
    url.searchParams.append("topic", "CustomEvent");
    const eventSource = new EventSource(url);

    for (const [eventName, eventHandler] of Object.entries(listeners)) {
        eventSource.addEventListener(eventName, eventHandler);
    }

    return eventSource;
}
