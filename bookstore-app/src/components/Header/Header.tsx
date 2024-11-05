import { images } from "../../assets/export";

import "../../css/header.css";

export const Header = (): JSX.Element => {
  return (
    <header className="header_container">
      <img className="header_logo" src={images.libraryLogo} alt="logo"></img>
    </header>
  );
};
