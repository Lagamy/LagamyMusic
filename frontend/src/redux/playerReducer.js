import { PLAY_AUDIO, PAUSE_AUDIO, SET_TRACK } from "./playerActions";

const initialState = {
  isPlaying: false,
  currentTrack: null,
};


export const playerReducer = (state = initialState, action) => {
    switch (action.type) {
      case PLAY_AUDIO:
        return { ...state, isPlaying: true }; // ... - creates shallow copies to make state immutable
      case PAUSE_AUDIO:
        return { ...state, isPlaying: false };
      case SET_TRACK:
        // console.log(action.payload)
        return { ...state, currentTrack: action.payload, isPlaying: true };
      default:
        return state;
    }
};