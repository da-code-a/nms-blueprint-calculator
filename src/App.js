import React from "react";
import { getBlueprintsByCategory } from "./services/BlueprintService";
import "react-loader-spinner/dist/loader/css/react-spinner-loader.css";
import { Puff } from "react-loader-spinner";

import "./App.css";

function App() {

  var loading = true;

  var blueprints = null;
  getBlueprintsByCategory().then(response => {
    loading = false;
    blueprints = response;
  })

  return (
    <div className="App">
      <header className="app-header">No Man's Sky Blueprint Calculator</header>
      <div className="main-container">
        {loading ? <Puff height="100" width="100" color="gray" ariaLabel="loading" /> : <pre>{JSON.stringify(blueprints, null, 2)}</pre>}
      </div>
    </div>
  );
}

export default App;
