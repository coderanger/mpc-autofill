import * as React from "react";
import App from "./editor/App";
import store from "./editor/store";
import { Provider } from "react-redux";
import * as ReactDOMClient from "react-dom/client";

import "../scss/styles.scss";
import "../css/custom.css";

// require("./base.js");
// require("bootstrap/js/dist/dropdown");
require("bootstrap-icons/font/bootstrap-icons.css");

import "bootstrap5-toggle/css/bootstrap5-toggle.min.css";
import "bootstrap5-toggle";

const root = ReactDOMClient.createRoot(
  document.getElementById("app") as HTMLElement
);
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);
