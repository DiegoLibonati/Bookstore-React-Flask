import { Fragment } from "react/jsx-runtime";

import { Header } from "./components/Header/Header";
import { Main } from "./components/Main/Main";

function App(): JSX.Element {
  return (
    <Fragment>
      <Header></Header>
      <Main></Main>
    </Fragment>
  );
}

export default App;
