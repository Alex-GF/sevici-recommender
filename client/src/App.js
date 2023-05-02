import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import Predictor from './pages/predictor';
import Graphs from './pages/graphs';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route path="/predictor" element={<Predictor />} />
        <Route path="/graphs" element={<Graphs />} />
      </Routes>
    </Router>
  );
}

export default App;
