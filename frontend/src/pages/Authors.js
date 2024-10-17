import React, { useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import {API_URL, MEDIA_URL} from '../serverConstants'
import axios from 'axios';


function Authors() {
  const [authors, setAuthors] = useState([]); // State to store the authors list
  const [loading, setLoading] = useState(true); // State to track loading
  const [error, setError] = useState(null); // State to track error
  const server = 'http://127.0.0.1:8000'
  // Fetch authors when the component mounts
  useEffect(() => {
    const fetchAuthors = async () => {
      try {
        const response = await axios.get(server + '/api/authors');
        setAuthors(response.data); // Store data in the state
        setLoading(false); // Set loading to false when data is fetched
      } catch (err) {
        setError(err.message); // Handle errors
        setLoading(false); // Stop loading even if there's an error
      }
    };

    fetchAuthors(); // Call the function to fetch authors
  }, []); // Empty dependency array means this runs once when the component mounts

  // Handle loading and error states
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