import type { JSX } from "react";

import assets from "@/assets/export";

import "@/components/Header/Header.css";

const Header = (): JSX.Element => {
  return (
    <header className="header-wrapper">
      <img className="header-wrapper__logo" src={assets.images.libraryLogo} alt="logo"></img>
    </header>
  );
};

export default Header;
