import { configureStore } from "@reduxjs/toolkit"
import { playerReducer} from "./playerReducer"

export const playerStore = configureStore({
    reducer: {
      audio: playerReducer,  // I can add more reducers here for other stuff besides the player
    },
    devTools: process.env.NODE_ENV !== 'production', 
  });
  
  export default playerStore;