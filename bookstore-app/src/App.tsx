import { Fragment } from "react/jsx-runtime";

import { Header } from "@src/components/Header/Header";
import { Main } from "@src/components/Main/Main";

function App(): JSX.Element {
  return (
    <Fragment>
      <Header></Header>
      <Main></Main>
    </Fragment>
  );
}

export default App;
