import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [data, setData] = useState(null);
  // const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    async function fetchData() {
      // setLoading(true);
      const response = await fetch("/api/data");
      const result = await response.json();
      setData(result);
      // setLoading(false);
    }
    
    fetchData();
  }, []);
  
  // Render
  // if(loading) {
  //   return null; // loading
  // }
  
  return <div>{data.someProperty}</div>;
  return (
    <>
      <div>
        <h1>EventHub</h1>
      </div>
        
    </>
  )
}

export default App
