import React, { useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import {API_URL, MEDIA_URL} from '../serverConstants'
import axios from 'axios';


function Authors() {
  const [authors, setAuthors] = useState([]); // State to store the authors list
  const [loading, setLoading] = useState(true); // State to track loading
  const [error, setError] = useState(null); // State to track error
 
  const fetchAuthors = async () => {
    try {
      const response = await axios.get(API_URL + '/api/authors');
      setAuthors(response.data);
      setLoading(false); 
    } catch (err) {
      setError(err.message);
      setLoading(false); 
    }
  };

  useEffect(() => {
    fetchAuthors();
  }, []); // Empty dependency array means this runs once when the component mounts


  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  return (

    <div>
      Authors
      <div>
        {authors.map((author) => (
          <div key={author.id}>
            <Link to={`/${author.id}`}>
                {author.username}
                <img src={MEDIA_URL + author.image} alt={author.username} />
            </Link>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Authors