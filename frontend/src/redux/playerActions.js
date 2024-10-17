export const PLAY_AUDIO = "PLAY_AUDIO";
export const PAUSE_AUDIO = "PAUSE_AUDIO";
export const SET_TRACK = "SET_TRACK";

export const playAudio = () => ({
  type: PLAY_AUDIO,
});

export const pauseAudio = () => ({
  type: PAUSE_AUDIO,
});

export const setTrack = (track) => ({
  type: SET_TRACK,
  payload: track,
});