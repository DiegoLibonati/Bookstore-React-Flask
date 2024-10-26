import { Fragment } from "react/jsx-runtime";

import { Header } from "./components/Header";
import { Main } from "./components/Main";

import "./styles.css";

function App(): JSX.Element {
  return (
    <Fragment>
      <Header></Header>
      <Main></Main>
    </Fragment>
  );
}

export default App;
