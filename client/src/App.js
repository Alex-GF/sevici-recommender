import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import StationFilter from './pages/stationFilter';
import Predictor from './pages/predictor';
import Research from './pages/research';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route path="/filter" element={<StationFilter />} />
        <Route path="/predictor" element={<Predictor />} />
        <Route path="/research" element={<Research />} />
      </Routes>
    </Router>
  );
}

export default App;
