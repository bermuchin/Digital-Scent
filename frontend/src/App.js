import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Recommendation from './pages/Recommendation';
import PerfumeDetail from './pages/PerfumeDetail';
import PerfumeList from './pages/PerfumeList';
import './index.css';

function App() {
  return (
    <Router>
      <div className="App min-h-screen">
        <Navbar />
        <main className="pt-16">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/recommendation" element={<Recommendation />} />
            <Route path="/perfumes" element={<PerfumeList />} />
            <Route path="/perfumes/:id" element={<PerfumeDetail />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App; 