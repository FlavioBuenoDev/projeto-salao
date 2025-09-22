import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Header from './components/Header/Header'
import Footer from './components/Footer/Footer'
import Home from './pages/Home'
import Agendamentos from './pages/Agendamentos'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/agendamentos" element={<Agendamentos />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  )
}

export default App