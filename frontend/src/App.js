import Header from './components/Header';
import Player from './components/Player';
import Home from './pages/Home'
import Authors from './pages/Authors'
import Author from './pages/Author'
import Genres from './pages/Genres'
import Login from './pages/Login'
import Register from './pages/Register'
import './styles/App.css';
import { Routes, Route } from 'react-router-dom';
import { Theme } from "./theme"
import { ThemeProvider } from 'styled-components';
import { UserProvider } from './state_managment/userContext'
import { Provider } from 'react-redux'; // Import Provider from react-redux
import store from './redux/playerStore';      // Import your Redux store


function App() {

  
  return (
    <Provider store={store}>
    <UserProvider>
      <ThemeProvider theme={Theme}>
      <div className="App">
      {/* <Button color="primary">
      Test Button
      </Button> */}
        <Header />
        <div style={{ marginTop: '140px' }}>
        <Routes>
          <Route path="/" element={<Home/>}></Route>
          <Route path="/login" element={<Login/>}></Route>
          <Route path="/register" element={<Register/>}></Route>
          <Route path="/genres" element={<Genres/>}></Route>
          <Route path="/artists" element={<Authors/>}></Route>  
          <Route path="/:artistId" element={<Author/>}> </Route>
        </Routes>
        </div>
          {/* <img src={logo} className="App-logo" alt="logo" /> */}
        <Player />
      </div>
      </ThemeProvider>
    </UserProvider>
    </Provider>
  );
}

export default App;
