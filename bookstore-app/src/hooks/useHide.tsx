import { useState } from "react";
import { UseHide } from "../entities/entities";

export const useHide = (): UseHide => {
  const [hide, setHide] = useState<boolean>(false);

  const handleHide = (): void => {
    if (hide) {
      setHide(false);
      return;
    }

    setHide(true);
    return;
  };

  return {
    hide,
    handleHide,
  };
};
