import './App.css';

import Header from './components/Header/Header';
import Input from './components/Input/Input';
import Footer from './components/Footer/Footer';


function App() {
  return (
    <div className="App">
      <div className="wrapper" data-testid="Wrapper">
        <Header />
        <Input />
        <Footer />
      </div>
    </div>
  );
}

export default App;
