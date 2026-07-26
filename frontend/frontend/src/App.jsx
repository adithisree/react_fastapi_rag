import { useState } from "react";
import "./App.css";


function App() {
  let [question, setQuestion] = useState("");
  let [answer, setAnswer] = useState("");
  let [loading, setLoading] = useState(false);
  let [error, setError] = useState("");
  let handleSubmit = async function handlesubmit(e) {
      e.preventDefault();

  setLoading(true);
  setError("");
  setAnswer("");
  try {
  let response = await fetch("http://127.0.0.1:8000/api/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },  
    body: JSON.stringify({
      question: question,
    }),
  });

  let data = await response.json();
  setAnswer(data.answer);

} catch (err) {
  setError("Failed to connect to the backend.");

} finally {
  setLoading(false);
}

  };
  
  return (
    <div className="container">
      <h1>Question Answering Application</h1>

      <form  onSubmit={handleSubmit}>
       {loading && <p>Loading...</p>}

{error && <p className="error">{error}</p>}

        <input type="text" placeholder="Ask the question" 
              value={question}
           onChange={(e) => setQuestion(e.target.value)}></input><br></br>

        
          <div className="button-container">
          <button type="submit">Go</button>
    </div>
      </form>
      {answer && (
  <div  classname="answer-container">
    <h3 >Answer</h3>
    <p >{answer}</p>
  </div>
)}
     
    </div>
  );
}

export default App;