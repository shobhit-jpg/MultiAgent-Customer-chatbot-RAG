import { useState } from "react";
import LandingPage from "./components/LandingPage";
import ChatBox from "./components/ChatBox";
import "./App.css";

function App() {
  const [startChat, setStartChat] = useState(false);

  return (
    <>
      {startChat ? (
        <ChatBox />
      ) : (
        <LandingPage onStart={() => setStartChat(true)} />
      )}
    </>
  );
}

export default App;