import React, { useState, useEffect, useContext} from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import {API_URL, MEDIA_URL} from '../serverConstants'
import { Button, Typography } from '@mui/material';
import { UserContext } from '../state_managment/userContext'
import { usePlayer } from '../hooks/usePlayer';  // import custom hook

function Author() {
  const { artistId } = useParams();
  // const frozenArtistId = Object.freeze(artistId); // artistId is not Object, ergo when using const its immutable by default
  const [author, setAuthor] = useState([]); 
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { userState } = useContext(UserContext);

  const { handleSetTrack } = usePlayer();

  useEffect(() => {
    const fetchAuthor = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/${artistId}`, { withCredentials: true });
        setAuthor(response.data); 
        setLoading(false); 
      } catch (err) {
        setError(err.message); 
        setLoading(false); 
      }
    };

    fetchAuthor();
  }, []); 

  // Handle loading and error states
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;


  let singles;
  let albums;

  if (author.singles && author.albums.length !== 0) {
    albums = (
      <div> 
      <h1>Albums:</h1>
      {author.albums.map((album) => (
         <div key={album.id}>
        {album.name}
        <img src={MEDIA_URL + album.image}/>
        {userState && userState.id === artistId? (
          <Typography>Can edit</Typography>
        )
        : (
          <Typography></Typography>
        )}
        </div>
      ))}
      </div>
    )
  }

  if (author.albums && author.albums.length !== 0) {
    singles = (
        <div> 
        <h1>Singles:</h1>
        {author.singles.map((single) => (
           <div key={single.id}>
          {single.name}
          <img src={MEDIA_URL + single.image}/>
          <Button onClick={() => handleSetTrack(single)}> Play </Button>
          {/* <audio controls src={MEDIA_URL + single.audiotrack}></audio> */}
          {userState && userState.id === artistId? (
            <Typography>Can edit</Typography>
          )
          : (
            <Typography></Typography>
          )}
          </div>
        ))}
        </div>
      )
    }


  return (

    <div>
      <ul>
          <div>
            
            {author.username}
            <img src={MEDIA_URL + author.image}/>
            {singles}
            {albums}
          </div>
      </ul>
    </div>
  )
}

export default Author