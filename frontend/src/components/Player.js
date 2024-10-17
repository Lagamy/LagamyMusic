import React, {useRef, useEffect} from 'react'
import { MEDIA_URL} from '../serverConstants'
import { useSelector } from 'react-redux'
import { usePlayer } from '../hooks/usePlayer'
import { AppBar, Typography } from '@mui/material'
import { PlayerBar } from '../theme'

const Player = () => {
  const audioRef = useRef(null); // reference to the audio element
  const {handlePlayPause} = usePlayer();
  const isPlaying = useSelector((state) => state.audio.isPlaying);
  const currentTrack = useSelector((state) => state.audio.currentTrack);

   // handle "play or pause" when isPlaying changes in audio html component 
   useEffect(() => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.play().catch((e) => {
          console.error('Error while trying to play audio:', e);
        });
      } else {
        audioRef.current.pause();
      }
    }
  }, [isPlaying]);

  const handleVolumeChange = (e) => {
    const newVolume = e.target.value;
    if (audioRef.current) {
      audioRef.current.volume = newVolume; 
    }
  };

  // handle track change and reset audio before setting new src
  useEffect(() => {
    if (audioRef.current && currentTrack) {
      audioRef.current.pause(); 
      audioRef.current.currentTime = 0;
      audioRef.current.src = MEDIA_URL + currentTrack.audiotrack;
      audioRef.current.load(); // load new track before playing
      audioRef.current.play().catch((e) => {
        console.error('Error while trying to play new audio track:', e);
      });
    }
  }, [currentTrack]);

  


  return (
    <div  style={{ display: 'flex', flexDirection: 'column', minHeight: '90vh' }}>
  
      <AppBar
        position="fixed"
        sx={{
          display: currentTrack ? 'flex' : 'none',
          top: 'auto',
          bottom: 2,   
          boxShadow: 0,
          alignItems: 'center',
          bgcolor: 'transparent',
          backgroundImage: 'none',
        }}
      >
        <PlayerBar>
          {currentTrack ? (
            <div>
              <button onClick={handlePlayPause}>
                {isPlaying ? 'Pause' : 'Play' /* text of button */} 
              </button>
              <input class="volum-slider" type="range" min="0" max="1" step="any" onChange={handleVolumeChange}/>
              <audio ref={audioRef} controls style={{display: 'none'}}/>
            </div>
          ) : (
            <Typography> Choose Any Soundtrack </Typography>
          )}
        </PlayerBar>
      </AppBar>
    </div>
  );
}

export default Player