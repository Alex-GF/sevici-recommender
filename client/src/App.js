import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './pages/home';
import Predictor from './pages/predictor';

function App() {
  return (
    <Router>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route path="/predictor" element={<Predictor />} />
      </Routes>
    </Router>
  );
}

export default App;
