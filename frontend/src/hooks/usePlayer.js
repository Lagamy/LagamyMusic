import { useSelector, useDispatch } from 'react-redux';
import { setTrack, playAudio, pauseAudio } from '../redux/playerActions';

// custom hook to manage track setting and playback logic
export const usePlayer = () => {
  const currentTrack = useSelector((state) => state.audio.currentTrack);
  const isPlaying = useSelector((state) => state.audio.isPlaying);
  const dispatch = useDispatch();

  

  const handleSetTrack = (soundtrack) => {
    if (currentTrack && currentTrack.id === soundtrack.id) {
        handlePlayPause();
    } else {
        dispatch(setTrack(soundtrack)); // Dispatch play action
    }
  };

  const handlePlayPause = () => {
    if (isPlaying) {
      dispatch(pauseAudio());
    } else {
      dispatch(playAudio());
    }
  };

  return { handleSetTrack, handlePlayPause, currentTrack, isPlaying };
};